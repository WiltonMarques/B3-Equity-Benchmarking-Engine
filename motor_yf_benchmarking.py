import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

# Configuração da Página
st.set_page_config(page_title="EquityLens | Benchmarking", layout="wide")

st.title("📊 EquityLens: Motor de Benchmarking B3")
st.markdown("Análise comparativa fundamentalista por segmento (Dados reais via Yahoo Finance).")
st.markdown("---")

# ==========================================
# 1. MAPEAMENTO DE SETORES E TICKERS (B3)
# ==========================================
SETORES_B3 = {
    "Locadoras de Veículos": ["RENT3.SA", "MOVI3.SA"],
    "Varejo Farmacêutico": ["RADL3.SA", "PNVL3.SA", "PGMN3.SA"],
    "Frigoríficos e Proteína": ["JBSS3.SA", "MRFG3.SA", "BEEF3.SA", "BRFS3.SA"],
    "Siderurgia e Mineração": ["VALE3.SA", "CSNA3.SA", "GGBR4.SA", "USIM5.SA"],
    "Varejo de Calçados e Roupas": ["ALOS3.SA", "ARZZ3.SA", "CEAB3.SA", "LREN3.SA", "SOMA3.SA"],
    "Energia Elétrica (Geração/Transmissão)": ["ELET3.SA", "EGIE3.SA", "TAEE11.SA", "TRPL4.SA"]
}

# ==========================================
# 2. INGESTÃO DE DADOS (Barra Lateral)
# ==========================================
st.sidebar.header("🔌 Filtro de Ativos")
st.sidebar.markdown("Selecione o segmento para garantir a comparabilidade (Pares).")

# Caixas de Listagem (Dropdowns) dinâmicas
segmento_escolhido = st.sidebar.selectbox("1. Escolha o Segmento:", list(SETORES_B3.keys()))
tickers_disponiveis = SETORES_B3[segmento_escolhido]

ticker_a = st.sidebar.selectbox("2. Empresa A:", tickers_disponiveis, index=0)
# Garante que a Empresa B padrão seja diferente da Empresa A (se houver mais de uma opção)
index_b = 1 if len(tickers_disponiveis) > 1 else 0
ticker_b = st.sidebar.selectbox("3. Empresa B:", tickers_disponiveis, index=index_b)

if ticker_a == ticker_b:
    st.sidebar.warning("⚠️ Você selecionou a mesma empresa. Escolha empresas diferentes para o benchmarking.")

# ==========================================
# 3. FUNÇÕES DE EXTRAÇÃO E CÁLCULO
# ==========================================
def safe_get(df, row_name, default=0.0):
    try:
        val = df.loc[row_name].iloc[0]
        return float(val) if not pd.isna(val) else default
    except (KeyError, IndexError, AttributeError):
        return default

