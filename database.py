database = "CREATE DATABASE MercadoLivre;"
tabela = "CREATE TABLE produtos (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,Nome VARCHAR(250) NOT NULL,precoProduto VARCHAR(250) NOT NULL, recomendado VARCHAR(250) NOT NULL, dataInsert Datetime not null);"

# Importamos a biblioteca:
import pymysql

# Abrimos uma conexão com o banco de dados:
conexao = pymysql.connect(db='MercadoLivre', user='root', passwd='root')

# Cria um cursor:
cursor = conexao.cursor()

# Executa o comando:
#cursor.execute(database)
cursor.execute(tabela)

# Efetua um commit no banco de dados.
# Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
# suas alterações.
conexao.commit()

# Finaliza a conexão
conexao.close()