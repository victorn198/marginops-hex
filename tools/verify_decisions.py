"""Independent business and temporal-validation reference for the Hex review."""
from pathlib import Path
from itertools import permutations
from decimal import Decimal
import duckdb, numpy as np, pandas as pd, json

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'published'
OUT=ROOT/'outputs'/'verification'
OUT.mkdir(parents=True,exist_ok=True)
c=duckdb.connect()
c.execute("SET memory_limit='2GB'")
sales=(DATA/'sales.parquet').as_posix()

# Decomposition is an arithmetic identity, not an estimate of causal impact.
p=c.execute(f'''SELECT ProductKey,year(OrderDate) y,sum(Quantity)::DOUBLE q,
sum(Quantity*NetPrice)::DOUBLE r FROM read_parquet('{sales}')
WHERE year(OrderDate) IN (2024,2025) GROUP BY 1,2''').df()
q=p.pivot(index='ProductKey',columns='y',values='q').fillna(0)
r=p.pivot(index='ProductKey',columns='y',values='r').fillna(0).reindex(q.index)
q0,q1=q[2024].to_numpy(),q[2025].to_numpy()
r0,r1=r[2024].to_numpy(),r[2025].to_numpy()
p0=np.divide(r0,q0,out=np.zeros_like(r0),where=q0>0)
p1=np.divide(r1,q1,out=np.zeros_like(r1),where=q1>0)
# A product with no volume has no observed price: carry its observed price to
# the absent side; entry/exit is therefore attributed to volume/mix, not price.
p0=np.where(q0>0,p0,p1)
p1=np.where(q1>0,p1,p0)
factors={'volume':(q0.sum(),q1.sum()),'mix':(q0/q0.sum(),q1/q1.sum()),'price':(p0,p1)}
def revenue(state): return float(state['volume']*np.dot(state['mix'],state['price']))
effects=dict.fromkeys(factors,0.)
for sequence in permutations(factors):
    state={k:v[0] for k,v in factors.items()}
    previous=revenue(state)
    for key in sequence:
        state[key]=factors[key][1]
        current=revenue(state)
        effects[key]+=(current-previous)/6
        previous=current
delta=float(r1.sum()-r0.sum())
assert abs(sum(effects.values())-delta)<.01
decomposition={'baseline_year':2024,'current_year':2025,'revenue_delta_usd':delta,'effects_usd':effects,'reconciliation_error_usd':sum(effects.values())-delta,'method':'Symmetric Shapley across aggregate units, product unit shares and average net unit prices; all 6 permutations.'}

revenue_base,cogs_base=c.execute(f"SELECT sum(Quantity*NetPrice),sum(Quantity*UnitCost) FROM read_parquet('{sales}') WHERE year(OrderDate)=2025").fetchone()
gp_base=revenue_base-cogs_base
scenarios=[]
for discount,inflation,uplift in [(0,0,0),(5,10,15),(20,25,50)]:
    d,i,u=[Decimal(v)/100 for v in (discount,inflation,uplift)]
    net=revenue_base*(1-d)*(1+u)
    cogs=cogs_base*(1+i)*(1+u)
    contribution=revenue_base*(1-d)-cogs_base*(1+i)
    required=(gp_base/contribution-1) if contribution>0 else None
    scenarios.append({'additional_discount_pct':discount,'cost_inflation_pct':inflation,'assumed_volume_uplift_pct':uplift,'net_sales_usd':net,'cogs_usd':cogs,'gross_profit_usd':net-cogs,'delta_gross_profit_usd':net-cogs-gp_base,'required_volume_uplift':required})
assert scenarios[0]['gross_profit_usd']==gp_base

# Regular complete weeks only; initial/final partial weeks are excluded.
weekly=c.execute(f'''WITH bounds AS (SELECT min(OrderDate)::DATE lo,max(OrderDate)::DATE hi FROM read_parquet('{sales}')),
a AS (SELECT date_trunc('week',OrderDate)::DATE AS week_start,sum(Quantity*NetPrice)::DOUBLE AS net FROM read_parquet('{sales}') GROUP BY 1)
SELECT week_start,net FROM a,bounds WHERE week_start>=lo AND week_start+INTERVAL 7 DAY<=hi+INTERVAL 1 DAY ORDER BY week_start''').df()
series=weekly.set_index('week_start')['net'].asfreq('W-MON',fill_value=0)
assert len(series)>150

def feature(history,date):
    a=np.asarray(history,dtype=float)
    week=int(date.isocalendar().week)
    return np.array([a[-1],a[-2],a[-4],a[-13],a[-52],a[-4:].mean(),a[-13:].mean(),len(a),np.sin(2*np.pi*week/52.18),np.cos(2*np.pi*week/52.18)])

def ridge_fit_predict(train,horizon=4,alpha=10.):
    history=train.to_numpy(dtype=float)
    X=np.array([feature(history[:n],train.index[n]) for n in range(52,len(history))])
    y=history[52:]
    center=X.mean(axis=0); scale=X.std(axis=0); scale=np.where(scale<1e-8,1.,scale)
    X=np.column_stack([np.ones(len(X)),(X-center)/scale])
    penalty=np.eye(X.shape[1])*alpha; penalty[0,0]=0
    coef=np.linalg.solve(X.T@X+penalty,X.T@y)
    path=list(history); result=[]
    for step in range(horizon):
        date=train.index[-1]+pd.Timedelta(weeks=step+1)
        x=np.r_[1.,(feature(path,date)-center)/scale]
        value=max(0.,float(x@coef))
        path.append(value); result.append(value)
    return np.array(result)

folds=[]
for cutoff in range(len(series)-24,len(series),4):
    train=series.iloc[:cutoff]
    actual=series.iloc[cutoff:cutoff+4].to_numpy()
    predicted=ridge_fit_predict(train)
    seasonal=np.array([train.iloc[-52+h] for h in range(4)])
    assert train.index.max()<series.index[cutoff]
    for model,pred in [('ridge_recursive',predicted),('seasonal_naive_52w',seasonal)]:
        folds.append({'origin':str(train.index.max().date()),'first_test_week':str(series.index[cutoff].date()),'model':model,'absolute_error_sum':float(np.abs(actual-pred).sum()),'actual_sum':float(actual.sum()),'n':len(actual)})

scores={}
for model in ['ridge_recursive','seasonal_naive_52w']:
    results=[x for x in folds if x['model']==model]
    error=sum(x['absolute_error_sum'] for x in results)
    scores[model]={'wape':error/sum(x['actual_sum'] for x in results),'mae_usd':error/sum(x['n'] for x in results),'origins':len(results),'weeks_tested':sum(x['n'] for x in results)}
winner=min(scores,key=lambda name:scores[name]['wape'])
future=ridge_fit_predict(series) if winner=='ridge_recursive' else np.array([series.iloc[-52+h] for h in range(4)])
report={'status':'passed','decomposition':decomposition,'scenario_cases':scenarios,'forecast_reference':{'complete_week_count':len(series),'first_week':str(series.index[0].date()),'last_week':str(series.index[-1].date()),'scores':scores,'best_on_historical_wape':winner,'next_four_weeks_usd':future.tolist(),'validation':'6 non-overlapping rolling origins; 4-week recursive horizon; fixed alpha; training and scaling use only past observations; no future actual lags. Historical comparison, not guaranteed future accuracy.','folds':folds}}
(OUT/'decision-checks.json').write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
print(json.dumps({'decomposition':decomposition,'scenario_cases':scenarios,'forecast_scores':scores,'historical_winner':winner},default=str))
