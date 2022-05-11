import psycopg2
conn = psycopg2.connect(dbname='flask', user='postgres',password='1q2w3e4r',host='localhost',port='5432')

conn.autocommit = True

criando_tabela = '''CREATE TABLE anime (id SERIAL PRIMARY KEY NOT NULL, nome VARCHAR(255) NOT NULL, tipo VARCHAR(255) NOT NULL, episodios VARCHAR(255) NOT NULL);
CREATE TABLE usuario(id VARCHAR(10) PRIMARY KEY NOT NULL, nome VARCHAR(255) NOT NULL, senha VARCHAR(16) NOT NULL);'''

conn.cursor().execute(criando_tabela)

curs = conn.cursor()

curs.executemany('INSERT INTO usuario(id, nome, senha) VALUES (%s,%s,%s)',[('joao','Joao R','1q2w3e'),('emi','Emi C','1q2w'),('hina','Hina M', '1q2w3e4r')])

curs.execute('select * from usuario')

print('-----tabela users-----')
for user in curs.fetchall():
    print(user[1])

curs.executemany('INSERT INTO anime(nome, tipo, episodios) VALUES(%s, %s, %s)',[('86','Ação','24'),('Komi-sa','Romance','12'),('Re:Zero','Horro','48')])

curs.execute('select * from anime')
print('-----tabela animes-----')
for anime in curs.fetchall():
    print(anime[1])

curs.close()