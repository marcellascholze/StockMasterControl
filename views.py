from flask import render_template, request, redirect, session, flash, url_for
from stock_master_control import app,db
from datetime import datetime
from models import *

@app.route('/menu')
def menu():
    usuario = Usuario.query.filter_by(id=session['usuario_id']).first()
    return render_template('menu.html', titulo = 'Menu', usuario=usuario)

""""--------------------------------------------------produto--------------------------------------------------------"""

@app.route('/visualizar_estoque')
def visualizar_estoque():
    produtos_lista = Produto.query.filter_by(usuario_id=session['usuario_id']).order_by(Produto.id)
    return render_template('visualizar_estoque.html', titulo = 'Estoque', produtos = produtos_lista)
@app.route('/novo_produto')
def cadastrar_produto():
    if('usuario_logado' not in session or session['usuario_logado'] == None):
        return  redirect(url_for('login', proxima = url_for('cadastrar_produto')))

    return render_template('cadastrar_produto.html', titulo = 'Cadastrar novo produto')

@app.route('/criar_produto',methods = ['POST',])
def criar_produto():

    nome = request.form['nome']
    modelo = request.form['modelo']
    data_compra = request.form['data_compra']
    custo_compra = request.form['custo_compra']
    preco_sugerido = request.form['preco_sugerido']
    quantidade = request.form['quantidade']
    usuario_id = session['usuario_id']

    produto = Produto.query.filter_by(nome=nome, modelo=modelo).first()

    if (produto):
        flash('Esse produto já existe')

    novo_produto = Produto(nome=nome,
                           modelo=modelo,
                           data_compra=data_compra,
                           custo_compra=custo_compra,
                           preco_sugerido=preco_sugerido,
                           quantidade=quantidade,
                           usuario_id=usuario_id)
    db.session.add(novo_produto)
    db.session.commit()

    flash(nome + ' salvo com sucesso')
    upsert_metrica_compra(novo_produto)

    return redirect(url_for('visualizar_estoque'))

@app.route('/atualizar_produto',methods = ['POST',])
def atualizar_produto():

    produto = Produto.query.filter_by(id=request.form['id']).first()

    quantidade_antiga = produto.quantidade
    custo_produto_antigo = produto.custo_compra

    produto.nome = request.form['nome']
    produto.modelo = request.form['modelo']
    produto.data_compra = request.form['data_compra']
    produto.custo_compra = request.form['custo_compra']
    produto.preco_sugerido = request.form['preco_sugerido']
    produto.quantidade = request.form['quantidade']
    produto.usuario_id = session['usuario_id']

    db.session.add(produto)
    db.session.commit()


    flash(produto.nome + ' atualizado com sucesso')

    if(produto.custo_compra != custo_produto_antigo or produto.quantidade != quantidade_antiga):
        upsert_metrica_compra_atualiza(produto, quantidade_antiga, custo_produto_antigo)

    return redirect(url_for('visualizar_estoque'))



@app.route('/editar_produto/<int:id>')
def editar_produto(id):
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('editar_produto')))

    produto = Produto.query.filter_by(id=id, usuario_id=session['usuario_id']).first()

    return render_template('editar_produto.html', titulo = 'Editar produto', produto = produto)

@app.route('/deletar_produto/<int:id>')
def deletar_produto(id):
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login'))

    venda = Venda.query.filter_by(produto_id=id).first()
    if (not venda):
        produto_deletado= Produto.query.filter_by(id=id).first()
        produto = Produto.query.filter_by(id=id).delete()
        upsert_metrica_compra_deletada(produto_deletado)
        db.session.commit()
        flash('Produto deletado com sucesso')
    else:
        flash('Produto não pode ser deletado, pois existem vendas vinculadas a ele')

    return redirect(url_for('visualizar_estoque',))
""""--------------------------------------------------venda--------------------------------------------------------"""
@app.route('/nova_venda')
def cadastrar_venda():
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('cadastrar_venda')))

    opcoes_produtos = Produto.query.filter(Produto.quantidade>0)
    opcoes_plataforma = ['Facebook','Mercado livre','OLX', 'Shoppee','WhatsApp', 'Outro']
    opcoes_tipo_entrega = ['Retirada', 'Correio', 'Motoboy','Carro','Bicicleta']
    opcoes_forma_pagamento = ['Dinheiro', 'Crédito', 'Débito','Pix']
    return render_template('cadastrar_venda.html',
                           titulo = 'Cadastrar nova venda',
                           opcoes_produtos = opcoes_produtos,
                           opcoes_plataforma = opcoes_plataforma,
                           opcoes_tipo_entrega = opcoes_tipo_entrega,
                           opcoes_forma_pagamento=opcoes_forma_pagamento )

