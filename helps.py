import psycopg2
import os
from aniteca import app

def recupera_imagen(id):
    for arquiv_nome in os.listdir(app.config['UPLOAD_PATH']):
        if 'capa{}'.format(id) in arquiv_nome:
            return arquiv_nome

def excluir_imagem(id):
    imagem = recupera_imagen(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'],imagem))