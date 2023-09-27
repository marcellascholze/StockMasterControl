from flask import render_template, request, redirect, session, flash, url_for
from stock_master_control import app,db
#from models import Jogos, Usuarios

@app.route('/')
def menu():
    return render_template('menu.html')

"""@app.route('/novoProduto')
def cadastrar_produto():
    if('usuario_logado' not in session or session['usuario_logado'] == None):
        return  redirect(url_for('login', proxima = url_for('cadastrar_jogos')))

    return render_template('editar.html', titulo = 'Novo jogo')

@app.route('/editar/<int:id>')
def editar(id):
    if('usuario_logado' not in session or session['usuario_logado'] == None):
        return  redirect(url_for('login', proxima = url_for('editar')))

    jogo = Jogos.query.filter_by(id = id).first()

    return render_template('editar.html', titulo = 'Editar jogo', jogo = jogo)

@app.route('/addJogo',methods = ['POST',])
def add_jogo():
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']

    jogo = Jogos.query.filter_by(nome = nome).first()

    if(jogo):
        flash('Jogo já existente')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome = nome, categoria = categoria, console = console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/atualizar',methods = ['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id = request.form['id']).first()

    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login'))

    jogo = Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname = request.form['usuario']).first()
    if (usuario):
        senha = usuario.senha
        if (request.form['senha'] == senha):
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('login não realizado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout efetuado com sucesso")
    return redirect(url_for('menu'))"""
