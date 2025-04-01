import streamlit as st
import requests

# Título da aplicação
st.title('Pesquisa de Preços de Produtos')

# Campo para digitar o nome do produto
produto = st.text_input('Digite o nome do produto que você quer buscar:', '')

# Função para chamar a API Flask
def buscar_precos(produto):
    url = f"http://localhost:5000/buscar-preco?produto={produto}"
    response = requests.get(url)
    return response.json()

# Quando o usuário clicar no botão de pesquisa
if st.button('Buscar Preço'):
    if produto:
        st.write('Carregando...')
        # Chama a API Flask para buscar preços
        dados = buscar_precos(produto)

        if 'precos' in dados:
            st.subheader('Preços encontrados:')
            for preco in dados['precos']:
                st.write(preco)
        else:
            st.error(dados.get('erro', 'Erro desconhecido'))
    else:
        st.error("Por favor, digite o nome de um produto.")
