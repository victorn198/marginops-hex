"""Presentation helpers for native MarginOps Hex cells; no metric calculations."""
from html import escape as _mx_escape
from IPython.display import HTML as _mx_HTML

_mx_css = """<style>
.mx{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;color:#172b42;box-sizing:border-box;line-height:1.5}
.mx *{box-sizing:border-box}.mx-head{position:relative;overflow:hidden;border:1px solid #233e58;border-radius:16px;padding:26px 30px;background:linear-gradient(120deg,#102238 0%,#18394c 100%);color:#fff;box-shadow:0 10px 25px -20px #10223866}
.mx-head:after{content:'';position:absolute;width:210px;height:210px;border:1px solid #ffffff10;border-radius:50%;right:10px;top:-105px;pointer-events:none}
.mx-brand{display:flex;align-items:center;gap:11px;font-size:32px;font-weight:740;letter-spacing:-1.3px;line-height:1.1}.mx-mark{display:block;width:10px;height:25px;transform:skew(-15deg);border-radius:3px;background:#71d6bf;box-shadow:8px 0 0 #71d6bf45;margin-right:8px}
.mx-head p{font-size:14px;color:#cbdde7;margin:9px 0 17px;max-width:780px}.mx-kicker{font-size:10px;letter-spacing:1.7px;text-transform:uppercase;font-weight:650;color:#83c9bb;margin-bottom:12px}
.mx-chips{display:flex;gap:7px;flex-wrap:wrap}.mx-chip{font-size:10px;font-weight:550;letter-spacing:.1px;padding:5px 9px;border:1px solid #ffffff20;border-radius:5px;background:#ffffff08;color:#dce8ed}
.mx-section{display:flex;align-items:flex-start;gap:15px;padding:8px 0 17px;border-bottom:1px solid #dfe7ef;margin:3px 0 10px}
.mx-number{display:flex;align-items:center;justify-content:center;width:36px;height:36px;flex:none;border:1px solid #dce5ee;background:#edf3f8;border-radius:9px;color:#31546d;font-size:12px;font-weight:700;font-variant-numeric:tabular-nums}
.mx-section h2{font-size:24px;line-height:1.2;letter-spacing:-.7px;margin:0;font-weight:720}.mx-section p{font-size:12px;color:#64778a;max-width:1000px;margin:7px 0 0}
.mx-scope{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.mx-scope span{font-size:10px;color:#496277;background:#f0f5f8;border:1px solid #e1eaf0;padding:3px 7px;border-radius:4px}
.mx-tip{font-size:11px;color:#607486;padding:11px 0 0;margin:0}.mx-tip strong{color:#284a62;font-weight:650}
.mx-note{padding:18px 20px;border:1px solid #dce7ee;border-left:3px solid #298e7b;background:#f4f9f8;border-radius:0 10px 10px 0;font-size:12px;color:#274958}.mx-note h3{margin:0 0 9px;font-size:15px;letter-spacing:-.2px}.mx-note p{margin:6px 0}.mx-note li{margin:6px 0}.mx-note ul{padding-left:16px;margin:0}
.mx-metrics{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:15px 0 8px}.mx-metric{min-width:0;padding:17px 16px 15px;border:1px solid #dfe8ef;border-radius:12px;background:linear-gradient(155deg,#fff,#f8fafc);box-shadow:0 4px 12px -10px #19364b44;overflow:hidden}.mx-metric:first-child{border-top:3px solid #228f7c;padding-top:15px}.mx-label{font-size:10px;font-weight:650;color:#657d90;text-transform:uppercase;letter-spacing:.65px;min-height:18px}.mx-value{font-size:27px;line-height:1.2;font-weight:740;letter-spacing:-1.1px;font-variant-numeric:tabular-nums;margin:9px 0 11px;color:#15334b;white-space:nowrap}.mx-delta{display:inline-block;font-size:10px;font-weight:650;padding:4px 6px;border-radius:4px;color:#557184;background:#eaf0f4;white-space:nowrap}.mx-delta.up{color:#176d5b;background:#e1f3ec}.mx-delta.down{color:#a14955;background:#fae9ec}.mx-prior{font-size:10px;color:#7890a2;margin:13px 0 6px;font-variant-numeric:tabular-nums}.mx-bars{display:grid;gap:3px}.mx-bars i{display:block;height:3px;border-radius:3px;max-width:100%}.mx-bars i:first-child{background:#d5e1e9}.mx-bars i:last-child{background:#508c9b}
@media(max-width:900px){.mx-metrics{grid-template-columns:repeat(3,minmax(0,1fr))}.mx-metric:nth-last-child(-n+2){grid-column:span 1}.mx-value{font-size:25px}}
@media(max-width:620px){.mx-metrics{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.mx-metric:first-child{grid-column:1/-1}.mx-metric{padding:15px 12px}.mx-value{font-size:24px}}
@media(max-width:620px){.mx-head{padding:22px}.mx-brand{font-size:28px}.mx-section h2{font-size:21px}.mx-section{gap:10px}.mx-chip{font-size:9px}}
</style>
"""

def _mx_section(number, title, description="", scope=""):
    chips = "".join(f"<span>{_mx_escape(x.strip())}</span>" for x in str(scope).split("·") if x.strip())
    return _mx_HTML(_mx_css + f'<section class="mx mx-section"><div class="mx-number">{_mx_escape(str(number))}</div><div><h2>{_mx_escape(title)}</h2><p>{_mx_escape(description)}</p><div class="mx-scope">{chips}</div></div></section>')

