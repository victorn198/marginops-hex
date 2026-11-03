_ds = np.arange(0, 20.5, 2.5)
_ks = np.arange(0, 25.5, 5)
_z = np.array([[uplift_necessario(dd / 100, kk / 100) for dd in _ds] for kk in _ks])
fig_sens = go.Figure(go.Heatmap(
    z=np.where(np.isnan(_z), None, _z * 100), x=[f"{v:g}%" for v in _ds], y=[f"+{v:g}%" for v in _ks],
    colorscale=[[0, "#E8F1F2"], [0.5, "#3A9188"], [1, "#E0A100"]],
    text=[["sem solução" if np.isnan(v) else f"+{v*100:.0f}%" for v in row] for row in _z], texttemplate="%{text}",
    hovertemplate="Desconto %{x}, custo %{y}: volume necessário %{text}<extra></extra>", colorbar=dict(title="Volume<br>necessário (%)")))
fig_sens.add_trace(go.Scatter(x=[f"{min(_ds, key=lambda v: abs(v - desconto_adicional_pct)):g}%"],
                              y=[f"+{min(_ks, key=lambda v: abs(v - inflacao_custo_pct)):g}%"], mode="markers",
                              marker=dict(symbol="square-open", size=46, color=PALETA["navy"], line=dict(width=3)),
                              name="Cenário atual (mais próximo)", hoverinfo="skip"))
fig_sens.update_layout(title="Volume necessário para preservar o lucro bruto",
                       xaxis_title="Desconto adicional", yaxis_title="Inflação do custo unitário", template="plotly_white",
                       height=430, font=dict(color=PALETA["navy"]), showlegend=False)
fig_sens

_mx_style(fig_sens)
