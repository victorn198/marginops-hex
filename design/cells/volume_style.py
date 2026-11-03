_us = np.arange(0, 51, 1)
_gp = np.array([cenario(d_desc, k_custo, uu / 100)[2] for uu in _us]) - GP0
fig_curva = go.Figure()
fig_curva.add_trace(go.Scatter(x=_us, y=_gp, mode="lines", line=dict(color=PALETA["azul"], width=3), name="Δ lucro bruto do cenário",
                               hovertemplate="Volume +%{x}%: Δ lucro bruto %{y:$,.0f}<extra></extra>"))
fig_curva.add_hline(y=0, line=dict(color=PALETA["cinza"], dash="dash"))
fig_curva.add_vline(x=aumento_volume_pct, line=dict(color=PALETA["navy"], width=1.5), annotation_text="volume assumido")
if not np.isnan(uplift_req) and uplift_req * 100 <= 50:
    fig_curva.add_vline(x=uplift_req * 100, line=dict(color=PALETA["ambar"], width=2), annotation_text="ponto de equilíbrio", annotation_position="bottom right")
fig_curva.update_layout(title="Lucro bruto por cenário de volume",
                        xaxis_title="Aumento de volume assumido (%)", yaxis_title="Δ lucro bruto vs histórico (USD)",
                        template="plotly_white", height=400, font=dict(color=PALETA["navy"]), showlegend=False)
fig_curva

_mx_style(fig_curva)
