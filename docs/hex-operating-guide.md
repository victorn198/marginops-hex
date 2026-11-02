# Práticas de trabalho verificadas no Hex

Pesquisa e verificação da interface: 02/11/2026. Workspace autenticado pelo usuário; plano Community, Small com 4 GB, sem método de pagamento. A assinatura foi apenas consultada.

## Recursos escolhidos

- Notebook reativo: declarar caminhos, fontes e parâmetros explicitamente para preservar as dependências entre células.
- SQL com fonte Dataframes/DuckDB para consultas sobre Parquet e resultados anteriores; Python para estatística e cálculos que exigem etapas próprias.
- Entradas nativas, Single Values, gráficos, tabelas e pivôs; App Builder com abas e composição de saídas selecionadas.
- Dados grandes ficam em Parquet. Colunas e períodos são limitados, agregando cedo. Inputs de cenário são colocados depois da aquisição e das consultas estáveis.
- Nenhum cache de warehouse é prometido para SQL sobre dataframe: são caminhos de execução diferentes.
- O agente nativo ajuda a criar células e layout; seus resultados são revisados contra verificações executadas separadamente.
- Regras monetárias, granularidade, denominadores, maturidade de coortes, datas incompletas e hipóteses do simulador ficam documentadas.

## Recursos condicionados ao plano

MCP e CLI oficiais estão documentados para Team/Enterprise. O CLI não tem suporte nativo ao Windows. Não foi alterada a assinatura nem criado token. Publicação, compartilhamento público e incorporação precisam ser conferidos na interface real; publicar uma versão não concede acesso por si só. Temas personalizados, agendamento, Tasks e integrações administrativas não serão tratados como disponíveis no Community.

## Publicação e continuidade

Foi verificada na interface a opção `Anyone with the link` do compartilhamento deste projeto, ainda sem selecioná-la durante a construção. O trabalho ocorre no projeto nativo de notebook/Classic App para preservar células, parâmetros, indicadores, pivôs e layout auditável. A documentação atual também oferece Generative Apps e Hex 4.0, com interfaces geradas em código; essa alternativa não substitui a validação dos cálculos. Context Studio e Evals são documentados para Team/Enterprise e não foram ativados no Community.

1. Confirmar as alterações desejadas do agente e retirar células temporárias.
2. Reiniciar o kernel e executar tudo, conferindo resultados e memória.
3. Testar combinações de filtros e cenários e conferir os componentes apresentados.
4. Exportar o formato nativo `.hex.yaml`, validando contra o schema oficial, pois preserva entradas, células SQL e layout melhor que `.ipynb`.
5. Conferir o preview de publicação antes de publicar; então configurar o acesso web permitido e testar o link público.
6. Atualizar o portfólio com o link real e a descrição exata do que funciona.

## Fontes oficiais

- https://learn.hex.tech/docs/getting-started/develop-your-notebook
- https://learn.hex.tech/docs/explore-data/projects/project-execution/execution-model
- https://learn.hex.tech/tutorials/develop-notebooks/project-execution-guide
- https://learn.hex.tech/tutorials/develop-notebooks/memory-management-in-hex
- https://learn.hex.tech/docs/explore-data/cells/sql-cells/sql-cells-introduction
- https://learn.hex.tech/docs/explore-data/cells/sql-cells/query-caching
- https://learn.hex.tech/docs/explore-data/cells/input-cells/input-cells-introduction
- https://learn.hex.tech/docs/share-insights/apps/app-builder
- https://learn.hex.tech/docs/share-insights/apps/publish-and-share-apps
- https://learn.hex.tech/docs/collaborate/sharing-and-permissions/project-sharing
- https://learn.hex.tech/docs/explore-data/projects/import-export
- https://static.hex.site/hex-file-schema.json
- https://learn.hex.tech/tutorials/ai-best-practices/notebook-agent-best-practices
- https://learn.hex.tech/docs/api-integrations/mcp-server
- https://learn.hex.tech/docs/api-integrations/cli
- https://hex.tech/pricing/
- https://learn.hex.tech/docs/share-insights/apps/generative-apps
- https://learn.hex.tech/docs/hex-4-0/what-is-hex-4-0
- https://learn.hex.tech/docs/agent-management/context-studio
- https://learn.hex.tech/docs/agent-management/evals
- https://learn.hex.tech/docs/agent-management/governed-mode
