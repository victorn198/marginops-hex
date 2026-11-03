"""Compact presentation only. Inputs are the notebook's existing, validated results."""
from IPython.display import HTML as _dc_HTML
from html import escape as _dc_e
import plotly.graph_objects as _dc_go

_dc_css = '''<style>
*{box-sizing:border-box}body{margin:0} .dc{font:12px/1.35 Inter,Arial,sans-serif;color:#183047}
.dc-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:10px;border-bottom:1px solid #dfe8ef;padding-bottom:8px}.dc h2{font-size:19px;letter-spacing:-.5px;margin:0}.dc-scope{font-size:10px;color:#647b8d}.dc-sub{font-size:10px;color:#687f91;margin:4px 0}
.dc-kpis{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin:8px 0 12px}.dc-card{border:1px solid #dce6ed;border-radius:7px;padding:9px 11px;background:#f9fbfc;min-width:0}.dc-label{font-size:9px;color:#5f788c;font-weight:600;text-transform:uppercase;letter-spacing:.3px}.dc-value{font-size:22px;font-weight:700;letter-spacing:-.6px;line-height:1.2;margin:4px 0;white-space:nowrap}.dc-delta{font-size:10px;color:#5e7384}.dc-up{color:#147a66}.dc-down{color:#ab5961}
.dc-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.dc-three{grid-template-columns:1.15fr 1fr 1fr}.dc-panel{min-width:0;border:1px solid #e0e8ee;border-radius:7px;background:white;overflow:hidden}.dc-panel h3{font-size:12px;margin:9px 12px 0;font-weight:650}.dc-note{font-size:10px;background:#eff6f5;border-left:3px solid #298d7c;padding:7px 10px;margin:8px 0;color:#35586a}.dc details{font-size:11px;border-top:1px solid #e1e9ef;margin-top:9px;padding-top:7px}.dc summary{cursor:pointer;color:#426477;font-weight:600}.dc details p,.dc details pre{font:11px/1.5 Inter,Arial,sans-serif;white-space:pre-wrap;margin:8px 0;color:#5d7181}.dc-table{overflow:auto;max-height:285px}.dc table{border-collapse:collapse;width:100%;font-size:10px;text-align:left}.dc th{background:#edf3f7;color:#426077;white-space:nowrap;font-weight:600}.dc td,.dc th{padding:6px 9px;border-bottom:1px solid #e8eef2}.dc-caption{font-size:10px;color:#6b8091;margin:5px 0}
@media(max-width:760px){.dc-three{grid-template-columns:1fr}.dc-grid{grid-template-columns:1fr}.dc-head{align-items:flex-start;flex-direction:column;gap:3px}.dc-kpis{grid-template-columns:repeat(3,minmax(0,1fr))}.dc-value{font-size:20px}}
</style>'''

def _dc_doc(title, scope, body):
    return _dc_HTML(_dc_css + '<main class="dc"><header class="dc-head"><h2>' + _dc_e(title) + '</h2><span class="dc-scope">' + _dc_e(str(scope)) + '</span></header>' + body + '</main>')

def _dc_card(label, value, detail='', cls=''):
    return '<article class="dc-card"><div class="dc-label">'+_dc_e(label)+'</div><div class="dc-value">'+_dc_e(str(value))+'</div><div class="dc-delta '+cls+'">'+_dc_e(str(detail))+'</div></article>'

def _dc_num(value, kind='usd'):
    import math
    if value is None or not math.isfinite(float(value)): return '—'
    value=float(value)
    if kind=='pct': return f'{value*100:.1f}%'.replace('.',',')
    if kind=='count': return f'{value:,.0f}'.replace(',','.')
    return (f'US$ {value/1e6:.1f} mi'.replace('.',',') if abs(value)>=1e6 else 'US$ '+f'{value:,.0f}'.replace(',','.'))

def _dc_details(title, text):
    return '<details><summary>'+_dc_e(title)+'</summary><pre>'+_dc_e(str(text))+'</pre></details>'

def _dc_plot(figure, title, height=230):
    f=_dc_go.Figure(figure)
    f.update_layout(title=None,template='plotly_white',height=height,autosize=True,
        margin=dict(l=50,r=22,t=12,b=45),font=dict(family='Arial,sans-serif',size=10,color='#405c70'),
        paper_bgcolor='white',plot_bgcolor='white',legend=dict(orientation='h',y=-.22,x=0,font_size=9),
        hoverlabel=dict(bgcolor='#183047',font_color='white'),modebar=dict(color='#8298a9',activecolor='#168775'))
    f.update_xaxes(automargin=True,showline=False,zeroline=False,gridcolor='#edf2f5',title_font_size=10)
    f.update_yaxes(automargin=True,showline=False,gridcolor='#edf2f5',title_font_size=10)
    for t in f.data:
        if t.type=='heatmap': t.textfont=dict(size=9,color='#234354');t.colorbar.thickness=8
    return '<section class="dc-panel"><h3>'+_dc_e(title)+'</h3>'+f.to_html(full_html=False,include_plotlyjs='cdn',config={'responsive':True,'displayModeBar':'hover','displaylogo':False})+'</section>'

