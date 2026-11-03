import itertools
import plotly.graph_objects as go

PALETA = {"navy": "#1B2A41", "azul": "#2F6690", "teal": "#3A9188", "ambar": "#E0A100", "cinza": "#8A94A6", "claro": "#F4F6F9"}

_w = base_pvm.pivot_table(index="ProductKey", columns="periodo", values=["unidades", "receita_liquida"], aggfunc="sum", fill_value=0)
_w.columns = [f"{a}_{b}" for a, b in _w.columns]
for _col in ["unidades_atual", "unidades_anterior", "receita_liquida_atual", "receita_liquida_anterior"]:
    if _col not in _w:
        _w[_col] = 0.0
_w = _w.astype(float)
U0, U1 = _w.unidades_anterior.sum(), _w.unidades_atual.sum()
R0, R1 = _w.receita_liquida_anterior.sum(), _w.receita_liquida_atual.sum()

pvm_ok = U0 > 0 and U1 > 0
if pvm_ok:
    p0 = np.where(_w.unidades_anterior > 0, _w.receita_liquida_anterior / _w.unidades_anterior.replace(0, np.nan), np.nan)
    p1 = np.where(_w.unidades_atual > 0, _w.receita_liquida_atual / _w.unidades_atual.replace(0, np.nan), np.nan)
    p0, p1 = np.where(np.isnan(p0), p1, p0), np.where(np.isnan(p1), p0, p1)
    s0, s1 = (_w.unidades_anterior / U0).values, (_w.unidades_atual / U1).values
    est = {"U": (U0, U1), "s": (s0, s1), "p": (p0, p1)}
    f = lambda U, s, p: U * float(np.sum(s * p))
    efeito = {fat: 0.0 for fat in est}
    perms = list(itertools.permutations(est))
    for ordem in perms:
        cur = {fat: est[fat][0] for fat in est}
        for fat in ordem:
            antes = f(cur["U"], cur["s"], cur["p"])
            cur[fat] = est[fat][1]
            efeito[fat] += (f(cur["U"], cur["s"], cur["p"]) - antes) / len(perms)
    residuo = (R1 - R0) - sum(efeito.values())
    if abs(residuo) > 1e-6 * max(1.0, abs(R1 - R0)):
        raise RuntimeError(f"Decomposição não reconcilia: resíduo {residuo}")
else:
    efeito = {"U": np.nan, "s": np.nan, "p": np.nan}
    residuo = np.nan

n_novos = int(((_w.unidades_anterior == 0) & (_w.unidades_atual > 0)).sum())
n_desc = int(((_w.unidades_anterior > 0) & (_w.unidades_atual == 0)).sum())
pvm = pd.DataFrame({
    "componente": [f"Receita {ano-1}", "Volume (unidades totais)", "Mix (participação dos produtos)", "Preço (preço líquido médio por produto)", f"Receita {ano}"],
    "valor_usd": [R0, efeito["U"], efeito["s"], efeito["p"], R1],
})
fmt_br = lambda v: f"{v:,.0f}".replace(",", ".")
pvm_nota = (f"Δ receita = USD {fmt_br(R1-R0)} = volume {fmt_br(efeito['U'])} + mix {fmt_br(efeito['s'])} + preço {fmt_br(efeito['p'])} "
            f"(resíduo numérico {abs(residuo):.1e}). Produtos novos no recorte: {n_novos}; descontinuados: {n_desc}." if pvm_ok
            else "Decomposição indisponível: um dos períodos não tem unidades vendidas neste recorte.")

fig_pvm = go.Figure(go.Waterfall(
    orientation="v", measure=["absolute", "relative", "relative", "relative", "total"],
    x=pvm.componente, y=pvm.valor_usd.fillna(0),
    increasing={"marker": {"color": PALETA["teal"]}}, decreasing={"marker": {"color": PALETA["ambar"]}},
    totals={"marker": {"color": PALETA["navy"]}},
    text=[f"{v/1e6:,.1f} mi".replace(".", ",") if pd.notna(v) else "—" for v in pvm.valor_usd], textposition="outside",
    connector={"line": {"color": PALETA["cinza"]}}))
fig_pvm.update_layout(title=f"Ponte da receita · {ano-1} → {ano}", template="plotly_white",
                      yaxis_title="USD", height=430,
                      yaxis_range=[0.8 * min(R0, R1), 1.08 * max(R0, R1)] if pvm_ok else None, margin=dict(t=60, b=40), font=dict(color=PALETA["navy"]))
fig_pvm

_mx_style(fig_pvm)
