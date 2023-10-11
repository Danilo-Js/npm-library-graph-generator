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

package_name = "react-native-search-select"
start_date = "2022-12-03"
end_date = datetime.now().strftime('%Y-%m-%d')

# Buscar detalhes do pacote
package_url = f"https://registry.npmjs.org/{package_name}"
package_response = requests.get(package_url)
all_time_data = package_response.json()['time']

version_date_map = {d.split('T')[0]: v for v, d in all_time_data.items() if v.replace('.', '').isnumeric()}

# Buscar downloads por data
downloads_url = f"https://api.npmjs.org/downloads/range/{start_date}:{end_date}/{package_name}"
downloads_response = requests.get(downloads_url)
downloads_data = downloads_response.json()['downloads']

dates = []
downloads = []
versions_on_release = []

# Estruturando os dados
for entry in downloads_data:
    date = entry['day']
    download = entry['downloads']
    version = version_date_map.get(date)

    dates.append(datetime.strptime(date, '%Y-%m-%d'))
    downloads.append(download)
    versions_on_release.append(version if version else 'N/A')

# Filtrando dados para entradas onde a versão não é "N/A"
filtered_downloads = [d for v, d in zip(versions_on_release, downloads) if v != 'N/A']
filtered_versions = [v for v in versions_on_release if v != 'N/A']

# Estruturando os dados e acumulando downloads por versão
version_downloads = defaultdict(int)
for entry in downloads_data:
    date = entry['day']
    download = entry['downloads']
    
    # A versão associada à data ou a versão anterior se a data atual não tiver uma nova versão lançada
    version = version_date_map.get(date, None)
    if not version:
        valid_dates = [d for d in version_date_map.keys() if d <= date]
        if valid_dates:
            version = version_date_map[max(valid_dates)]
            
    if version:
        version_downloads[version] += download

# plot_downloads_x_data(dates, downloads)
plot_downloads_x_version_on_release(filtered_versions, filtered_downloads)
# plot_cumulative_downloads_x_version(version_downloads)
