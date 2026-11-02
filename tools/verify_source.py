from pathlib import Path
from decimal import Decimal
import duckdb, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'published'
OUT=ROOT/'outputs'/'verification'
OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((DATA/'manifest.json').read_text())
c=duckdb.connect()
c.execute("SET memory_limit='2GB'")
checks={}
for name,meta in manifest['tables'].items():
    file=DATA/meta['file']
    assert hashlib.sha256(file.read_bytes()).hexdigest()==meta['sha256'],name
    c.execute(f"CREATE VIEW {name} AS SELECT * FROM read_parquet('{file.as_posix()}')")
    count=c.execute(f'SELECT count(*) FROM {name}').fetchone()[0]
    assert count==meta['rows'],name
    checks[f'{name}_source_rows']=count

for table,key in [('orders','OrderKey'),('customer','CustomerKey'),('product','ProductKey'),('store','StoreKey')]:
    duplicates=c.execute(f'SELECT count(*)-count(DISTINCT {key}) FROM {table}').fetchone()[0]
    assert duplicates==0,(table,'duplicate key')
    checks[f'{table}_duplicate_keys']=duplicates

for table,cols in [('sales','OrderKey, LineNumber'),('orderrows','OrderKey, RowNumber')]:
    duplicates=c.execute(f'SELECT sum(n-1) FROM (SELECT count(*) n FROM {table} GROUP BY {cols} HAVING count(*)>1)').fetchone()[0] or 0
    assert duplicates==0,(table,'duplicate grain')
    checks[f'{table}_duplicate_rows']=duplicates

join='FROM sales s LEFT JOIN product p USING(ProductKey) LEFT JOIN customer c USING(CustomerKey) LEFT JOIN store st USING(StoreKey)'
row=c.execute('SELECT count(*),count(*) FILTER (WHERE p.ProductKey IS NULL),count(*) FILTER (WHERE c.CustomerKey IS NULL),count(*) FILTER (WHERE st.StoreKey IS NULL) '+join).fetchone()
assert row==(manifest['tables']['sales']['rows'],0,0,0),row
checks['joined_rows_and_orphans']=row
invalid=c.execute('SELECT count(*) FROM sales WHERE Quantity<=0 OR UnitPrice<0 OR NetPrice<0 OR UnitCost<0 OR NetPrice>UnitPrice OR ExchangeRate<=0 OR OrderDate IS NULL').fetchone()[0]
assert invalid==0,invalid
checks['invalid_business_rows']=invalid

summary={}
for year in [2024,2025]:
    row=c.execute('''SELECT count(*),count(DISTINCT OrderKey),sum(Quantity),sum(Quantity*UnitPrice),sum(Quantity*NetPrice),sum(Quantity*UnitCost),sum(Quantity*(UnitPrice-NetPrice)),sum(Quantity*(NetPrice-UnitCost)) FROM sales WHERE year(OrderDate)=?''',[year]).fetchone()
    keys=['line_items','orders','units','gross_sales_usd','net_sales_usd','cogs_usd','discounts_usd','gross_profit_usd']
    result=dict(zip(keys,row))
    assert result['gross_sales_usd']-result['discounts_usd']==result['net_sales_usd']
    assert result['net_sales_usd']-result['cogs_usd']==result['gross_profit_usd']
    result['gross_margin']=result['gross_profit_usd']/result['net_sales_usd']
    summary[year]=result

reconciled=c.execute('''SELECT count(*),sum(r.Quantity*r.NetPrice),sum(r.Quantity*r.UnitCost) FROM orders o JOIN orderrows r USING(OrderKey) WHERE year(o.DT)=2025''').fetchone()
assert reconciled[0]==summary[2025]['line_items']
assert reconciled[1]==summary[2025]['net_sales_usd']
assert reconciled[2]==summary[2025]['cogs_usd']
checks['orders_rows_vs_sales_2025_reconciled']=True

fx_bad=c.execute('''SELECT count(*) FROM sales s LEFT JOIN currencyexchange fx ON fx.Date=s.OrderDate AND fx.FromCurrency='USD' AND fx.ToCurrency=s.CurrencyCode WHERE fx.Exchange IS NULL OR abs(fx.Exchange-s.ExchangeRate)>0.00001''').fetchone()[0]
assert fx_bad==0,fx_bad
checks['unmatched_or_different_fx']=fx_bad

# Independent row-by-row recomputation from the normalized order representation
# for one complete month; Python Decimal does the arithmetic, not the summary SQL.
rows=c.execute('''SELECT r.Quantity,r.NetPrice,r.UnitCost FROM orders o JOIN orderrows r USING(OrderKey) WHERE o.DT>='2025-01-01' AND o.DT<'2025-02-01' ''').fetchall()
independent_net=sum((Decimal(q)*n for q,n,_ in rows),Decimal(0))
independent_cost=sum((Decimal(q)*k for q,_,k in rows),Decimal(0))
native=c.execute("SELECT sum(Quantity*NetPrice),sum(Quantity*UnitCost) FROM sales WHERE OrderDate>='2025-01-01' AND OrderDate<'2025-02-01'").fetchone()
assert (independent_net,independent_cost)==native
checks['independent_decimal_reconciliation_jan_2025']={'rows':len(rows),'net_sales_usd':independent_net,'cogs_usd':independent_cost}

store_keys=c.execute('SELECT StoreKey,StoreCode,Description,CountryCode FROM store ORDER BY StoreKey LIMIT 4').fetchall()
online_keys=c.execute("SELECT StoreKey,StoreCode,Description,CountryCode FROM store WHERE StoreCode<0 OR lower(Description) LIKE '%online%'").fetchall()
countries=c.execute('SELECT DISTINCT Country,CountryFull FROM customer ORDER BY 2').fetchall()
categories=c.execute('SELECT DISTINCT CategoryName FROM product ORDER BY 1').fetchall()
customer_versions=c.execute("SELECT count(*) FILTER(WHERE EndDT<'2099-01-01'),min(StartDT),max(EndDT) FROM customer").fetchone()
report={'status':'passed','checks':checks,'year_summaries':summary,'store_keys_sample':store_keys,'online_store_keys':online_keys,'countries':countries,'categories':categories,'customer_version_dates':customer_versions,'currency_semantics':'Base prices and transaction costs are NOT multiplied by FX in the SQLBI generator. Consolidated metrics stay in base USD; source Engine.cs lines 272-277 and 516-532.'}
(OUT/'source-checks.json').write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
print(json.dumps({'status':'passed','checks':len(checks),'summary':summary,'store_sample':store_keys,'online_store_keys':online_keys,'countries':countries,'categories':categories,'customer_versions':customer_versions},default=str))
