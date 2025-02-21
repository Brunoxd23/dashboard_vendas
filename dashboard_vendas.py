import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import locale

# Configurando a localização para formato brasileiro de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas de Veículos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado atualizado para os cards
st.markdown("""
<style>
    .card {
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        height: 120px; /* Altura fixa para todos os cards */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .card-title {
        font-size: 0.9em;
        color: rgba(255,255,255,0.8);
        margin-bottom: 10px;
    }
    .card-value {
        font-size: 1.6em; /* Reduzido um pouco para caber melhor */
        font-weight: bold;
        color: white;
        white-space: nowrap; /* Evita quebra de linha */
    }
    .card-blue {
        background: linear-gradient(135deg, #6B7FD7 0%, #8662DD 100%);
    }
    .card-green {
        background: linear-gradient(135deg, #4CAF50 0%, #45B649 100%);
    }
    .card-orange {
        background: linear-gradient(135deg, #FF8C42 0%, #F7A440 100%);
    }
    .card-red {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4949 100%);
    }
</style>
""", unsafe_allow_html=True)

# Função para formatar valores em reais
def format_currency(value):
    return f"R$ {value:,.2f}"

# Função para criar um card personalizado
def create_metric_card(title, value, color):
    return f"""
    <div class="card card-{color}">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
    </div>
    """

# Função para carregar os dados
@st.cache_data
def load_data():
    # Carregando os dados brutos
    df = pd.read_csv('arquivo_vendas.csv')
    df['faturamento'] = df['quantidade'] * df['preco_unitario']
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    return df

# Carregando os dados
df = load_data()

# Título do Dashboard
st.title("📊 Dashboard de Vendas de Veículos")

# Layout dos cards em colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        create_metric_card(
            "Total de Vendas",
            f"{df['quantidade'].sum():,}",
            "blue"
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        create_metric_card(
            "Faturamento Total",
            format_currency(df['faturamento'].sum()).replace(" ", ""),  # Remove espaço entre R$ e valor
            "green"
        ),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        create_metric_card(
            "Ticket Médio",
            format_currency(df['faturamento'].mean()),
            "orange"  # Mudado de yellow para orange para melhor visibilidade
        ),
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        create_metric_card(
            "Total de Modelos",
            f"{df['produto'].nunique()}",
            "red"
        ),
        unsafe_allow_html=True
    )

# Criando duas colunas para os gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Evolução do Faturamento Diário")
    faturamento_diario = df.groupby('data')['faturamento'].sum().reset_index()
    fig_evolucao = px.line(
        faturamento_diario,
        x='data',
        y='faturamento',
        title="Faturamento ao Longo do Tempo",
    )
    fig_evolucao.update_layout(
        yaxis_title="Faturamento (R$)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_gridcolor='rgba(128,128,128,0.1)',
        xaxis_gridcolor='rgba(128,128,128,0.1)'
    )
    st.plotly_chart(fig_evolucao, use_container_width=True)

with col_right:
    st.subheader("Distribuição do Faturamento por Modelo")
    faturamento_modelo = df.groupby('produto')['faturamento'].sum().reset_index()
    fig_pizza = px.pie(
        faturamento_modelo,
        values='faturamento',
        names='produto',
        hole=0.6
    )
    fig_pizza.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

# Ranking de Faturamento por Modelo
st.subheader("Ranking de Faturamento por Modelo")
faturamento_modelo = df.groupby('produto').agg({
    'faturamento': 'sum',
    'quantidade': 'sum'
}).reset_index()

faturamento_modelo = faturamento_modelo.sort_values('faturamento', ascending=False)
fig_barras = px.bar(
    faturamento_modelo,
    x='produto',
    y='faturamento',
    text=faturamento_modelo['faturamento'].apply(lambda x: f'R$ {x:,.2f}'),
    title="Faturamento Total por Modelo"
)
fig_barras.update_traces(textposition='outside')
fig_barras.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    yaxis_gridcolor='rgba(128,128,128,0.1)',
    xaxis_gridcolor='rgba(128,128,128,0.1)'
)
st.plotly_chart(fig_barras, use_container_width=True)

# Tabelas detalhadas
st.subheader("Dados Detalhados")
tabs = st.tabs(["Resumo por Modelo", "Dados Brutos"])

with tabs[0]:
    st.dataframe(
        faturamento_modelo.style.format({
            'faturamento': 'R$ {:,.2f}',
            'quantidade': '{:,}'
        }),
        hide_index=True
    )

with tabs[1]:
    st.dataframe(
        df.style.format({
            'preco_unitario': 'R$ {:,.2f}',
            'faturamento': 'R$ {:,.2f}'
        }),
        hide_index=True
    )

# Filtros no Sidebar
st.sidebar.title("Filtros")
st.sidebar.subheader("Selecione o período")
data_inicio = st.sidebar.date_input("Data Inicial", df['data'].min())
data_fim = st.sidebar.date_input("Data Final", df['data'].max())

modelos = st.sidebar.multiselect(
    "Selecione os Modelos",
    options=df['produto'].unique(),
    default=df['produto'].unique()
)

# Download dos dados
st.sidebar.markdown("---")
st.sidebar.subheader("Exportar Dados")

# Botão para download CSV
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="vendas_veiculos.csv",
    mime="text/csv"
)

# Rodapé
st.markdown("---")
st.markdown("Dashboard desenvolvido com Streamlit - Análise de Vendas de Veículos")