# Análise de Vendas de Veículos

Este projeto consiste em dois scripts Python que geram e analisam dados de vendas de veículos.

## Estrutura do Projeto

- `arquivo_vendas.py`: Gera dados simulados de vendas
- `analise_vendas.py`: Analisa os dados e gera relatórios
- `dashboard_vendas.py`: Dashboard interativo com upload, filtros e gráficos
- `arquivo_vendas.csv`: Arquivo gerado com os dados de vendas
- `relatorio_vendas.xlsx`: Relatório final com análises

## Descrição dos Scripts

### arquivo_vendas.py

Este script gera dados simulados de vendas de veículos com as seguintes características:

- Gera vendas aleatórias para os últimos 30 dias
- Inclui 8 modelos diferentes de carros
- Cada dia tem entre 3 a 8 vendas
- Preços variam ±5% do valor base
- Quantidade vendida varia de 1 a 3 unidades por venda

Colunas geradas:

- data: Data da venda (dd/mm/yyyy)
- produto: Modelo do veículo
- quantidade: Quantidade vendida
- preco_unitario: Preço unitário do veículo

### analise_vendas.py

Este script analisa os dados e gera um relatório Excel com três abas:

1. **Resumo**:
   - Faturamento total por produto
   - Produto com maior faturamento
   - Produto com menor faturamento

2. **Faturamento por Produto**:
   - Lista detalhada do faturamento por produto
   - Ordenado do maior para o menor faturamento

3. **Dados Brutos**:
   - Todos os dados originais das vendas

## Como Usar

1. Primeiro, crie um ambiente virtual e ative-o:

2. # Windows
   py -m venv venv
   venv\Scripts\activate

# Linux/Mac

python -m venv venv
source venv/bin/activate

Instale as dependências necessárias:

pip install pandas openpyxl

2. Execute os scripts na seguinte ordem:

python arquivo_vendas.py
python analise_vendas.py

3. Verifique os arquivos gerados:
   - `arquivo_vendas.csv`: Contém os dados brutos
   - `relatorio_vendas.xlsx`: Contém as análises formatadas

## Resultados

O relatório final (`relatorio_vendas.xlsx`) apresenta:

- Visão geral do faturamento por produto
- Identificação do produto mais vendido
- Identificação do produto menos vendido
- Valores formatados em reais (R$)
- Layout profissional com formatação adequada

## Requisitos

- Python 3.x
- pandas
- openpyxl

## Observações

- Os dados gerados são simulados e aleatórios
- Os preços base dos veículos são fixos, mas têm variação aleatória
- O relatório é formatado automaticamente para melhor visualização

### dashboard_vendas.py

Este script cria um dashboard interativo usando Streamlit com as seguintes características:

1. **Upload de Dados**:
   - Upload de planilhas CSV e Excel (.xlsx/.xls)
   - Validação automática de colunas obrigatórias
   - Normalização de nomes de colunas (minúsculo, sem espaços)
   - Suporte a múltiplos formatos de data
   - Barra de progresso animada no carregamento
   - Notificação toast com total de registros carregados
   - Botão de limpar dados para resetar o dashboard

2. **Cards Principais (KPIs)**:
   - Total de Vendas
   - Faturamento Total
   - Ticket Médio
   - Total de Modelos

3. **Gráficos**:
   - Evolução do Faturamento Diário
   - Distribuição do Faturamento por Modelo
   - Ranking de Faturamento por Modelo

4. **Tabelas Detalhadas**:
   - Resumo por Modelo
   - Dados Brutos

5. **Filtros Dinâmicos** (barra inline abaixo dos KPIs):
   - Seleção por período (De/Até)
   - Seleção por modelos com contador
   - Exportação de dados em CSV

6. **Interface e UX**:
   - Sidebar com ícones SVG estilo Lucide/shadcn
   - Seções organizadas em cards com bordas sutis
   - CSS customizado com gradientes e design responsivo
   - Controle de estado via `st.session_state`
   - Cache de dados com `@st.cache_data`
   - Feedback visual com `st.toast` e `st.progress`

## Como Usar

1. Primeiro, crie um ambiente virtual e ative-o:

python -m venv venv
venv\Scripts\activate

2. Instale as dependências necessárias:

pip install pandas openpyxl streamlit plotly

3. Execute os scripts na seguinte ordem:

python arquivo_vendas.py
python analise_vendas.py
streamlit run dashboard_vendas.py

4. Verifique os arquivos gerados:
   - `arquivo_vendas.csv`: Contém os dados brutos
   - `relatorio_vendas.xlsx`: Contém as análises formatadas
   - Dashboard interativo: Acessível via navegador após executar o Streamlit

## Resultados

O projeto oferece três formas de visualização dos dados:

1. **Arquivo CSV** (`arquivo_vendas.csv`):
   - Dados brutos das vendas

2. **Relatório Excel** (`relatorio_vendas.xlsx`):
   - Visão geral do faturamento por produto
   - Identificação do produto mais vendido
   - Identificação do produto menos vendido
   - Valores formatados em reais (R$)
   - Layout profissional com formatação adequada

3. **Dashboard Interativo**:
   - Upload de planilhas próprias (CSV/Excel) com validação automática
   - Visualização em tempo real dos dados
   - Gráficos interativos com Plotly
   - Filtros dinâmicos inline (período e modelos)
   - KPIs estratégicos com cards gradientes
   - Barra de progresso animada no carregamento
   - Notificações toast de feedback
   - Botão de limpar dados
   - Sidebar com ícones SVG (Lucide/shadcn)
   - Interface moderna e responsiva
   - Exportação de dados

## Requisitos

- Python 3.x
- pandas
- openpyxl
- streamlit
- plotly

## Observações

- Os dados gerados são simulados e aleatórios
- Os preços base dos veículos são fixos, mas têm variação aleatória
- O relatório é formatado automaticamente para melhor visualização
- O dashboard é interativo e pode ser acessado via navegador web

# Instalação das dependências na AWS

mkdir meu_projeto

CD meu_projeto

python3 -m venv venv
source venv/bin/activate

# 1. Atualize o sistema

sudo yum update -y

# 2. Instale o Python e pip

sudo yum install python3 python3-pip -y

# 3. Instale o git

sudo yum install git -y

# 4. Clone seu repositório

https://github.com/Brunoxd23/dashboard_vendas.git
cd dashboard_vendas

# 5. Instale as dependências

pip3 install -r requirements.txt

# 6. Instale o Streamlit

pip3 install streamlit

# 7. Instale e use o tmux para manter o dashboard rodando

sudo yum install tmux -y

tmux new -s dashboard

Anexar a uma sessão existente:

tmux attach-session -t dashboard

Listar sessões ativas:

tmux list-sessions

Sair do tmux sem fechar a sessão:
Pressione Ctrl + B, depois D.

para entrar na sessão
tmux attach-session -t dashboard

# 8. Dentro da sessão tmux, execute o dashboard

streamlit run dashboard_vendas.py --server.port 8501 --server.address 0.0.0.0

# 9. Puxe as atualizações do GitHub

git pull origin main