def _dc_delta_plot(frame, dimension):
    d=frame[frame.dimensao==dimension].sort_values('delta_lucro_bruto')
    names=[str(s) if len(str(s))<24 else str(s)[:21]+'…' for s in d.item]
    f=_dc_go.Figure(_dc_go.Bar(x=d.delta_lucro_bruto,y=names,orientation='h',
        marker_color=['#258b78' if v>=0 else '#ba7380' for v in d.delta_lucro_bruto],
        customdata=d[['item','delta_receita','delta_margem_pb']].values,
        hovertemplate='%{customdata[0]}<br>Δ lucro bruto: US$ %{x:,.0f}<br>Δ receita: US$ %{customdata[1]:,.0f}<br>Δ margem: %{customdata[2]:.0f} p.b.<extra></extra>'))
    f.update_xaxes(tickformat='.2s',title='Δ lucro bruto · USD')
    f.update_layout(showlegend=False)
    return f

def _dc_overview(kpis, mensal, contribuicoes, year, scope, narrative):
    r=kpis.iloc[0]; cards=[]
    for field,label,kind in [('receita_liquida','Receita líquida','usd'),('lucro_bruto','Lucro bruto','usd'),('margem_bruta','Margem bruta','pct'),('pedidos','Pedidos','count'),('ticket_medio','Ticket médio','usd')]:
        a,b=float(r[field]),float(r[field+'_ant']); delta=(a-b)*100 if kind=='pct' else (a/b-1)*100 if b else None
        text='Sem comparação' if delta is None else (f'{delta:+.2f} p.p.' if kind=='pct' else f'{delta:+.1f}%')+f' vs {year-1}'
        semantic=field in ('receita_liquida','lucro_bruto','margem_bruta')
        cards.append(_dc_card(label,_dc_num(a,kind),text.replace('.',',',1),'dc-up' if semantic and delta and delta>0 else 'dc-down' if semantic and delta and delta<0 else ''))
    f=_dc_go.Figure()
    for i,(name,df) in enumerate(mensal.groupby('serie',sort=True)):
        prior=str(year-1) in str(name); color='#1a8c79' if 'Lucro' in name else '#345f8b'
        f.add_trace(_dc_go.Scatter(x=df.mes,y=df.valor,name=name,mode='lines',line=dict(color=color,width=1.6 if prior else 2.4,dash='dot' if prior else 'solid'),hovertemplate='%{x}<br>US$ %{y:,.0f}<extra>%{fullData.name}</extra>'))
    f.update_yaxes(tickformat='.2s');f.update_xaxes(categoryorder='array',categoryarray=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'])
    body='<div class="dc-kpis">'+''.join(cards)+'</div>'
    body+='<div class="dc-grid dc-three">'+_dc_plot(f,'Receita e lucro bruto · meses',290)+_dc_plot(_dc_delta_plot(contribuicoes,'Categoria'),'Δ lucro bruto · categorias',290)+_dc_plot(_dc_delta_plot(contribuicoes,'Mercado'),'Δ lucro bruto · mercados',290)+'</div>'
    body+='<div class="dc-caption">Contoso · dados sintéticos · valores em USD. Pontilhado: ano anterior. Selecione o recorte acima e pressione Run.</div>'+_dc_details('Leitura detalhada do recorte',narrative)
    return _dc_doc('MarginOps · visão executiva',scope,body)

def _dc_motors(pvm_figure, contribuicoes, scope, note):
    d=contribuicoes[contribuicoes.dimensao=='Canal']; f=_dc_go.Figure()
    for col,label,color in [('receita_anterior','Ano anterior','#c3d1df'),('receita_atual','Ano selecionado','#298d7b')]:
        f.add_trace(_dc_go.Bar(x=d.item,y=d[col],name=label,marker_color=color,hovertemplate='%{x}<br>US$ %{y:,.0f}<extra>%{fullData.name}</extra>'))
    f.update_layout(barmode='group');f.update_yaxes(tickformat='.2s')
    body='<div class="dc-grid">'+_dc_plot(pvm_figure,'Preço, volume e mix · ponte de receita',280)+_dc_plot(f,'Receita por canal',280)+'</div>'
    body+=_dc_details('Como interpretar a decomposição',note+'\nAtribuição aritmética, sem inferência causal. O pivot abaixo mantém a exploração por categoria, canal e ano.')
    return _dc_doc('Motores de resultado',scope,body)

def _dc_cohorts(heat, recompra, year, market):
    d=recompra[recompra.maturada==True]
    f=_dc_go.Figure(_dc_go.Bar(x=d.coorte_rotulo,y=d.recompra_365d,marker_color='#328d80',customdata=d.clientes_iniciais,
        hovertemplate='Coorte %{x}<br>Recompra em 365 dias: %{y:.1%}<br>Clientes iniciais: %{customdata:,.0f}<extra></extra>'))
    f.update_yaxes(tickformat='.0%');f.update_layout(showlegend=False)
    body='<div class="dc-note">Cliente = registro CustomerKey. Categoria não se aplica a esta aba. Células imaturas permanecem em branco.</div><div class="dc-grid">'+_dc_plot(heat,'Atividade por idade da coorte',300)+_dc_plot(f,'Recompra em até 365 dias · coortes maduras',300)+'</div>'
    body+=_dc_details('Definição, maturidade e limitações','Primeira compra observada no histórico completo até o ano de corte. Atividade = clientes da coorte com pedido na idade / clientes iniciais. Recompra de 365 dias só é exibida quando todos os integrantes tiveram 365 dias de observação. 2016 é censurada à esquerda: a fonte começa em 18/05/2016. CustomerKey pode representar versões históricas; não há deduplicação garantida por pessoa física.')
    return _dc_doc('Clientes e coortes',f'Ano de corte: {year} · Mercado: {market}',body)

def _dc_forecast(figure, metrics, forecast, scope, note):
    cards=''.join(_dc_card(str(r.modelo),f'{r.WAPE*100:.2f}%'.replace('.',','),'WAPE · menor é melhor','dc-up' if r.WAPE==metrics.WAPE.min() else '') for r in metrics.itertuples())
    body='<div class="dc-kpis" style="grid-template-columns:1fr 1fr">'+cards+'</div>'+_dc_plot(figure,'Receita semanal · histórico, validação e projeção',250)
    tab=forecast.copy();tab['semana']=tab['semana'].dt.strftime('%d/%m/%Y') if hasattr(tab['semana'],'dt') else tab['semana'].astype(str).str[:10]
    for col in ['ridge_ar','sazonal_ingenua_52s']:tab[col]=tab[col].map(_dc_num)
    tab=tab[['semana','ridge_ar','sazonal_ingenua_52s']].rename(columns={'semana':'Semana','ridge_ar':'Ridge AR · USD','sazonal_ingenua_52s':'Referência sazonal · USD'})
    body+='<div class="dc-table">'+tab.to_html(index=False,border=0)+'</div>'+_dc_details('Validação temporal e limites',note+'\nSeis origens × quatro semanas. Treino só com o passado e previsão recursiva. Sem intervalos formais; não interpretar como garantia de resultado.')
    body+='<details><summary>Inspecionar WAPE e erro absoluto em USD</summary><div class="dc-table">'+metrics.round(4).to_html(index=False,border=0)+'</div></details>'
    return _dc_doc('Previsão e validação',scope,body)

def _dc_scenario_header(sim, scope):
    r=sim.iloc[0]
    specs=[('Receita do cenário',r.receita_liquida_cenario,'usd'),('Lucro bruto',r.lucro_bruto_cenario,'usd'),('Margem bruta',r.margem_cenario,'pct'),('Volume necessário',r.uplift_necessario,'pct')]
    body='<div class="dc-kpis" style="grid-template-columns:repeat(4,1fr)">'+''.join(_dc_card(label,_dc_num(value,kind),'Cenário hipotético') for label,value,kind in specs)+'</div>'
    return _dc_doc('Simulador de margem',scope,body)

def _dc_scenario_plots(sensitivity, curve, message):
    body='<div class="dc-note">'+_dc_e(message.replace('**',''))+'</div><div class="dc-grid">'+_dc_plot(sensitivity,'Volume necessário · desconto × custo',255)+_dc_plot(curve,'Δ lucro bruto × volume assumido',255)+'</div>'
    body+=_dc_details('Premissas e fórmulas','Receita = N0 × (1−desconto) × (1+volume). CPV = C0 × (1+custo) × (1+volume). Lucro bruto = receita − CPV. Volume necessário = GP0 / [N0(1−desconto) − C0(1+custo)] − 1. Sem solução positiva e finita quando a contribuição unitária é nula ou negativa. Mix constante; volume é uma premissa, não elasticidade estimada. Altere as três premissas e pressione Run.')
    return _dc_HTML(_dc_css+'<main class="dc">'+body+'</main>')

def _dc_quality(integrity, reference, methodology):
    a=int(integrity.ok.sum());b=int(reference.ok.sum());failed=int((~integrity.ok).sum()+(~reference.ok).sum())
    body='<div class="dc-kpis" style="grid-template-columns:repeat(3,1fr)">'+_dc_card('Integridade',a,f'{len(integrity)} verificações','dc-up')+_dc_card('Referências numéricas',b,f'{len(reference)} verificações no recorte','dc-up')+_dc_card('Falhas',failed,'Execução interrompe em divergências','dc-up' if not failed else 'dc-down')+'</div>'
    for label,frame in [('Inspecionar verificações de integridade',integrity),('Inspecionar comparações de referência',reference)]:
        body+='<details><summary>'+label+'</summary><div class="dc-table">'+frame.to_html(index=False,border=0)+'</div></details>'
    body+=_dc_details('Fonte, dicionário de métricas e metodologia',methodology)
    return _dc_doc('Qualidade e metodologia','Contoso · empresa fictícia · preços e custos em USD',body)
