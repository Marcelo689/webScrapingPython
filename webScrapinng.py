from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pymysql
import time
# Abrimos uma conexão com o banco de dados:
conexao = pymysql.connect(db='MercadoLivre', user='root', passwd='root')
# Cria um cursor:
cursor = conexao.cursor()
dataDaBusca = datetime.now()  

def FormataPalavraParaBuscaTerabyte(entrada):
    saida = entrada.replace(" ", "+")
    return saida

def convertTimestampToSQLDateTime(value):
    return time.strftime('%Y-%m-%d %H:%M:%S',datetime.timestamp(value))

def FormataPalavraParaBuscaMercadoLivre(entrada):
    saida = entrada.replace(" ", "%20")
    inicio = entrada.replace(" ", "-")
    fim =  f"#D[A:{saida}]"
    busca = inicio + fim
    return busca

def InserirProdutoDB(nome,precoProduto,recomendado,data):
    insertProduto = f"INSERT INTO produtos(Nome,precoProduto,recomendado,dataInsert) VALUES({nome},{precoProduto},{recomendado},{data});"
    # Executa o comando:
    cursor.execute(insertProduto)

def ConteudoTag(textoHtml):
    return re.search(">(.*)<", str(textoHtml)).group(1)

dataDaBusca = convertTimestampToSQLDateTime(dataDaBusca)
# Site que será coletado
mercadoLivre = "https://lista.mercadolivre.com.br/"
#site = "https://www.terabyteshop.com.br/"
palavraChave = "placa de video"
palavraChaveFormatada = FormataPalavraParaBuscaMercadoLivre(palavraChave)
filtro = f"{palavraChaveFormatada}"

mercadoLivre += filtro
# Coleta os dados do site
html = requests.get(mercadoLivre).content

# Formatando os dados
dados = BeautifulSoup(html, 'html.parser')
#print(dados.prettify())

# # Busca por tag HTML
# busca_por_tag = dados.find("TAG_BUSCADA")

# # Busca por id
# busca_por_id = dados.find(id="ABC")

# # Busca por class
# busca_por_class = dados.find(class_="XYZ")

# # Buscando todos os elementos
# busca_tudo = dados.find_all("div")

classDivItem = "ui-search-layout ui-search-layout--grid"
classPrecoItem = "price-tag-fraction"
classMaisVendido = "ui-search-styled-label ui-search-item__highlight-label__text"
classNomeProduto = "ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title"

itens = dados.find_all(class_= classDivItem)

print(len(itens))
for iten in itens:
    tagNome = iten.find( class_ = classNomeProduto)
    if(tagNome):
        nome = ConteudoTag(tagNome)
    else:
        nome = ""
    tagPreco = iten.find( class_ = classPrecoItem)
    if(tagPreco):
        preco = ConteudoTag(tagPreco)
    else:
        preco = ""
    tagMaisVendido = iten.find( class_= classMaisVendido)
    if(tagMaisVendido):
        isMaisVendido = ConteudoTag(tagMaisVendido)
    else:
        isMaisVendido = ""
    InserirProdutoDB(nome,preco,isMaisVendido,dataDaBusca)

conexao.commit()
# Finaliza a conexão
conexao.close()