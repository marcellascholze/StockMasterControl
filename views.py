from flask import render_template, request, redirect, session, flash, url_for
from stock_master_control import app,db
#from models import Jogos, Usuarios

@app.route('/')
def menu():
    return render_template('menu.html', titulo = 'Menu')

@app.route('/visualizar_estoque')
def visualizar_estoque():
    return render_template('visualizar_estoque.html', titulo = 'Estoque')

@app.route('/visualizar_metricas')
def visualizar_metricas():
    return render_template('visualizar_metricas.html', titulo = 'Fechamento do mês')
@app.route('/historico_vendas')
def historico_vendas():
    return render_template('historico_vendas.html', titulo = 'Histórico de vendas')
@app.route('/novo_produto')
def cadastrar_produto():
    #if('usuario_logado' not in session or session['usuario_logado'] == None):
        #return  redirect(url_for('login', proxima = url_for('cadastrar_jogos')))

    return render_template('cadastrar_produto.html', titulo = 'Cadastrar novo produto')

@app.route('/criar_produto',methods = ['POST',])
def criar_produto():
    """nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()"""

    return redirect(url_for('menu'))

@app.route('/cadastrar_usuario')
def cadastrar_usuario():
    #if('usuario_logado' not in session or session['usuario_logado'] == None):
        #return  redirect(url_for('login', proxima = url_for('cadastrar_jogos')))

    return render_template('cadastrar_usuario.html', titulo = 'Cadastrar novo usuário')

@app.route('/criar_usuario',methods = ['POST',])
def criar_usuario():
    """nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()"""

    return redirect(url_for('menu'))
@app.route('/nova_venda')
def cadastrar_venda():
    #if('usuario_logado' not in session or session['usuario_logado'] == None):
        #return  redirect(url_for('login', proxima = url_for('cadastrar_jogos')))

    return render_template('cadastrar_venda.html', titulo = 'Cadastrar nova venda')

@app.route('/criar_venda',methods = ['POST',])
def criar_venda():
    """nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()"""

    return redirect(url_for('menu'))

@app.route('/editar_produto/<int:id>')
def editar(id):
   # if('usuario_logado' not in session or session['usuario_logado'] == None):
    #    return  redirect(url_for('login', proxima = url_for('editar')))

  #  jogo = Jogos.query.filter_by(id = id).first()

    return render_template('editar_produto.html', titulo = 'Editar produto')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
   """"  usuario = Usuarios.query.filter_by(nickname = request.form['usuario']).first()
    if (usuario):
        senha = usuario.senha
        if (request.form['senha'] == senha):
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('login não realizado')
        return redirect(url_for('login'))"""

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout efetuado com sucesso")
    return redirect(url_for('index'))



"""@app.route('/atualizar',methods = ['POST',])
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

    return redirect(url_for('index'))"""


