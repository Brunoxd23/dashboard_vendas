import pandas as pd
from datetime import datetime, timedelta
import random

# Lista de carros com seus preços base
carros = {
    'Honda Civic': 120000,
    'Toyota Corolla': 115000,
    'Volkswagen Golf': 95000,
    'Hyundai HB20': 75000,
    'Fiat Pulse': 89000,
    'Jeep Compass': 150000,
    'Chevrolet Onix': 70000,
    'Ford Territory': 140000
}

# Criando lista para armazenar os dados
dados = []

# Gerando dados para os últimos 30 dias
data_inicial = datetime.now() - timedelta(days=30)

for dia in range(30):
    data = data_inicial + timedelta(days=dia)
    
    # Para cada dia, geramos algumas vendas aleatórias
    for _ in range(random.randint(3, 8)):  # 3 a 8 vendas por dia
        carro = random.choice(list(carros.keys()))
        preco_base = carros[carro]
        
        # Variação aleatória no preço (±5%)
        preco_unitario = preco_base * random.uniform(0.95, 1.05)
        
        # Quantidade vendida (1 a 3 unidades)
        quantidade = random.randint(1, 3)
        
        dados.append({
            'data': data.strftime('%d/%m/%Y'),
            'produto': carro,
            'quantidade': quantidade,
            'preco_unitario': round(preco_unitario, 2)
        })

# Criando o DataFrame
df = pd.DataFrame(dados)

# Salvando em CSV
df.to_csv('arquivo_vendas.csv', index=False)

# Salvando em Excel
df.to_excel('arquivo_vendas.xlsx', index=False)

print("Arquivos 'arquivo_vendas.csv' e 'arquivo_vendas.xlsx' foram criados!")

# Mostrando as primeiras linhas do DataFrame
print("\nPrimeiras linhas do arquivo gerado:")
print(df.head())