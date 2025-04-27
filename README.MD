
# Armazenando Dados de um Ecommerce na Azure

Usando o um Banco de Dados SQL e um Storage Account para armazenar dados de produtos e foto na Azure

## 🛠 Habilidades
SQL Database, Storage Accounts, Blobs, Azure, Query String, Python, Streamit...

## Criando o Ecommerce

Para simular o Front-End do Ecommerce, utilizamos o Streamlit do Python para criar uma página basica para cadastro e listagem dos produtos.

Essa página esta conectada ao banco SQL criado na Azure para cadastras os produtos, já a imagem, a mesma é salva num Blob e apenas a url dela é salva no banco de dados.
## Recursos

Ao todo, criamos dois recursos no Azure, um banco de dados SQL e um storage account

![Todos os Recursos](https://github.com/goncasthiago/lab01-azure/blob/main/img/recursos.jpeg?raw=true)


## Front End

Tela de Cadastro de produtos que se conecta ao banco e faz o insert das informações do produto, e salva a imagem do mesmo no storage account

![Cadastro de Produtos](https://github.com/goncasthiago/lab01-azure/blob/main/img/cadastro.jpeg?raw=true)

Por último, uma página para listar todos os produtos cadastrados no banco de dados

![Lista de Produtos](https://github.com/goncasthiago/lab01-azure/blob/main/img/Summarization_input.png?raw=true)


## Laboratório DIO

[Laboratório DIO](https://github.com/digitalinnovationone/Microsoft_Application_Platform)

## Feedback

Se você tiver algum feedback, por favor me deixe saber por meio de thiagodebia@gmail.com

