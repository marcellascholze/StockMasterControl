from stock_master_control import db

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(100))
    data_compra = db.Column(db.Date, nullable=False)
    custo_compra = db.Column(db.Double, nullable=False)
    preco_sugerido = db.Column(db.Double)
    quantidade = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Name %r>' % self.nome

class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<nome %r>' % self.nome

class Venda(db.Model):
    __tablename__ = 'Venda'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(50), nullable=False)
    data_venda = db.Column(db.Date, nullable=False)
    produto_id = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo_entrega = db.Column(db.String(50), nullable=False)
    valor_entrega = db.Column(db.Double)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    valor_venda = db.Column(db.Double, nullable=False)
    lucro = db.Column(db.Double, nullable=False)
    plataforma_venda = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<nome %r>' % self.nome_cliente

class Metrica(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    custo_entrega = db.Column(db.Double)
    valor_investido = db.Column(db.Double)
    faturamento = db.Column(db.Double)
    lucro = db.Column(db.Double)
    usuario_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<mes %r>' % self.mes+'/'+self.ano


