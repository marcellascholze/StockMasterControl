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

    return render_template('cadastrar_usuario.html', titulo = 'Cadastrar novo usuário')

@app.route('/criar_usuario',methods = ['POST',])
def criar_usuario():

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

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    pass

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout efetuado com sucesso")
    return redirect(url_for('index'))



