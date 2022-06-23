from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from cadastro import Anime, Usuario, Mangas
from helps import  recupera_imagen, excluir_imagem
from aniteca import app, db
import time


@app.route('/')
def inicio():
    listaanime = Anime.query.all()
    listamangas = Mangas.query.all()
    return render_template("home.html", titulo="AniTeca", animes = listaanime, mangas=listamangas)


@app.route('/cadastroanimes')
def cadastroanimes():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('cadastroanimes')))
    else:
        return render_template("cadastroanimes.html", titulo="Cadastro de Animes")


@app.route('/salvar',methods = ['POST',])
def salvar():
    nome = request.form['nome']
    tipo = request.form['tipo']
    episodios = request.form['episodios']
    anime = Anime(nome,tipo,episodios)
    db.session.add(anime)
    db.session.commit()
    arquivo = request.files['arquivo']
    timestampp = time.time()
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save('{}/capa{}-{}.jpg'.format(upload_path,anime.id,timestampp))
    return redirect(url_for('inicio'))


@app.route('/cadastromangas')
def cadastromangas():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('cadastromangas')))
    else:
        return render_template("cadastromangas.html", titulo="Cadastro de Mangas")


@app.route('/salvar_mangas',methods= ['POST',])
def salvar_mangas():
    nome = request.form['nome']
    tipo = request.form['tipo']
    capitulos = request.form['capitulos']
    manga = Mangas(nome, tipo, capitulos)
    db.session.add(manga)
    db.session.commit()
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(r'{}/capamanga{}.jpg'.format(upload_path, manga.id))
    return redirect(url_for('inicio'))


@app.route('/cadastrousuarios')
def cadastrousuarios():
    return render_template('cadastrousuarios.html', titulo='Cadastro Usuario')



@app.route('/criar_usuario',methods=['POST'])
def criar_usuario():
    nome = request.form['nome']
    user = request.form['user']
    senha = request.form['senha']
    usuario = Usuario(nome=nome, user=user, senha=senha)
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/login')
def login():
    proxima = request.args.get("proxima")

    return render_template("login.html", titulo="Faça seu Login" ,proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    proxima_pagina = request.form["proxima"]
    usuario = Usuario.query.get(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.user
            flash(session['usuario_logado']+" logado com sucesso")
            return redirect(proxima_pagina)
    else:
        flash("Usuario ou Senha Invalida")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Usuario não mais logado")
    return redirect(url_for('inicio'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('editar',id=id)))
    anime = Anime.query.get(id)
    nome_imagem = recupera_imagen(id)
    return render_template("editar.html", titulo="Editando Animes", anime=anime, capa_anime=nome_imagem )### arrumar para animes e mangas


@app.route('/atualizar',methods=['POST',])
def atualizar():
    nome = request.form['nome']
    tipo = request.form['tipo']
    episodios = request.form['episodios']
    id = request.form['id']
    anime = Anime.query.get(id)
    anime.nome = nome
    anime.tipo = tipo
    anime.episodios = episodios
    anime.id = id
    db.session.commit()
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    excluir_imagem(anime.id)
    timestampp = time.time()
    arquivo.save('{}/capa{}-{}.jpg'.format(upload_path,anime.id,timestampp))
    '''editar capa portque esta quebrndo se nao for atualizada'''
    return redirect(url_for('inicio'))


@app.route('/deletar-anime/<int:id>')
def deletar_anime(id):
    anime = Anime.query.get(id)
    db.session.delete(anime)
    db.session.commit()
    flash("Anime Deletado")
    return redirect(url_for('inicio'))
    

@app.route('/deletar-manga/<int:id>')
def deletar_manga(id):
    mangas = Mangas.query.get(id)
    db.session.delete(mangas)
    db.session.commit()
    flash("Manga Deletado")
    return redirect(url_for('inicio'))


@app.route('/uploads/<nome_imagem>')
def imagem(nome_imagem):
    return send_from_directory('uploads',nome_imagem)