@app.route('/criar_venda',methods = ['POST',])
def criar_venda():

    nome_cliente = request.form['nome_cliente']
    data_venda = request.form['data_venda']
    quantidade = request.form['quantidade']
    tipo_entrega = request.form['tipo_entrega']
    valor_entrega = request.form['valor_entrega'] if request.form['valor_entrega'] else 0
    forma_pagamento = request.form['forma_pagamento']
    valor_bruto = request.form['valor_bruto']
    lucro = request.form['lucro']
    plataforma_venda = request.form['plataforma_venda']
    produto_id=request.form['produto']
    usuario_id = session['usuario_id']

    produto = Produto.query.get(produto_id)

    if (produto.quantidade < int(quantidade)):
        mensagem_erro = 'Venda não concluida,pois restam apenas ' + str(produto.quantidade) + ' unidades disponíveis do produto selecionado'
        return render_template('cadastrar_venda.html', mensagem_erro=mensagem_erro)

        # Se houver erros, permaneça na mesma página
        if mensagem_erro:
            return render_template('formulario.html', mensagem_erro=mensagem_erro)
        return redirect(url_for('criar_venda'))



    nova_venda = Venda(nome_cliente=nome_cliente,
                        data_venda=data_venda,
                        quantidade=quantidade,
                        tipo_entrega=tipo_entrega,
                        valor_entrega=valor_entrega,
                        forma_pagamento=forma_pagamento,
                        valor_venda=valor_bruto,
                        lucro=lucro,
                        plataforma_venda=plataforma_venda,
                        produto_id=produto_id,
                        usuario_id=usuario_id)



    produto.quantidade -= int(quantidade)

    db.session.add(nova_venda)
    db.session.commit()

    upsert_metrica_venda(nova_venda)


    flash('Venda cadastrada com sucesso')

    return redirect(url_for('historico_vendas'))

@app.route('/historico_vendas')
def historico_vendas():
    vendas= Venda.query.filter_by(usuario_id=session['usuario_id']).order_by(Venda.id)

    vendas_lista = []

    for venda in vendas:
        produto_associado = Produto.query.get(venda.produto_id)
        vendas_lista.append((venda, produto_associado.nome+'-'+produto_associado.modelo))

    return render_template('historico_vendas.html', titulo = 'Histórico de vendas', vendas=vendas_lista)

@app.route('/atualizar_venda',methods = ['POST',])
def atualizar_venda():

    venda = Venda.query.filter_by(id=request.form['id']).first()

    produto_antigo = Produto.query.filter_by(id=venda.produto_id).first()
    quantidade_antiga = venda.quantidade

    valor_faturado_antigo = venda.valor_venda
    custo_entrega_antigo = venda.valor_entrega

    venda.nome_cliente = request.form['nome_cliente']
    venda.data_venda = request.form['data_venda']
    venda.quantidade = request.form['quantidade']
    venda.tipo_entrega = request.form['tipo_entrega']
    venda.valor_entrega = request.form['valor_entrega'] if request.form['valor_entrega'] else 0
    venda.forma_pagamento = request.form['forma_pagamento']
    venda.valor_venda = request.form['valor_bruto']
    venda.lucro = request.form['lucro']
    venda.plataforma_venda = request.form['plataforma_venda']
    venda.usuario_id = session['usuario_id']
    if('produto' in request.form):
        venda.produto_id = request.form['produto']
    else:
        venda.produto_id = produto_antigo.id

    produto_novo = Produto.query.filter_by(id=venda.produto_id).first()

    if(produto_novo.quantidade < int(venda.quantidade)):
        flash(f'Atualização de venda não concluida, pois restam apenas {produto_novo.quantidade} unidades disponíveis do produto selecionado')
        return redirect(url_for('historico_vendas'))

    if(venda.produto_id != produto_antigo.id):
        produto_novo.quantidade -= int(venda.quantidade)
        produto_antigo.quantidade += int(quantidade_antiga)

    if(venda.valor_venda != valor_faturado_antigo or venda.valor_entrega != custo_entrega_antigo):
        upsert_metrica_venda_atualiza(venda,valor_faturado_antigo, custo_entrega_antigo)

    db.session.add(venda)
    db.session.commit()

    flash('venda atualizado com sucesso')

    return redirect(url_for('historico_vendas'))

@app.route('/editar_venda/<int:id>')
def editar_venda(id):
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('editar_venda')))

    venda = Venda.query.filter_by(id=id).first()
    produto = Produto.query.filter_by(id=venda.produto_id).first()


    opcoes_produtos = Produto.query.filter(Produto.quantidade>0)
    opcoes_plataforma = ['Facebook','Mercado livre','OLX', 'Shoppee','WhatsApp', 'Outro']
    opcoes_tipo_entrega = ['Retirada', 'Correio', 'Motoboy','Carro','Bicicleta']
    opcoes_forma_pagamento = ['Dinheiro', 'Crédito', 'Débito','Pix']
    return render_template('editar_venda.html',
                           titulo = 'Editar venda',
                           opcoes_produtos = opcoes_produtos,
                           opcoes_plataforma = opcoes_plataforma,
                           opcoes_tipo_entrega = opcoes_tipo_entrega,
                           opcoes_forma_pagamento=opcoes_forma_pagamento,
                           venda = venda,
                           produto = produto)


