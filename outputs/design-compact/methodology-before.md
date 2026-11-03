## Qualidade e metodologia
**Fonte.** SQLBI *Contoso Data Generator V2* — conjunto "Contoso 1M" 
([release](https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/
releases/tag/ready-to-use-data), licença MIT), convertido em 8 arquivos 
Parquet no snapshot [victorn198/marginops-hex @ eb9985f](https://github.
com/victorn198/marginops-hex/tree/eb9985f/data/published) ([manifest.
json](https://raw.githubusercontent.com/victorn198/marginops-hex/
eb9985f/data/published/manifest.json)). Período: **18/05/2016 a 31/12/
2025**; 2.349.091 linhas de venda, 980.666 pedidos. **Empresa e 
clientes são fictícios**; os dados de cliente foram projetados para 
chaves, datas SCD e campos geográficos. Este projeto não representa 
trabalho para cliente, dados de produção nem impacto de negócio 
realizado.
**Status das verificações:** {{ qa_status }}
**Moeda.** O gerador ([Engine.cs](https://github.com/sql-bi/
Contoso-Data-Generator-V2/blob/main/DatabaseGenerator/Engine.cs), 
*BuildSaleItems*) constrói UnitPrice, NetPrice e UnitCost a partir dos 
preços-base do produto **sem** aplicar ExchangeRate. Por isso todos os 
valores consolidados ficam em **USD** e não são divididos pela taxa; a 
tabela de moedas confirma razão = 1 entre preço/custo transacionado e 
cadastro nas 5 moedas. ExchangeRate (USD → moeda do pedido) não é usado 
nos consolidados.
**Grão e reconciliação.** Grão principal: `OrderKey + LineNumber` em 
*sales*. *orders + orderrows* (grão `OrderKey + RowNumber`) é uma 
representação equivalente: foi reconciliada linha a linha e em valores, 
e **não** é somada a *sales*. Todos os joins são muitos-para-um, sem 
órfãos e sem perda/duplicação de linhas; nenhuma linha foi excluída.
**Dicionário de métricas.**
| Métrica | Definição |
|---|---|
| Receita bruta | Σ Quantity × UnitPrice |
| Receita líquida | Σ Quantity × NetPrice |
| Descontos | Receita bruta − receita líquida |
| CPV | Σ Quantity × UnitCost (custo histórico da transação, não o 
custo atual do cadastro) |
| Lucro bruto | Receita líquida − CPV (não é EBITDA nem lucro líquido) |
| Margem bruta | Lucro bruto ÷ receita líquida (razão de somas, nunca 
média de margens por linha) |
| Pedidos | COUNT(DISTINCT OrderKey) no escopo filtrado ativo |
| Canal | *Online* = StoreKey 999999 ("Online store" no cadastro de 
lojas); demais = loja física |
| Mercado | País do cliente (CountryFull) |
| Dias de entrega | DeliveryDate − OrderDate, duração observada (0 a 21 
dias); não há SLA prometido |
**Limitações.** Não há saldos de estoque, contas a receber/pagar, 
despesas operacionais fixas nem SLA de entrega: o projeto não calcula 
lucro líquido, fluxo de caixa ou atrasos. Comparações ano a ano usam 
anos completos (o escopo permite 2023–2025). Coorte 2016 censurada à 
esquerda. Previsão e simulador são exercícios analíticos, não 
recomendações garantidas.