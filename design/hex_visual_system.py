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