@app.route('/deletar_venda/<int:id>')
def deletar_venda(id):
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login'))

    venda_deletada = Venda.query.filter_by(id=id).first()
    produto = Produto.query.filter_by(id=venda_deletada.produto_id).first()
    produto.quantidade += venda_deletada.quantidade
    venda = Venda.query.filter_by(id=id).delete()
    upsert_metrica_venda_deletada(venda_deletada)
    db.session.add(produto)
    db.session.commit()
    flash('Venda deletado com sucesso')

    return redirect(url_for('historico_vendas'))

""""--------------------------------------------------metrica--------------------------------------------------------"""

def upsert_metrica_venda(venda):

    mes = venda.data_venda.month
    ano = venda.data_venda.year

    metrica = Metrica.query.filter_by(mes=mes,ano=ano).first()

    if(metrica):
        metrica.custo_entrega += venda.valor_entrega
        metrica.faturamento += venda.valor_venda
        metrica.lucro += venda.valor_venda
    else:
        metrica = Metrica(mes=mes,
                           ano=ano,
                           custo_entrega=venda.valor_entrega,
                           valor_investido = 0,
                           faturamento=venda.valor_venda,
                           lucro=venda.valor_venda,
                           usuario_id=session['usuario_id'])

    db.session.add(metrica)
    db.session.commit()

def upsert_metrica_venda_atualiza(venda, valor_antigo,custo_entrega_antigo):

    data_venda = datetime.strptime(venda.data_venda, '%Y-%m-%d')
    mes = data_venda.month
    ano = data_venda.year

    metrica = Metrica.query.filter_by(mes=mes, ano=ano).first()

    if (not metrica): return;

    metrica.custo_entrega -= custo_entrega_antigo
    metrica.custo_entrega += float(venda.valor_entrega)
    metrica.faturamento -= valor_antigo
    metrica.faturamento += float(venda.valor_venda)
    metrica.lucro += metrica.faturamento

    db.session.add(metrica)
    db.session.commit()

def upsert_metrica_venda_deletada(venda_deletada):
    mes = venda_deletada.data_venda.month
    ano = venda_deletada.data_venda.year

    metrica = Metrica.query.filter_by(mes=mes, ano=ano).first()

    if (not metrica): return;

    metrica.custo_entrega -= venda_deletada.valor_entrega
    metrica.faturamento -= venda_deletada.valor_venda
    metrica.lucro -= venda_deletada.valor_venda

    db.session.add(metrica)
    db.session.commit()



def upsert_metrica_compra(produto):

    mes = produto.data_compra.month
    ano = produto.data_compra.year

    metrica = Metrica.query.filter_by(mes=mes,ano=ano).first()

    if(metrica):
        metrica.valor_investido += produto.custo_compra * produto.quantidade
        metrica.lucro =  metrica.faturamento - metrica.valor_investido
    else:
        metrica = Metrica(mes=mes,
                           ano=ano,
                           valor_investido=produto.custo_compra*produto.quantidade,
                           custo_entrega = 0,
                           faturamento=0,
                           lucro=-(produto.custo_compra * produto.quantidade),
                           usuario_id=session['usuario_id'])

    db.session.add(metrica)
    db.session.commit()

def upsert_metrica_compra_atualiza(produto, quantidade_antiga,custo_produto_antigo):
    mes = produto.data_compra.month
    ano = produto.data_compra.year

    custo_antigo = quantidade_antiga * custo_produto_antigo

    metrica = Metrica.query.filter_by(mes=mes, ano=ano).first()

    if(not metrica): return;

    metrica.valor_investido -= custo_antigo
    metrica.valor_investido += produto.custo_compra * produto.quantidade
    metrica.lucro = metrica.faturamento - metrica.valor_investido

    db.session.add(metrica)
    db.session.commit()

def upsert_metrica_compra_deletada(produto_deletado):
    mes = produto_deletado.data_compra.month
    ano = produto_deletado.data_compra.year

    metrica = Metrica.query.filter_by(mes=mes, ano=ano).first()

    if (not metrica): return;

    metrica.valor_investido -= produto_deletado.custo_compra * produto_deletado.quantidade
    metrica.lucro = metrica.faturamento - metrica.valor_investido

    db.session.add(metrica)
    db.session.commit()


@app.route('/deletar_metrica/<int:id>')
def deletar_metrica(id):
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login'))

    metrica = Metrica.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Métrica deletada com sucesso')

    return redirect(url_for('visualizar_metricas'))

@app.route('/visualizar_metricas')
def visualizar_metricas():
    metricas_lista = Metrica.query.filter_by(usuario_id=session['usuario_id']).order_by(Metrica.id)
    return render_template('visualizar_metricas.html', titulo = 'Fechamento do mês', metricas = metricas_lista)