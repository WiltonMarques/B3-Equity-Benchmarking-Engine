# 📊 EquityLens: Motor de Benchmarking B3 (IFRS/CPC)

O **EquityLens** é uma aplicação *SaaS* (Software as a Service) desenvolvida em Python para análise fundamentalista automatizada e *benchmarking* relativo de empresas listadas na B3.

Construído sob a ótica de *Equity Research* institucional, o sistema realiza a extração em tempo real de demonstrações financeiras (DRE, Balanço Patrimonial e DFC), padroniza as rubricas contábeis (conversão US GAAP para IFRS/CPC) e calcula dinamicamente 10 Indicadores-Chave de Performance (KPIs) focados em rentabilidade, eficiência operacional e geração de caixa.

## 🚀 Arquitetura e Funcionalidades

* **Ingestão de Dados em Tempo Real:** Integração via API (`yfinance`) para raspar as demonstrações financeiras mais recentes divulgadas no mercado.
* **Segmentação Inteligente de Pares:** Funil de seleção automatizado que força a comparação entre ativos do mesmo setor de atuação, garantindo aderência analítica (ex: comparar frigorífico apenas com frigorífico).
* **Tratamento e Engenharia de Dados Contábeis:**
    * Cálculo de lucros intermediários (Lucro Bruto, EBIT, EBITDA, NOPAT).
    * Cálculo de Capital Investido (Patrimônio Líquido + Dívida Total).
* **Motor de KPIs (Análise DuPont Expandida):**
    * *Margens Operacionais:* Bruta, EBIT, EBITDA, Líquida.
    * *Qualidade de Caixa:* Margem FCO, Conversão FCO e Margem de Fluxo de Caixa Livre (FCL).
    * *Alocação de Capital:* ROE (Return on Equity), ROIC (Return on Invested Capital) e ROA (Return on Assets).
* **Dashboard Executivo (UI/UX):** Interface interativa desenvolvida com `Streamlit` e `Plotly`, destacando automaticamente a empresa vencedora por meio de formatação condicional e gráficos de barras.

## 🛠️ Stack Tecnológico

* **Linguagem:** Python
* **Data Extraction:** `yfinance`
* **Data Manipulation:** `pandas`, `numpy`
* **Data Visualization & Interface:** `streamlit`, `plotly`

## ⚖️ Aviso Legal e Compliance (Disclaimer)

**Este projeto possui finalidade estritamente didática e de demonstração de arquitetura de dados financeiros.** O *EquityLens* é um ensaio quantitativo baseado nos fundamentos de Análise Fundamentalista. As informações, cálculos e sínteses geradas automaticamente por este sistema **NÃO constituem e não devem ser interpretadas como recomendação de compra, venda, manutenção de ativos financeiros, relatório de análise (Resolução CVM nº 20) ou aconselhamento profissional.**

Dados extraídos de APIs públicas podem conter atrasos, omissões ou inconsistências estruturais em relação aos balanços oficiais auditados (DFP/ITR) entregues à Comissão de Valores Mobiliários (CVM). O desenvolvedor exime-se de qualquer responsabilidade por eventuais decisões de investimento tomadas com base nas informações fornecidas por esta ferramenta.
