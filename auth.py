from flask import render_template, request, redirect, session, flash, url_for
from stock_master_control import app,db
from models import Usuario
from views import *
@app.route('/')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    usuario = Usuario.query.filter_by(login=request.form['usuario']).first()
    if (usuario):
        senha = usuario.senha
        if (request.form['senha'] == senha):
            session['usuario_logado'] = usuario.login
            flash(usuario.login + ' logado com sucesso!')
            proxima_pagina = url_for('menu')
            if (request.form['proxima'] != 'None'):
                proxima_pagina = request.form['proxima']

            return redirect(proxima_pagina)

    else:
        flash('login não realizado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout efetuado com sucesso")
    return redirect(url_for('login'))

@app.route('/novo_usuario')
def cadastrar_usuario():
    return render_template('cadastrar_usuario.html', titulo='Cadastrar novo usuário')

@app.route('/criar_usuario',methods = ['POST',])
def criar_usuario():
    nome = request.form['nome']
    login = request.form['login']
    senha = request.form['senha']

    usuario = Usuario.query.filter_by(login=login).first()

    if usuario:
        flash('Este login já está em uso!')
        return redirect(url_for('cadastrar_usuario'))

    novo_usuario = Usuario(nome=nome, login=login, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('login'))



