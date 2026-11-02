# Caso empresarial — crescer preservando margem

Esta é uma análise de uma empresa **fictícia**, Contoso/SQLBI. Os valores abaixo vêm de cálculos sobre o snapshot publicado, não de um cliente real nem de uma intervenção implementada.

## Decisão

Uma diretoria comercial quer entender por que a receita diminuiu, quais componentes explicam a mudança e quanto volume adicional uma promoção precisaria gerar para preservar o lucro bruto. O projeto reúne vendas, pedidos, clientes, produtos, lojas, calendário e câmbio, com granularidade de item do pedido.

## O que a apuração independente encontrou

| Indicador, USD nominais | 2024 | 2025 |
| --- | ---: | ---: |
| Receita líquida de descontos comerciais | 325.037.485,20 | 299.946.187,10 |
| Custo dos produtos vendidos | 143.349.791,62 | 131.862.649,08 |
| Lucro bruto | 181.687.693,58 | 168.083.538,02 |
| Margem bruta ponderada | 55,8975% | 56,0379% |
| Pedidos distintos | 163.695 | 161.802 |

Receita e lucro bruto caíram, enquanto a margem percentual subiu ligeiramente. Avaliar apenas o percentual de margem deixaria de mostrar a redução do resultado absoluto.

A receita diminuiu **US$ 25.091.298,10**. Uma decomposição simétrica de Shapley, com as seis ordens possíveis de alteração dos fatores, atribui aritmeticamente a diferença a:

| Componente | Variação de receita, USD |
| --- | ---: |
| Volume total de unidades | -3.433.776,77 |
| Mix de unidades entre produtos | -21.779.029,80 |
| Preço líquido médio por produto | +121.508,48 |

A soma fecha com a mudança observada. Atribuição aritmética não demonstra uma causa comportamental: a investigação comercial seguinte deve examinar as categorias e produtos que mudaram de participação e testar hipóteses de demanda.

## Teste de uma proposta de promoção

Partindo do conjunto completo de 2025, um desconto **adicional de 5%**, inflação de custo unitário de **10%** e aumento **assumido** de volume de **15%** produziria, sob essas hipóteses uniformes:

- Receita de US$ 327.691.209,41;
- Custo dos produtos de US$ 166.806.251,09;
- Lucro bruto de US$ 160.884.958,32;
- Redução de lucro bruto de US$ 7.198.579,70 em relação à base.

O volume necessário para preservar o lucro bruto seria **20,1455% maior**. Esse é um ponto de equilíbrio matemático, não uma previsão de resposta do cliente. O simulador permite variar essas premissas e verificar o resultado.

Fórmula: `lucro_cenário = (1 + aumento_volume) × [receita_base × (1 - desconto_adicional) - custo_base × (1 + inflação_custo)]`.

## Validação de previsão

A referência independente compara uma autoregressão ridge de parâmetros fixos com uma referência sazonal de 52 semanas. Foram usadas seis origens temporais e quatro semanas futuras por origem, com treino, normalização e variáveis defasadas calculados sem utilizar observações futuras. Semanas parciais nas bordas foram removidas.

Nesse teste, a referência sazonal teve WAPE de **4,4446%** e MAE de **US$ 264.526,51**, frente a WAPE de **8,6830%** e MAE de **US$ 516.785,45** da ridge. O resultado favorece a referência sazonal nesse recorte. A implementação do aplicativo também deve mostrar a comparação observada, permitindo que a referência vença. A série é sintética e o teste não garante acurácia em uma operação real.

## Cuidados que mudam os resultados

- As colunas de preço e custo permanecem na moeda-base USD no gerador. Aplicar uma segunda conversão por causa de `CurrencyCode` distorceria a apuração.
- Custo de venda é `UnitCost` da transação, preservando a informação histórica. O custo atual no cadastro do produto não substitui esse valor.
- Pedidos distintos não podem ser somados indiscriminadamente entre categorias, pois um mesmo pedido pode conter várias categorias.
- `sales` e `orders + orderrows` são duas representações dos mesmos eventos; a reconciliação é útil, a concatenação duplicaria os resultados.
- Cadastros possuem versões históricas. Os relacionamentos usam chaves substitutas únicas, e coortes por `CustomerKey` não garantem deduplicação da pessoa entre versões sem uma chave natural persistente.
- Margem bruta é a razão entre somas de lucro e receita. A média das margens das linhas seria uma medida diferente.
- A fonte não traz OPEX, saldo de estoque ou contas a receber/pagar. O projeto não interpreta lucro bruto como lucro líquido ou fluxo de caixa.

## Reprodutibilidade

O manifesto em `data/published/manifest.json` registra arquivos, hashes SHA256, contagens e período. `tools/verify_source.py` reconcilia as representações e confere um mês com aritmética Decimal independente. `tools/verify_decisions.py` registra os testes da decomposição, do cenário e da validação temporal. Os resultados completos estão em `outputs/verification/`.

Fontes: [SQLBI Contoso](https://docs.sqlbi.com/contoso-data-generator/), [gerador de preços e custos](https://github.com/sql-bi/Contoso-Data-Generator-V2/blob/main/DatabaseGenerator/Engine.cs), [snapshot utilizado](https://github.com/victorn198/marginops-hex/tree/eb9985f/data/published).


## Aplicativo entregue

O aplicativo está [publicado no Hex](https://app.hex.tech/019fb7c2-0139-75db-a781-a6d19adf4a2e/app/034qivrUc5i5OGHBvR7b6o/latest). Filtros e cenários são aplicados pelo botão **Run**. A execução conjunta foi escolhida após o teste de alterações rápidas no modo automático revelar resultados antigos temporariamente misturados a novos.

O teste publicado de 2024, todos os mercados/categorias, concluiu com WAPE ridge de 24,5703% e referência sazonal de 42,1914%, consistentes entre indicadores, tabela e narrativa. Isso também demonstra que a comparação não força a mesma técnica a vencer em todos os recortes.

Os controles são nativos do Hex. SQL e Python ficam no notebook; o aplicativo apresenta resultados e métodos sem expor os códigos de cada célula. O repositório guarda a preparação e as verificações independentes; a exportação nativa YAML ainda não foi recuperada nesta sessão.
