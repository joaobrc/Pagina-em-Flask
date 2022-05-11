from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from cadastro import Anime, Usuarios, Mangas
from helps import conectabano, recupera_imagen, excluir_imagem
from aniteca import app, db
import time

@app.route('/')
def inicio():
    listaanime = conectabano(methods=1)
    listAnimes = listaanime.lista()
    return render_template("lista.html", titulo="AniTeca", animes = listAnimes)


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

@app.route('/login')
def login():
    proxima = request.args.get("proxima")

    return render_template("login.html", titulo="Faça seu Login" ,proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    proxima_pagina = request.form["proxima"]
    usuario = conectabano(2).buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.nome
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
    anime = conectabano(1).buscar_animes_id(id)
    nome_imagem = recupera_imagen(id)
    return render_template("editar.html", titulo="Editando Animes", anime=anime, capa_anime=nome_imagem )### arrumar para animes e mangas


@app.route('/atualizar',methods=['POST',])
def atualizar():
    nome = request.form['nome']
    tipo = request.form['tipo']
    episodios = request.form['episodios']
    id = request.form['id']
    anime = Animes(nome,tipo,episodios, id)
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    excluir_imagem(anime.id)
    timestampp = time.time()
    arquivo.save('{}/capa{}-{}.jpg'.format(upload_path,anime.id,timestampp))
    conectabano(1).salvar(anime)
    return redirect(url_for('inicio'))

@app.route('/deletar/<int:id>')
def deletar(id):
    conectabano(1).deletar_anime(id)
    flash("Anime Deletado")
    return redirect(url_for('inicio'))
    

@app.route('/uploads/<nome_imagem>')
def imagem(nome_imagem):
    return send_from_directory('uploads',nome_imagem)