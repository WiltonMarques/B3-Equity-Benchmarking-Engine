# B3-Equity-Benchmarking-Engine
EquityLens: B3 Benchmarking Engine - Motor quantitativo de Equity Research para a B3. Realiza extração via API, padronização contábil (IFRS/CPC) e benchmarking automatizado de KPIs fundamentalistas.

## 📖 Sobre o Projeto (Description)

O **EquityLens** é uma aplicação *SaaS* de análise fundamentalista e *benchmarking* relativo, construída para simular o rigor de uma mesa de *Equity Research* institucional. 

O sistema resolve um dos maiores gargalos da análise quantitativa de ações: a padronização de dados. Ele consome demonstrações financeiras brutas em tempo real da B3 (via Yahoo Finance), realiza o mapeamento "De/Para" de rubricas internacionais (US GAAP) para o padrão brasileiro (IFRS/CPC) e processa os dados em um motor matemático automatizado.

O objetivo principal é mitigar vieses de análise ao forçar a comparação exclusiva entre "pares" (empresas do mesmo segmento), gerando um painel interativo com 10 Indicadores-Chave de Performance (KPIs) divididos em três pilares:
1. **Eficiência Operacional** (Margens de Lucratividade)
2. **Geração e Qualidade de Caixa** (Métricas de FCO e FCL)
3. **Eficiência na Alocação de Capital** (ROE, ROA e ROIC)
