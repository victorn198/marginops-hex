# MarginOps — Inteligência Comercial e Rentabilidade no Hex

Projeto empresarial de portfólio por Victor Nogueira, desenvolvido com SQL, Python e células nativas do Hex.

**[Abrir aplicativo publicado no Hex](https://app.hex.tech/019fb7c2-0139-75db-a781-a6d19adf4a2e/app/034qivrUc5i5OGHBvR7b6o/latest)** · [Caso de negócio e resultados](docs/business-case-study.md)

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
- Simulador de desconto adicional, aumento de custo e volume necessário para preservar o lucro bruto.
- Reconciliação entre vendas e pedidos/itens, unicidade de chaves, integridade dos relacionamentos e conferência monetária.
- Dicionário das métricas, origem, limites e regras de conversão de moeda.

A base não contém posição de estoque, contas a pagar/receber ou despesas operacionais; por isso, os resultados comerciais não serão apresentados como lucro líquido ou fluxo de caixa.

## Uso no Hex

O aplicativo publicado usa seis abas, células de SQL, Python, entradas, indicadores, gráficos nativos, pivot e gráficos Plotly. Escolha os filtros ou as premissas e clique em **Run** para recalcular o conjunto; aguarde a conclusão antes de interpretar os resultados. A atualização explícita evita execuções sobrepostas ao alterar vários campos.

O código e o layout nativos estão no projeto Hex. Este repositório contém o snapshot, a preparação, os cálculos independentes, os relatórios de verificação e a documentação. O download do export nativo YAML não foi recuperado nesta sessão e, portanto, esse export não foi validado nem está incluído aqui.

Os dados de publicação estão em `data/published/`. As tabelas são lidas de forma seletiva, sem materializar milhões de linhas desnecessariamente em dataframes. A projeção de clientes elimina nomes, endereços e outros atributos sem uso analítico.

## Fontes

- [Documentação SQLBI](https://docs.sqlbi.com/contoso-data-generator/)
- [Dataset original](https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/tag/ready-to-use-data)
- [Gerador e regras dos valores](https://github.com/sql-bi/Contoso-Data-Generator-V2/blob/main/DatabaseGenerator/Engine.cs)
- [Formato nativo e importação do Hex](https://learn.hex.tech/docs/explore-data/projects/import-export)

## Apresentação visual

A revisão visual usa cabeçalhos em azul profundo, indicadores comparativos com o ano anterior, cartões responsivos e estilos de gráficos coerentes entre abas. As tabelas terminais de previsão e validação usam nomes de negócio e valores arredondados somente na apresentação; os dataframes analíticos mantêm sua precisão.

As referências e os componentes de apresentação estão em `design/`. Esses arquivos representam as células alteradas nesta revisão, não um export completo do projeto Hex. O layout, os filtros, o pivot, as tabelas, o botão Run e a publicação continuam nativos. Nenhum tema pago foi ativado.

## Layout compacto (03/11/2026)

As seis abas foram reorganizadas para priorizar a leitura em tela de notebook. A visão executiva apresenta os filtros antes de cinco indicadores pequenos, série mensal e variações por categoria e mercado lado a lado. Os gráficos principais têm 230–300 px de altura, com hover, zoom e legenda interativa. Os componentes são saídas Python/HTML do próprio Hex, ligadas aos dataframes e figuras existentes.

As explicações e verificações podem ser expandidas. O pivot, as tabelas de produtos e recompra e a auditoria de arquivos permanecem nativos como detalhe; essas áreas podem exigir rolagem. Os controles de filtro, sliders e Run continuam nativos. `design/compact/` contém apenas a composição da apresentação; os cálculos analíticos não foram substituídos.
