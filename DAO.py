from cadastro import Anime, Usuarios


SQL_DELETE_ANIME = '''DELETE FROM anime WHERE id = {};'''
SQL_ANIME_POR_ID = '''SELECT * FROM anime WHERE id = {};'''
SQL_USUARIO_POR_ID = '''SELECT * FROM usuario WHERE id = '{}';'''
SQL_ATUALIZA_ANIME = '''UPDATE anime SET nome='{}', tipo='{}', episodios='{}' WHERE id={};'''
SQL_BUSCA_ANIME = '''SELECT * FROM anime'''
SQL_ADICIONAR_ANIME = '''INSERT INTO anime(nome, tipo, episodios) VALUES ('{}','{}','{}') RETURNING id;'''

class AnimeDAO:
    def __init__(self,db):
        self.__db=db
        self.__db.autocommit = True

    def salvar(self, anime):
        
        curs = self.__db.cursor()
        
        if anime.id:
            curs.execute(SQL_ATUALIZA_ANIME.format(anime.nome, anime.tipo, anime.episodios, anime.id))
        else:
            curs.execute(SQL_ADICIONAR_ANIME.format(anime.nome, anime.tipo, anime.episodios))
            anime.id = curs.fetchone()[0]
        return anime


    def lista(self):
        curs = self.__db.cursor()
        curs.execute(SQL_BUSCA_ANIME)
        animes = traduz_anime(curs.fetchall())
        return animes
    

    def buscar_animes_id(self,id):
        curs = self.__db.cursor()
        curs.execute(SQL_ANIME_POR_ID.format(id))
        busca = curs.fetchone()
        return Anime(busca[1],busca[2],busca[3],id=busca[0])


    def deletar_anime(self,id):
        curs = self.__db.cursor()
        curs.execute(SQL_DELETE_ANIME.format(id))
        self.__db.commit()

class UsuariosDAO():
    def __init__(self,db):
        self.__db = db
    

    def buscar_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USUARIO_POR_ID.format(id))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

def traduz_anime(jogos):
    def cria_anime_com_tupla(tupla):
        return Anime(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_anime_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuarios(tupla[0], tupla[1], tupla[2])



