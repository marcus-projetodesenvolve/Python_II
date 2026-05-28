import os
import json
import requests
import matplotlib.pyplot as plt
from skimage import io

# ==========================================
# 1. CARREGAMENTO DA CHAVE DE AUTENTICAÇÃO
# ==========================================
def carregar_api_key():
    try:
        with open('key.json', 'r') as file:
            dados = json.load(file)
            return dados.get('API_KEY', 'DEMO_KEY')
    except (FileNotFoundError, json.JSONDecodeError):
        print("Aviso: 'key.json' não encontrado ou inválido. Usando 'DEMO_KEY'.")
        return 'DEMO_KEY'

API_KEY = carregar_api_key()


# ==========================================
# 2 & 3. ASTRONOMY PICTURE OF THE DAY (APOD) & LIMITES
# ==========================================
print("--- [Etapa 2 & 3] Acessando APOD ---")
url_apod = 'https://api.nasa.gov/planetary/apod'
params_apod = {'api_key': API_KEY}

response_apod = requests.get(url_apod, params=params_apod)

if response_apod.status_code == 200:
    data_apod = response_apod.json()
    
    # 2. Imprimir campos copyright e explanation
    print(f"Copyright: {data_apod.get('copyright', 'Domínio Público')}")
    print(f"Explanation: {data_apod.get('explanation')}\n")
    
    # 3. Consultar e imprimir limites do Header
    limite_total = response_apod.headers.get('X-RateLimit-Limit')
    limite_restante = response_apod.headers.get('X-RateLimit-Remaining')
    print(f"Limite Total da API: {limite_total}")
    print(f"Limite Restante da API: {limite_restante}\n")
    
    # 2. Plotar a imagem usando scikit-image e matplotlib
    url_imagem = data_apod.get('hdurl', data_apod.get('url'))
    try:
        img_apod = io.imread(url_imagem)
        plt.figure(figsize=(10, 6))
        plt.imshow(img_apod)
        plt.title(data_apod.get('title', 'NASA APOD'))
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Não foi possível plotar a imagem (pode ser um vídeo). URL: {url_imagem}")
else:
    print(f"Erro ao acessar APOD: Código {response_apod.status_code}")


# ==========================================
# 4. MARS ROVER PHOTOS - MANIFEST
# ==========================================
print("\n--- [Etapa 4] Acessando Manifest do Rover ---")
rover = 'curiosity'
url_manifest = f'https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}'

response_manifest = requests.get(url_manifest, params={'api_key': API_KEY})

if response_manifest.status_code == 200:
    manifest_data = response_manifest.json()['photo_manifest']
    max_sol = manifest_data['max_sol']
    max_date = manifest_data['max_date']
    
    print(f"Rover: {rover.capitalize()}")
    print(f"max_sol (Máximo dia marciano): {max_sol}")
    print(f"max_date (Última data terrestre): {max_date}\n")
else:
    print(f"Erro ao acessar Manifest: Código {response_manifest.status_code}")
    max_sol = 1000  # Valor padrão caso falhe


# ==========================================
# 5. MARS ROVER PHOTOS - PAGINAÇÃO E FILTRAGEM
# ==========================================
print("--- [Etapa 5] Buscando e Paginando Fotos do Rover ---")
url_photos = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'

# Configurações para a busca
sol_selecionado = max_sol  # Usa o max_sol descoberto na etapa anterior
camera_selecionada = 'FHAZ' # Opções comuns: 'NAVCAM', 'FHAZ', 'RHAZ'
pagina = 1

while True:
    print(f"Requisitando página {pagina} para o Sol {sol_selecionado}...")
    
    params_photos = {
        'api_key': API_KEY,
        'sol': sol_selecionado,
        'page': pagina
    }
    
    response_photos = requests.get(url_photos, params=params_photos)
    
    if response_photos.status_code != 200:
        print(f"Erro na requisição da página {pagina}. Código: {response_photos.status_code}")
        break
        
    dados_fotos = response_photos.json()
    lista_fotos = dados_fotos.get('photos', [])
    
    # Condição de parada: se a lista vier vazia ou nula, interrompe a paginação
    if not lista_fotos:
        print(f"Paginação encerrada. Nenhum resultado ou fim das páginas na página {pagina}.")
        break
        
    # Varre as fotos da página atual filtrando pela câmera escolhida
    encontrou_foto = False
    for foto in lista_fotos:
        if foto['camera']['name'] == camera_selecionada:
            encontrou_foto = True
            link_foto = foto['img_src']
            id_foto = foto['id']
            
            # Carrega e exibe a imagem do robô
            try:
                img_rover = io.imread(link_foto)
                plt.figure(figsize=(8, 5))
                plt.imshow(img_rover)
                
                # Título conforme a regra: página da requisição, nome da câmera e id da imagem
                plt.title(f"Página: {pagina} | Câmera: {camera_selecionada} | ID: {id_foto}")
                plt.axis('off')
                plt.show()
            except Exception as e:
                print(f"Erro ao carregar a imagem ID {id_foto}: {e}")
                
    if not encontrou_foto:
        print(f"Nenhuma foto da câmera {camera_selecionada} encontrada na página {pagina}.")
        
    # Avança para a próxima página do loop
    pagina += 1