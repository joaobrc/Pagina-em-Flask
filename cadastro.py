from aniteca import db


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    episodios = db.Column(db.Integer())

    def __init__(self, nome, tipo, episodios, id = None):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.episodios = episodios


class Usuario(db.Model):
    nome = db.Column(db.String(255), primary_key=True)
    user = db.Column(db.String(255))
    senha = db.Column(db.Integer())

    def __init__(self, nome, user, senha ):
        self.nome = nome
        self.user = user
        self.senha = senha
                
class Mangas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    capitulos = db.Column(db.Integer())

    def __init__(self, nome, tipo, capitulos, id=None):
        self.nome = nome
        self.tipo = tipo 
        self.capitulos = capitulos
        self.id = id