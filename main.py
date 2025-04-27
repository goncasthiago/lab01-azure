import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
from dotenv import load_dotenv
import uuid
import json

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Azure Blob Storage
BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")

# Configurações do banco de dados MySQL
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# Função para conectar ao banco de dados
def get_db_connection():
    return pymssql.connect(
        host=SQL_SERVER,
        user=SQL_USER,
        password=SQL_PASSWORD,
        database=SQL_DATABASE
    )

# Streamlit app
st.title("Gerenciamento de Produtos")

# Menu de navegação
menu = st.sidebar.selectbox("Menu", ["Cadastrar Produto", "Listar Produtos"])

if menu == "Cadastrar Produto":
    st.header("Cadastro de Produtos")

    # Formulário de cadastro
    with st.form("product_form"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço", min_value=0.0, format="%.2f")
        descricao = st.text_area("Descrição")
        imagem = st.file_uploader("Imagem do Produto", type=["jpg", "png", "jpeg"])
        
        # Botão de submissão
        submitted = st.form_submit_button("Cadastrar Produto")

        if submitted:
            if not nome or not preco or not descricao or not imagem:
                st.error("Por favor, preencha todos os campos.")
            else:
                # Upload da imagem para o Azure Blob Storage
                try:
                    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
                    blob_client = blob_service_client.get_blob_client(container=BlobContainerName, blob=f"{uuid.uuid4()}-{imagem.name}")
                    blob_client.upload_blob(imagem, overwrite=True)
                    imagem_url = blob_client.url

                    # Conexão com o banco de dados e inserção do produto
                    connection = get_db_connection()
                    with connection.cursor() as cursor:
                        sql = """
                        INSERT INTO produtos (nome, preco, descricao, imagem_url)
                        VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(sql, (nome, preco, descricao, imagem_url))
                        connection.commit()
                    
                    st.success("Produto cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar o produto: {e}")

elif menu == "Listar Produtos":
    st.header("Lista de Produtos")

    try:
        # Conexão com o banco de dados para buscar os produtos
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome, preco, descricao, imagem_url FROM produtos")
            produtos = cursor.fetchall()

        # Exibir os produtos
        if produtos:
            cars_por_linha = 3
            colunas = st.columns(cars_por_linha)
            for i, produto in enumerate(produtos):
                nome, preco, descricao, imagem_url = produto
                with colunas[i % cars_por_linha]:
                    st.subheader(nome)
                    st.write(f"**Preço:** R$ {preco:.2f}")
                    st.write(f"**Descrição:** {descricao}")
                    if imagem_url:
                        st.image(imagem_url, width=200)
                    st.markdown("---")
            st.markdown("---")
            
        else:
            st.info("Nenhum produto cadastrado.")
    except Exception as e:
        st.error(f"Erro ao buscar os produtos: {e}")