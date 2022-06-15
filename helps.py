import psycopg2
import os
from aniteca import app
##from DAO import AnimeDAO, UsuariosDAO
#
#
#def conec_db(dbname,user,senha,host,port):
#    conn =  psycopg2.connect(dbname=dbname, user=user,password=senha,host=host,port=port)
#    return conn
#
#def conectabano(methods:int):
#    if methods == 1:
#        anime_dao = AnimeDAO(conec_db('flask','postgres','1q2w3e4r','localhost','5432'))
#        return anime_dao
#    elif methods == 2:
#        usuario_dao = UsuariosDAO(conec_db('flask','postgres','1q2w3e4r','localhost','5432'))
#        return usuario_dao
#    else:
#        ValueError('Metedo Invalido')

def recupera_imagen(id):
    for arquiv_nome in os.listdir(app.config['UPLOAD_PATH']):
        if 'capa{}'.format(id) in arquiv_nome:
            return arquiv_nome

def excluir_imagem(id):
    imagem = recupera_imagen(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'],imagem))