import streamlit as st
from azure.storage.blob import BlobServiceClient
import pymssql
import uuid
import json
import os
import pandas as pd

# Configurações do Azure Storage via variáveis de ambiente
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "produtos"
ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

# Configurações do Azure SQL Server via variáveis de ambiente
SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

# Título da aplicação
st.title("Cadastro de Produto - E-Commerce na Cloud")

# Formulário para cadastro do produto
product_name = st.text_input("Nome do Produto")
description = st.text_area("Descrição do Produto")
price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
uploaded_file = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

def upload_image(file):
    """Faz upload da imagem para o Azure Blob Storage."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True)
        return f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
    except Exception as e:
        st.error(f"Erro ao enviar imagem: {e}")
        return None

def execute_sql(query, params=None, fetch=False):
    """Executa consultas SQL com gerenciamento seguro de conexões."""
    try:
        with pymssql.connect(server=SQL_SERVER, user=SQL_USERNAME, password=SQL_PASSWORD, database=SQL_DATABASE) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                conn.commit()
    except Exception as e:
        st.error(f"Erro ao executar SQL: {e}")
        return [] if fetch else False

def list_products():
    """Lista os produtos armazenados no banco de dados."""
    return execute_sql("SELECT id, nome, descricao, preco, imagem_url FROM dbo.Produtos", fetch=True)

def list_products_screen():
    """Exibe os produtos em um layout responsivo."""
    products = list_products()
    if products:
        for product in products:
            with st.expander(product['nome']):
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R$ {product['preco']:.2f}")
                if product["imagem_url"]:
                    st.image(product["imagem_url"], width=200)
    else:
        st.info("Nenhum produto encontrado.")

if st.button("Cadastrar Produto"):
    if not product_name or not description or price is None:
        st.warning("Preencha todos os campos obrigatórios!")
    else:
        image_url = upload_image(uploaded_file) if uploaded_file else ""
        product_data = {"nome": product_name, "descricao": description, "preco": price, "imagem_url": image_url}

        if execute_sql("INSERT INTO dbo.Produtos (nome, descricao, preco, imagem_url) VALUES (%s, %s, %s, %s)", 
                       (product_data["nome"], product_data["descricao"], product_data["preco"], product_data["imagem_url"])):
            st.success("Produto cadastrado com sucesso no Azure SQL!")
            list_products_screen()
        else:
            st.error("Erro ao cadastrar produto.")

st.header("Listagem dos Produtos")
if st.button("Listar Produtos"):
    list_products_screen()
