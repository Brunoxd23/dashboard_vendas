# Análise de Vendas de Veículos

Este projeto consiste em dois scripts Python que geram e analisam dados de vendas de veículos.

## Estrutura do Projeto

- `arquivo_vendas.py`: Gera dados simulados de vendas
- `analise_vendas.py`: Analisa os dados e gera relatórios
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
python -m venv venv
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
