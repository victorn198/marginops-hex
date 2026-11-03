select strftime(semana, '%d/%m/%Y') as "Semana",
  replace(replace(replace(printf('%,.2f', ridge_ar), ',', '@'), '.', ','), '@', '.') as "Modelo (USD)",
  replace(replace(replace(printf('%,.2f', sazonal_ingenua_52s), ',', '@'), '.', ','), '@', '.') as "Referência sazonal (USD)"
from previsao order by previsao.semana
