select modelo as "Modelo", round(WAPE * 100, 2) as "WAPE (%)", cast(round(MAE_usd, 2) as decimal(18,2)) as "Erro absoluto médio (USD)" from metricas_prev order by WAPE
