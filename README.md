# MarginOps — Inteligência Comercial e Rentabilidade no Hex

Projeto empresarial de portfólio por Victor Nogueira, desenvolvido para SQL, Python e aplicativos nativos do Hex.

## Decisão de negócio

Como priorizar mercados, categorias, produtos e clientes para crescer com margem? Como preço, volume e mix explicam a variação da receita? Quanto de volume adicional seria necessário para compensar descontos e inflação de custos?

## Base empresarial

O projeto usa a base **Contoso, da SQLBI**, uma empresa fictícia destinada a demonstração e treinamento. O arquivo publicado na escala nominal de um milhão contém **980.666 pedidos e 2.349.091 itens vendidos**, distribuídos por oito tabelas relacionadas: vendas, pedidos, itens de pedidos, clientes, produtos, lojas, calendário e câmbio. Período observado: 18/05/2016 a 31/12/2025.

Não representa resultados de uma empresa real. As análises são calculadas sobre as linhas do dataset, e hipóteses do simulador são identificadas separadamente. A licença MIT original é preservada em `DATA_LICENSE`.

## Escopo analítico

- Visão executiva com comparação de anos completos, receita, descontos, custo dos produtos e margem bruta ponderada.
- Decomposição aritmética da variação da receita por preço, volume e mix.
- Prioridades comerciais por categoria, produto, mercado e canal.
- Coortes de clientes com maturidade explícita e contexto de aquisição.
- Previsão semanal com validação temporal e comparação contra referência sazonal.
- Simulador de desconto adicional, aumento de custo e volume necessário para preservar a margem.
- Reconciliação entre vendas e pedidos/itens, unicidade de chaves, integridade dos relacionamentos e conferência monetária.
- Dicionário das métricas, origem, limites e regras de conversão de moeda.

A base não contém posição de estoque, contas a pagar/receber ou despesas operacionais; por isso, os resultados comerciais não serão apresentados como lucro líquido ou fluxo de caixa.

## Uso no Hex

O aplicativo usa células de SQL, Python, entradas, indicadores, gráficos, tabelas e abas. O arquivo `.hex.yaml` será validado contra o esquema público oficial. O funcionamento em nuvem e o compartilhamento público serão verificados antes de apresentar o projeto como publicado.

Os dados de publicação estão em `data/published/`. As tabelas são lidas de forma seletiva, sem materializar milhões de linhas desnecessariamente em dataframes. A projeção de clientes elimina nomes, endereços e outros atributos sem uso analítico.

## Fontes

- [Documentação SQLBI](https://docs.sqlbi.com/contoso-data-generator/)
- [Dataset original](https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/tag/ready-to-use-data)
- [Gerador e regras dos valores](https://github.com/sql-bi/Contoso-Data-Generator-V2/blob/main/DatabaseGenerator/Engine.cs)
- [Formato nativo e importação do Hex](https://learn.hex.tech/docs/explore-data/projects/import-export)
