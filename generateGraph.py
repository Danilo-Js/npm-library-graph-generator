import requests
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Exibindo gráfico dos downloads por data
def plot_downloads_x_data(dates, downloads, versions):
    fig, ax = plt.subplots(figsize=(15, 7)) # Cria uma nova figura com o tamanho definido.
    ax.plot(dates, downloads, '-o', color='blue') # Plota os dados de downloads com as datas e com um estilo definido.
    for i, (date, download) in enumerate(zip(dates, downloads)):  # Anota as versões correspondentes em cada ponto do gráfico.
        ax.annotate(versions[i], (date, download), textcoords="offset points", xytext=(0,10), ha='center')
    ax.set_title('Downloads x Data') # Define o título do gráfico.
    ax.set_xlabel('Data') # Define o título do eixo x.
    ax.set_ylabel('Downloads') # Define o título do eixo y.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y')) # Define o formato da data no eixo x.
    ax.xaxis.set_major_locator(mdates.MonthLocator()) # Define o espaçamento entre os meses no eixo x.
    plt.xticks(rotation=90) # Rotaciona os rótulos do eixo x.
    ax.grid(True) # Habilita as linhas de grade.
    plt.tight_layout() # Ajusta o layout do gráfico para que não haja sobreposição de elementos.
    plt.show() # Exibe o gráfico.

# Exibindo gráfico dos downloads por versão
def plot_downloads_x_version(version_downloads):
    plt.figure(figsize=(10, 5)) # Cria uma nova figura com o tamanho definido.
    plt.bar(version_downloads.keys(), version_downloads.values(), color='blue') # Plota os dados de downloads com as versões e com um estilo definido.
    plt.title('Downloads x Versão') # Define o título do gráfico.
    plt.xlabel('Versão') # Define o título do eixo x.
    plt.ylabel('Downloads') # Define o título do eixo y.
    plt.xticks(rotation=45) # Rotaciona os rótulos do eixo x.
    plt.grid(True) # Habilita as linhas de grade.
    plt.tight_layout() # Ajusta o layout do gráfico para que não haja sobreposição de elementos.
    plt.show() # Exibe o gráfico.

interested_versions = ['1.2.2', '3.0.8', '3.0.9', '4.0.0'] # Principais versões
url = f"https://registry.npmjs.org/react-native-search-select" # Endereço da API para obter informações do pacote.
response = requests.get(url) # Obtendo os dados do pacote 
data = response.json()['time'] # Formatanto os dados

# Mapeando datas de lançamento para versões
version_date_map = {d.split('T')[0]: v for v, d in data.items() if v in interested_versions}

# Obtendo dados de downloads
downloads_url = f"https://api.npmjs.org/downloads/range/2022-12-03:{datetime.now().strftime('%Y-%m-%d')}/react-native-search-select" # Endereço da API para obter informações de downloads do pacote.
downloads_response = requests.get(downloads_url) # Obtendo os dados de downloads do pacote
downloads_data = downloads_response.json()['downloads'] # Formatando os dados

# Prepara listas para armazenar as datas e downloads.
dates = []
downloads = []
# Cria um dicionário para acumular os downloads por versão.
version_downloads = defaultdict(int)

# Processa cada entrada nos dados de downloads.
for entry in downloads_data:
    date = entry['day'] # Data do download.
    download = entry['downloads'] # Quantidade de downloads.
    version = version_date_map.get(date) # Versão lançada na data.  
    # se ela estiver na lista de interesse e houver downloads, adiciona a data e o download às listas.
    if version and download > 0:
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
        downloads.append(download)
        version_downloads[version] += download

# Plotando os gráficos
plot_downloads_x_data(dates, downloads, interested_versions)
plot_downloads_x_version(version_downloads)