@st.cache_data(ttl=3600)
def extrair_dados_yfinance(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    dre = ticker.financials
    bp = ticker.balance_sheet
    dfc = ticker.cashflow
    
    if dre.empty or bp.empty or dfc.empty:
        return None

    receita_liquida = safe_get(dre, "Total Revenue")
    custos = abs(safe_get(dre, "Cost Of Revenue"))
    
    lucro_operacional = safe_get(dre, "Operating Income")
    if lucro_operacional == 0:
        lucro_operacional = safe_get(dre, "EBIT")
        
    despesas_op = (receita_liquida - custos) - lucro_operacional
    
    depreciacao = safe_get(dfc, "Depreciation And Amortization")
    if depreciacao == 0:
        depreciacao = safe_get(dre, "Reconciled Depreciation")
        
    resultado_financeiro = abs(safe_get(dre, "Net Non Operating Interest Income Expense"))
    ir = abs(safe_get(dre, "Tax Provision"))
    
    fco = safe_get(dfc, "Operating Cash Flow")
    capex = abs(safe_get(dfc, "Capital Expenditure"))
    
    patrimonio_liquido = safe_get(bp, "Stockholders Equity")
    ativo_total = safe_get(bp, "Total Assets")
    
    divida_total = safe_get(bp, "Total Debt")
    capital_investido = patrimonio_liquido + divida_total
    
    return {
        "Receita_Liquida": receita_liquida, "Custos": custos, "Despesas_Operacionais": despesas_op,
        "Depreciacao": depreciacao, "Resultado_Financeiro": resultado_financeiro, "IR": ir,
        "FCO": fco, "Capex": capex, "Patrimonio_Liquido": patrimonio_liquido,
        "Capital_Investido": capital_investido, "Ativo_Total": ativo_total
    }

def calcular_kpis(dados_dict):
    kpis = {}
    for nome, d in dados_dict.items():
        if d is None:
            continue
            
        lucro_bruto = d["Receita_Liquida"] - d["Custos"]
        lucro_operacional = lucro_bruto - d["Despesas_Operacionais"]
        ebitda = lucro_operacional + d["Depreciacao"]
        lucro_liquido = lucro_operacional - d["Resultado_Financeiro"] - d["IR"]
        nopat = lucro_operacional - d["IR"]

        kpis[nome] = {
            "Margem Bruta (%)": (lucro_bruto / d["Receita_Liquida"] * 100) if d["Receita_Liquida"] else 0,
            "Margem Operacional (%)": (lucro_operacional / d["Receita_Liquida"] * 100) if d["Receita_Liquida"] else 0,
            "Margem EBITDA (%)": (ebitda / d["Receita_Liquida"] * 100) if d["Receita_Liquida"] else 0,
            "Margem Líquida (%)": (lucro_liquido / d["Receita_Liquida"] * 100) if d["Receita_Liquida"] else 0,
            "Margem FCO (%)": (d["FCO"] / d["Receita_Liquida"] * 100) if d["Receita_Liquida"] else 0,
            "Conversão FCO (%)": (d["FCO"] / ebitda * 100) if ebitda else 0,
            "Margem FCL (%)": ((d["FCO"] - d["Capex"]) / d["Receita_Liquida"] * 100) if d["Receita_Liquida"] else 0,
            "ROE (%)": (lucro_liquido / d["Patrimonio_Liquido"] * 100) if d["Patrimonio_Liquido"] else 0,
            "ROIC (%)": (nopat / d["Capital_Investido"] * 100) if d["Capital_Investido"] else 0,
            "ROA (%)": (lucro_liquido / d["Ativo_Total"] * 100) if d["Ativo_Total"] else 0
        }
    return pd.DataFrame(kpis)

# ==========================================
# 4. RENDERIZAÇÃO DO DASHBOARD
# ==========================================
if st.sidebar.button("Executar Valuation Real", type="primary"):
    if ticker_a == ticker_b:
        st.error("Selecione duas empresas diferentes para realizar a comparação.")
    else:
        with st.spinner(f"Baixando demonstrações financeiras de {ticker_a} e {ticker_b}..."):
            
            dados_reais = {
                f"Empresa A ({ticker_a})": extrair_dados_yfinance(ticker_a),
                f"Empresa B ({ticker_b})": extrair_dados_yfinance(ticker_b)
            }
            
            if None in dados_reais.values():
                st.error("Erro ao buscar dados na API. Verifique a conexão ou a disponibilidade dos Tickers.")
            else:
                df_resultados = calcular_kpis(dados_reais)
                
                st.subheader("🏆 Painel Comparativo (Vencedor em Destaque)")

                def colorir_vencedor(row):
                    styles = [''] * len(row)
                    if row.name in df_resultados.index:
                        vencedor_idx = row.argmax()
                        styles[vencedor_idx] = 'background-color: #d4edda; color: #155724; font-weight: bold;'
                    return styles

                st.dataframe(
                    df_resultados.style.apply(colorir_vencedor, axis=1).format("{:.2f}%"),
                    use_container_width=True,
                    height=380
                )

                st.markdown("---")
                st.subheader("📈 Análise Visual por Bloco de Eficiência")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 🛒 Bloco de Margens (Eficiência Operacional)")
                    margens = ['Margem Bruta (%)', 'Margem Operacional (%)', 'Margem EBITDA (%)', 'Margem Líquida (%)']
                    fig_margens = go.Figure(data=[
                        go.Bar(name=f"A: {ticker_a}", x=margens, y=df_resultados.loc[margens, f"Empresa A ({ticker_a})"], marker_color='#1f77b4'),
                        go.Bar(name=f"B: {ticker_b}", x=margens, y=df_resultados.loc[margens, f"Empresa B ({ticker_b})"], marker_color='#ff7f0e')
                    ])
                    fig_margens.update_layout(barmode='group', template='plotly_white', margin=dict(t=30, b=0))
                    st.plotly_chart(fig_margens, use_container_width=True)

                with col2:
                    st.markdown("#### 💰 Bloco de Retorno (Alocação de Capital)")
                    retornos = ['ROE (%)', 'ROIC (%)', 'ROA (%)']
                    fig_retornos = go.Figure(data=[
                        go.Bar(name=f"A: {ticker_a}", x=retornos, y=df_resultados.loc[retornos, f"Empresa A ({ticker_a})"], marker_color='#1f77b4'),
                        go.Bar(name=f"B: {ticker_b}", x=retornos, y=df_resultados.loc[retornos, f"Empresa B ({ticker_b})"], marker_color='#ff7f0e')
                    ])
                    fig_retornos.update_layout(barmode='group', template='plotly_white', margin=dict(t=30, b=0))
                    st.plotly_chart(fig_retornos, use_container_width=True)