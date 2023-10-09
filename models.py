from stock_master_control import db

"""class Produto(db.Model):
    def __repr__(self):
        return '<Name %r>' % self.nome"""

class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<nome %r>' % self.nome

"""class Venda(db.Model):

    def __repr__(self):
        return '<nome %r>' % self.nome

class Metrica(db.Model):

    def __repr__(self):
        return '<nome %r>' % self.nome"""