def _mx_number(value, kind):
    import math
    if value is None or not math.isfinite(float(value)):
        return "—"
    value = float(value)
    if kind == "pct":
        return f"{value * 100:.1f}%".replace(".", ",")
    if kind == "count":
        return f"{value:,.0f}".replace(",", ".")
    if abs(value) >= 1_000_000:
        return (f"US$ {value / 1_000_000:.1f} mi").replace(".", ",")
    return "US$ " + f"{value:,.0f}".replace(",", ".")

def _mx_metric_strip(frame, selected_year):
    import math
    if frame is None or frame.empty:
        return _mx_HTML(_mx_css + '<p class="mx mx-note">Sem dados para o recorte selecionado.</p>')
    row = frame.iloc[0]
    specs = [
        ("receita_liquida", "Receita líquida", "usd", "receita_liquida_ant", True),
        ("lucro_bruto", "Lucro bruto", "usd", "lucro_bruto_ant", True),
        ("margem_bruta", "Margem bruta", "pct", "margem_bruta_ant", True),
        ("pedidos", "Pedidos distintos", "count", "pedidos_ant", False),
        ("ticket_medio", "Ticket médio", "usd", "ticket_medio_ant", False),
    ]
    missing = [x for spec in specs for x in (spec[0], spec[3]) if x not in frame.columns]
    if missing:
        raise ValueError("Campos necessários aos indicadores: " + ", ".join(missing))
    cards = []
    for field, title, kind, previous, semantic in specs:
        now, old = row[field], row[previous]
        valid = now is not None and old is not None and math.isfinite(float(now)) and math.isfinite(float(old))
        delta, cls, widths = "Comparação indisponível", "", (0, 0)
        if valid:
            now, old = float(now), float(old)
            scale = max(abs(now), abs(old), 1e-12)
            widths = (max(0, old) / scale * 100, max(0, now) / scale * 100)
            change = (now - old) * 100 if kind == "pct" else (now / old - 1) * 100 if old else None
            if change is not None:
                precision = 2 if kind == "pct" else 1
                sign = "+" if change > 0 else "−" if change < 0 else ""
                unit = " p.p." if kind == "pct" else "%"
                delta = f"{sign}{abs(change):.{precision}f}{unit} vs {int(selected_year)-1}".replace(".", ",", 1)
                cls = ("up" if change > 0 else "down") if semantic and change != 0 else ""
        cards.append(f'<article class="mx-metric"><div class="mx-label">{_mx_escape(title)}</div><div class="mx-value">{_mx_escape(_mx_number(now,kind))}</div><div class="mx-delta {cls}">{_mx_escape(delta)}</div><div class="mx-prior">{int(selected_year)-1} · {_mx_escape(_mx_number(old,kind))}</div><div class="mx-bars" aria-hidden="true"><i style="width:{widths[0]:.2f}%"></i><i style="width:{widths[1]:.2f}%"></i></div></article>')
    return _mx_HTML(_mx_css + '<section class="mx mx-metrics" aria-label="Indicadores comerciais">' + "".join(cards) + '</section>')

def _mx_style(figure):
    figure.update_layout(
        template="plotly_white", paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter, Arial, sans-serif", size=12, color="#274158"),
        title=dict(font=dict(size=18,color="#142d43",family="Inter, Arial, sans-serif"),x=0.02,xanchor="left"),
        margin=dict(l=60,r=32,t=80,b=70),
        hoverlabel=dict(bgcolor="#142d43",font_color="white",font_size=12,bordercolor="#142d43"),
        legend=dict(font=dict(size=11,color="#536a7d")),
        modebar=dict(bgcolor="rgba(255,255,255,.9)",color="#8597a7",activecolor="#147d70"),
    )
    heat = any(t.type == "heatmap" for t in figure.data)
    figure.update_xaxes(showgrid=False,zeroline=False,showline=False,tickfont=dict(size=11,color="#6a7e90"),title_font=dict(size=12),automargin=True)
    figure.update_yaxes(showgrid=not heat,gridcolor="#e6edf3",zeroline=False,showline=False,tickfont=dict(size=11,color="#6a7e90"),title_font=dict(size=12),automargin=True)
    for trace in figure.data:
        if trace.type == "scatter":
            trace.line.width = 2.6
            if trace.mode and "markers" in trace.mode and trace.marker.symbol != "square-open":
                trace.marker.size = 5
        if trace.type == "heatmap":
            trace.colorscale = ([[0,"#f5f8fa"],[0.5,"#f8e5c3"],[1,"#e6b46d"]]
                if "Volume" in str(trace.colorbar.title.text) else [[0,"#f4f8fa"],[0.5,"#c4e6df"],[1,"#65b8a6"]])
            trace.colorbar.thickness = 10
            trace.colorbar.outlinewidth = 0
            trace.textfont = dict(size=11,color="#183b4b")
    return figure

_mx_HTML(_mx_css + '''<header class="mx mx-head">
<div class="mx-kicker">Inteligência comercial e rentabilidade</div>
<div class="mx-brand"><span class="mx-mark" aria-hidden="true"></span>MarginOps</div>
<p>Receita, composição de vendas e clientes — do desempenho histórico às decisões de margem.</p>
<div class="mx-chips"><span class="mx-chip">2,35 milhões de registros</span><span class="mx-chip">980.666 pedidos</span><span class="mx-chip">8 tabelas relacionadas</span><span class="mx-chip">Contoso · empresa fictícia</span><span class="mx-chip">USD · 2016–2025</span><span class="mx-chip">Por Victor Nogueira</span></div>
</header><p class="mx mx-tip"><strong>Explore:</strong> selecione o recorte abaixo e pressione <strong>Run</strong> para atualizar as análises. Os cenários são hipóteses; a base é sintética.</p>''')

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
