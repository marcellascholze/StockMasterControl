from flask import render_template, request, redirect, session, flash, url_for
from stock_master_control import app,db

@app.route('/menu')
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
    if('usuario_logado' not in session or session['usuario_logado'] == None):
        return  redirect(url_for('login', proxima = url_for('cadastrar_produto')))

    return render_template('cadastrar_produto.html', titulo = 'Cadastrar novo produto')

@app.route('/criar_produto',methods = ['POST',])
def criar_produto():

    return redirect(url_for('menu'))

@app.route('/nova_venda')
def cadastrar_venda():

    return render_template('cadastrar_venda.html', titulo = 'Cadastrar nova venda')

@app.route('/criar_venda',methods = ['POST',])
def criar_venda():

    return redirect(url_for('menu'))

@app.route('/editar_produto/<int:id>')
def editar(id):

    return render_template('editar_produto.html', titulo = 'Editar produto')



