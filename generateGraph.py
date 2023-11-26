import requests
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict


def plot_downloads_x_data(dates, downloads):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, downloads, '-o', color='blue')
    plt.title('Downloads x Data')
    plt.xlabel('Data')
    plt.ylabel('Downloads')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_downloads_x_version_on_release(versions, downloads):
    plt.figure(figsize=(10, 5))
    plt.bar(versions, downloads, color='blue')
    plt.title('Downloads x Versão (No dia de lançamento)')
    plt.xlabel('Versão')
    plt.ylabel('Downloads')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_cumulative_downloads_x_version(version_downloads):
    plt.figure(figsize=(10, 5))
    plt.bar(version_downloads.keys(), version_downloads.values(), color='blue')
    plt.title('Downloads Acumulados x Versão')
    plt.xlabel('Versão')
    plt.ylabel('Downloads')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Informações do pacote e intervalo de datas
package_name = "react-native-search-select"
start_date = "2022-12-03"
end_date = datetime.now().strftime('%Y-%m-%d')

# Versões de interesse
interested_versions = ['1.2.2', '3.0.8', '3.0.9', '4.0.0']

# Obtendo os dados do pacote
package_url = f"https://registry.npmjs.org/{package_name}"
package_response = requests.get(package_url)
all_time_data = package_response.json()['time']

# Mapeando datas de lançamento para versões
version_date_map = {d.split('T')[0]: v for v, d in all_time_data.items() if v in interested_versions}

# Obtendo dados de downloads
downloads_url = f"https://api.npmjs.org/downloads/range/{start_date}:{end_date}/{package_name}"
downloads_response = requests.get(downloads_url)
downloads_data = downloads_response.json()['downloads']

# Preparando dados para plotagem
dates = []
downloads = []
version_downloads = defaultdict(int)

# Acumulando downloads por versão de interesse
for entry in downloads_data:
    date = entry['day']
    download = entry['downloads']
    version = version_date_map.get(date)
    
    # Adicionar a versão se ela estiver na lista de interesse e houver downloads
    if version and download > 0:
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
        downloads.append(download)
        version_downloads[version] += download

# Filtrando para incluir apenas as datas onde versões de interesse foram lançadas
filtered_dates = [dates[i] for i, v in enumerate(dates) if version_date_map.get(v.strftime('%Y-%m-%d'))]
filtered_downloads = [downloads[i] for i, v in enumerate(dates) if version_date_map.get(v.strftime('%Y-%m-%d'))]

# Plotando os gráficos
plot_downloads_x_data(filtered_dates, filtered_downloads)
plot_downloads_x_version_on_release(interested_versions, [version_downloads[v] for v in interested_versions])
plot_cumulative_downloads_x_version(version_downloads)