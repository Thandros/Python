import requests
from bs4 import BeautifulSoup
import json

# Lê a chave da API e o ID do mecanismo de pesquisa (CX)
API_KEY = open('API_KEY').read().strip()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read().strip()

# Termo de pesquisa
consulta = 'samsung galaxy s24 ultra preço'

# URL da API do Google Custom Search
url = 'https://www.googleapis.com/customsearch/v1'

# Parâmetros da consulta
params = {
    'q': consulta,
    'key': API_KEY,
    'cx': SEARCH_ENGINE_ID,
    'gl': 'br',
    'hq': 'site:.br'
}

# Realiza a requisição à API do Google Custom Search
response = requests.get(url, params=params)

# Verifica se a resposta da API foi bem-sucedida
if response.status_code == 200:
    try:
        resultados = response.json()
        dados = []

        if 'items' in resultados:
            for item in resultados['items']:
                link = item['link']

                # Função para obter preço da página
                def obter_preco_da_pagina(url):
                    resposta = requests.get(url)
                    if resposta.status_code == 200:
                        sopa = BeautifulSoup(resposta.text, 'html.parser')
                        tag_preco = sopa.find('span', class_='price')  # Ajustar conforme a página
                        if tag_preco:
                            return tag_preco.text.strip()
                    return "Preço não encontrado"

                # Obtém o preço
                preco = obter_preco_da_pagina(link)

                # Adiciona ao JSON de retorno
                dados.append({"link": link, "preco": preco})

        # Retorna o JSON formatado
        print(json.dumps(dados, indent=4, ensure_ascii=False))

    except ValueError as e:
        print(json.dumps({"erro": "Falha ao decodificar JSON", "detalhes": str(e)}, indent=4, ensure_ascii=False))

else:
    print(json.dumps({"erro": f"Erro HTTP {response.status_code}"}, indent=4, ensure_ascii=False))
