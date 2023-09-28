SECRET_KEY= 'stockMasterControl'
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(SGBD = 'mysql+mysqlconnector', usuario = 'root', senha = '0611', servidor = 'localhost', database = 'stockMasterControl')
