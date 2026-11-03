_ini = backtest["semana"].min() - pd.Timedelta(weeks=12)
_hist = semanal[pd.to_datetime(semanal["semana"]) >= _ini]
fig_prev = go.Figure()
fig_prev.add_trace(go.Scatter(x=_hist["semana"], y=_hist["receita_liquida"], name="Real (histórico)", line=dict(color=PALETA["navy"], width=2.5)))
fig_prev.add_trace(go.Scatter(x=backtest["semana"], y=backtest["ridge_ar"], name="Validação · ridge AR", mode="markers+lines",
                              line=dict(color=PALETA["azul"], dash="dot"), marker=dict(size=6)))
fig_prev.add_trace(go.Scatter(x=backtest["semana"], y=backtest["sazonal_ingenua_52s"], name="Validação · sazonal ingênuo", mode="markers+lines",
                              line=dict(color=PALETA["teal"], dash="dot"), marker=dict(size=6, symbol="diamond")))
fig_prev.add_trace(go.Scatter(x=previsao["semana"], y=previsao["ridge_ar"], name="Previsão · ridge AR", line=dict(color=PALETA["azul"], width=3)))
fig_prev.add_trace(go.Scatter(x=previsao["semana"], y=previsao["sazonal_ingenua_52s"], name="Previsão · sazonal ingênuo", line=dict(color=PALETA["ambar"], width=3)))
for _orig in backtest["origem"].unique():
    fig_prev.add_vline(x=pd.Timestamp(_orig), line=dict(color="#C9CED6", width=1, dash="dash"))
fig_prev.update_layout(title="Receita semanal · realizado, validação e projeção",
                       template="plotly_white", height=460, yaxis_title="USD", font=dict(color=PALETA["navy"]),
                       legend=dict(orientation="h", y=-0.15), margin=dict(t=60))
fig_prev

_mx_style(fig_prev)
