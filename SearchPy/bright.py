from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitando CORS para todas as rotas

# Rota para buscar o preço do produto
@app.route('/buscar-preco', methods=['GET'])
def buscar_preco():
    produto = request.args.get('produto')
    
    if not produto:
        return jsonify({'erro': 'Produto não informado.'}), 400
    
    # Chama a função para pesquisar preços
    precos = pesquisar_precos(produto)
    
    if precos:
        return jsonify({'precos': precos})
    else:
        return jsonify({'erro': 'Preços não encontrados.'}), 404

# Função para buscar os preços do produto
def pesquisar_precos(produto):
    precos = []
    try:
        query = f"https://www.google.com/search?q={produto}&gl=br&tbm=shop&start=1&num=10"
        response = requests.get(query, timeout=30, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca por preços na primeira classe
            for span in soup.find_all('span', {'class': 'a8Pemb'}):  # Verifique as classes corretas
                preco = span.get_text()
                if preco and len(precos) < 10:
                    precos.append(preco)
            
            # Se não encontrar suficientes preços, tentamos uma segunda classe
            if len(precos) < 10:
                for span in soup.find_all('span', {'class': 'HRLxBb'}):  # Outra classe para tentar encontrar preços
                    preco = span.get_text()
                    if preco and len(precos) < 10:
                        precos.append(preco)
            
            return precos

        else:
            return None
    except Exception as e:
        print(f"Erro ao buscar preços: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
