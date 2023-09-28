from stock_master_control import db

class Produto(db.Model):
    def __repr__(self):
        return '<Name %r>' % self.nome

class Usuario(db.Model):

    def __repr__(self):
        return '<nome %r>' % self.nome

class Venda(db.Model):

    def __repr__(self):
        return '<nome %r>' % self.nome

class Metrica(db.Model):

    def __repr__(self):
        return '<nome %r>' % self.nome


