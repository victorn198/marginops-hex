_m = coortes.pivot(index="coorte_rotulo", columns="idade_anos", values="taxa_atividade").sort_index()
fig_coortes = go.Figure(go.Heatmap(
    z=_m.values, x=[f"Ano +{int(c)}" for c in _m.columns], y=_m.index.tolist(),
    colorscale=[[0, "#F4F6F9"], [0.5, "#7FB3D5"], [1, "#1B2A41"]], zmin=0, zmax=1,
    text=[[("" if pd.isna(v) else f"{v*100:.0f}%") for v in row] for row in _m.values], texttemplate="%{text}",
    hovertemplate="Coorte %{y}, %{x}: %{z:.1%}<extra></extra>", colorbar=dict(title="Ativos", tickformat=".0%")))
fig_coortes.update_layout(title="Atividade por idade da coorte",
                          template="plotly_white", height=430, yaxis=dict(autorange="reversed", title="Coorte de aquisição"),
                          xaxis_title="Idade (anos desde a primeira compra)", font=dict(color=PALETA["navy"]))
fig_coortes

_mx_style(fig_coortes)
