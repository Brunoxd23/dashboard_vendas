import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas de Veículos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para formatar valores em reais sem depender do locale
def format_currency(value):
    return f"R$ {value:,.2f}"

# CSS personalizado
st.markdown("""
<style>
    /* === KPI Cards === */
    .card {
        padding: 15px;
        border-radius: 10px;
        margin: 5px;
        min-height: 100px;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
        width: 100%;
    }
    .card-title {
        font-size: 0.85em;
        color: rgba(255,255,255,0.8);
        margin-bottom: 8px;
        line-height: 1.2;
    }
    .card-value {
        font-size: 1.3em;
        font-weight: bold;
        color: white;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.2;
    }
    @media (max-width: 1200px) {
        .card-value { font-size: 1.1em; }
    }
    @media (max-width: 992px) {
        .card { padding: 10px; }
        .card-title { font-size: 0.8em; }
        .card-value { font-size: 1em; }
    }
    .card-blue { background: linear-gradient(135deg, #6B7FD7 0%, #8662DD 100%); }
    .card-green { background: linear-gradient(135deg, #4CAF50 0%, #45B649 100%); }
    .card-orange { background: linear-gradient(135deg, #FF8C42 0%, #F7A440 100%); }
    .card-red { background: linear-gradient(135deg, #FF6B6B 0%, #FF4949 100%); }

    /* === Sidebar Sections === */
    .sidebar-section {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 16px 14px 12px;
        margin-bottom: 12px;
    }
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .sidebar-header svg {
        flex-shrink: 0;
        opacity: 0.7;
    }
    .sidebar-header span {
        font-size: 0.78em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        opacity: 0.6;
    }
    /* === Filtros inline === */
    .filter-bar {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 14px 18px;
        margin: 10px 0 20px;
    }
    .filter-label {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.75em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.5;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Função para criar um card personalizado
def create_metric_card(title, value, color):
    value = str(value).strip()
    return f"""
    <div class="card card-{color}">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
    </div>
    """

# Colunas obrigatórias para o dashboard
COLUNAS_OBRIGATORIAS = ['data', 'produto', 'quantidade', 'preco_unitario']

# Função para carregar os dados do arquivo padrão
@st.cache_data
def load_default_data():
    try:
        df = pd.read_csv('arquivo_vendas.csv')
        df['faturamento'] = df['quantidade'] * df['preco_unitario']
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        return df
    except Exception:
        return pd.DataFrame()

# Função para processar o arquivo enviado pelo usuário
def load_uploaded_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Formato não suportado. Envie um arquivo CSV ou Excel (.xlsx/.xls).")
            return pd.DataFrame()

        # Normalizar nomes das colunas (minúsculo, sem espaços extras)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Verificar colunas obrigatórias
        colunas_faltando = [col for col in COLUNAS_OBRIGATORIAS if col not in df.columns]
        if colunas_faltando:
            st.error(
                f"⚠️ Colunas obrigatórias não encontradas: **{', '.join(colunas_faltando)}**\n\n"
                f"Seu arquivo precisa ter as colunas: `data`, `produto`, `quantidade`, `preco_unitario`"
            )
            return pd.DataFrame()

        # Converter tipos
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
        df['preco_unitario'] = pd.to_numeric(df['preco_unitario'], errors='coerce')
        df = df.dropna(subset=['quantidade', 'preco_unitario'])

        df['faturamento'] = df['quantidade'] * df['preco_unitario']

        # Tentar múltiplos formatos de data
        for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y']:
            try:
                df['data'] = pd.to_datetime(df['data'], format=fmt)
                break
            except (ValueError, TypeError):
                continue
        else:
            df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')

        df = df.dropna(subset=['data'])

        if df.empty:
            st.error("Nenhum dado válido encontrado após o processamento.")
            return pd.DataFrame()

        return df
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
        return pd.DataFrame()

# Título do Dashboard
st.title("📊 Dashboard de Vendas de Veículos")

# ═══ SIDEBAR ═══
# Ícones SVG (estilo Lucide/shadcn)
ICON_UPLOAD = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'
ICON_FILTER = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>'
ICON_CALENDAR = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
ICON_CAR = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9L18 10l-3-5H9L6 10l-2.5 1.1C2.7 11.3 2 12.1 2 13v3c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>'
ICON_DOWNLOAD = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'

# Seção: Upload
st.sidebar.markdown(f'<div class="sidebar-section"><div class="sidebar-header">{ICON_UPLOAD}<span>Fonte de Dados</span></div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader(
    "Envie sua planilha",
    type=['csv', 'xlsx', 'xls'],
    help="Colunas: data, produto, quantidade, preco_unitario",
    label_visibility="collapsed"
)

# Botão limpar dados
if st.sidebar.button("Limpar Dados", use_container_width=True, type="secondary"):
    st.cache_data.clear()
    st.session_state['dados_limpos'] = True
    st.toast("Dados limpos com sucesso!")
    time.sleep(0.5)
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Carregar dados
if st.session_state.get('dados_limpos', False):
    df = pd.DataFrame()
    if uploaded_file is None:
        st.session_state['dados_limpos'] = False
elif uploaded_file is not None:
    df = load_uploaded_data(uploaded_file)
    if not df.empty and st.session_state.get('ultimo_arquivo') != uploaded_file.name:
        st.session_state['ultimo_arquivo'] = uploaded_file.name
        # Barra de progresso com efeito
        progress_bar = st.sidebar.progress(0, text="Carregando dados...")
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1, text="Carregando dados...")
        progress_bar.empty()
        st.toast(f"{len(df)} registros carregados com sucesso!")
else:
    df = load_default_data()

# Seção: Exportar
if not df.empty:
    st.sidebar.markdown(f'<div class="sidebar-section"><div class="sidebar-header">{ICON_DOWNLOAD}<span>Exportar</span></div>', unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="vendas_veiculos.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Verificar se temos dados
if df.empty:
    st.info(
        "👋 **Bem-vindo ao Dashboard de Vendas!**\n\n"
        "Envie sua planilha na barra lateral para começar a análise.\n\n"
        "**Formato esperado das colunas:**\n"
        "- `data` — data da venda (ex: 01/01/2025)\n"
        "- `produto` — nome do produto/modelo\n"
        "- `quantidade` — quantidade vendida\n"
        "- `preco_unitario` — preço unitário"
    )
    st.stop()

# Container para KPIs (aparece primeiro visualmente)
kpi_container = st.container()

# Filtros abaixo dos KPIs
st.markdown(f'<div class="filter-bar"><div class="filter-label">{ICON_FILTER} Filtros</div></div>', unsafe_allow_html=True)

min_date = df['data'].min().date() if not df.empty else datetime.now().date()
max_date = df['data'].max().date() if not df.empty else datetime.now().date()

fcol1, fcol2, fcol3, fcol4 = st.columns([1, 1, 3, 1])
with fcol1:
    data_inicio = st.date_input("📅 De", min_date)
with fcol2:
    data_fim = st.date_input("📅 Até", max_date)
with fcol3:
    produtos_disponiveis = df['produto'].unique() if not df.empty else []
    modelos = st.multiselect(
        "🚗 Modelos",
        options=produtos_disponiveis,
        default=produtos_disponiveis
    )
with fcol4:
    total_selecionados = len(modelos)
    total_disponiveis = len(produtos_disponiveis)
    st.markdown(f"<br><span style='opacity:0.5; font-size:0.85em'>{total_selecionados}/{total_disponiveis} modelos</span>", unsafe_allow_html=True)

# Aplicar filtros ao DataFrame
if not df.empty and modelos:
    df_filtered = df[
        (df['data'].dt.date >= data_inicio) & 
        (df['data'].dt.date <= data_fim) & 
        (df['produto'].isin(modelos))
    ]
else:
    df_filtered = df.copy()

# Renderizar KPIs no container (acima dos filtros)
with kpi_container:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            create_metric_card(
                "Total de Vendas",
                f"{df_filtered['quantidade'].sum():,}",
                "blue"
            ),
            unsafe_allow_html=True
        )

    with col2:
        faturamento_total = format_currency(df_filtered['faturamento'].sum())
        faturamento_total = faturamento_total.replace(" ", "")
        st.markdown(
            create_metric_card(
                "Faturamento Total",
                faturamento_total,
                "green"
            ),
            unsafe_allow_html=True
        )

    with col3:
        ticket_medio = format_currency(df_filtered['faturamento'].mean())
        ticket_medio = ticket_medio.replace(" ", "")
        st.markdown(
            create_metric_card(
                "Ticket Médio",
                ticket_medio,
                "orange"
            ),
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            create_metric_card(
                "Total de Modelos",
                f"{df_filtered['produto'].nunique()}",
                "red"
            ),
            unsafe_allow_html=True
        )

# Criando duas colunas para os gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Evolução do Faturamento Diário")
    faturamento_diario = df_filtered.groupby('data')['faturamento'].sum().reset_index()
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
    faturamento_modelo = df_filtered.groupby('produto')['faturamento'].sum().reset_index()
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
faturamento_modelo = df_filtered.groupby('produto').agg({
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
        df_filtered.style.format({
            'preco_unitario': 'R$ {:,.2f}',
            'faturamento': 'R$ {:,.2f}'
        }),
        hide_index=True
    )

# Seo exportar removida daqui (já está na sidebar)

# Rodapé
st.markdown("---")
st.markdown("Dashboard desenvolvido com Streamlit - Análise de Vendas de Veículos")