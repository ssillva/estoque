from app1 import db
from datetime import date
def schema():

    cse_item = db.Table('cse_item',
        db.Column('id_patrimonio', db.Integer, primary_key=True),
        db.Column('data_cadastro', db.Date, nullable=False, default=date.today),
        db.Column('mac', db.String(12), nullable=False, unique=True),
        db.Column('fonte', db.String(80), nullable=False),
        db.Column('volts', db.Integer, nullable=False),
        db.Column('ampere', db.Float(2), nullable=False),
        db.Column('produto_id', db.Integer, db.ForeignKey('sis_produto.id'), nullable=False),
        mariadb_engine = "TokuDB",
        mysql_engine = "TokuDB",
    )
    cse_entrada = db.Table('cse_entrada',
                           db.Column('id_entrada', db.Integer, primary_key=True),
                           db.Column('documento', db.String(45), nullable=False),
                           db.Column('qtd', db.Integer, primary_key=False),
                           db.Column('motivo', db.String(100), nullable=False),
                           db.Column('origem', db.String(80), nullable=False),
                           db.Column('obs_entrada', db.String(455), nullable=False),
                           db.Column('user_id', db.Integer, db.ForeignKey('sis_acesso.idacesso'), nullable=False),
                           mariadb_engine="TokuDB",
                           mysql_engine="TokuDB",
                           )
    cse_saida = db.Table('cse_saida',
                         db.Column('id_saida', db.Integer, primary_key=True),
                         db.Column('qtd', db.Integer, primary_key=False),
                         db.Column('motivo', db.String(100), nullable=False),
                         db.Column('destino', db.String(80), nullable=False),
                         db.Column('obs_entrada', db.String(455), nullable=False),
                         db.Column('user_id', db.Integer, db.ForeignKey('sis_acesso.idacesso'), nullable=False),
                         mariadb_engine="TokuDB",
                         mysql_engine="TokuDB",
                         )

    cse_entradahist = db.Table('cse_entradahist',
                               db.Column('data_entrada', db.Date, nullable=False, default=date.today),
                               db.Column('entrada_id', db.Integer, db.ForeignKey('cse_entrada.id_entrada'),
                                         primary_key=True),
                               db.Column('item_id', db.Integer, db.ForeignKey('sis_item.id_patrimonio'),
                                         primary_key=True),
                               mariadb_engine="TokuDB",
                               mysql_engine="TokuDB",
                               )
    cse_saidahist = db.Table('cse_saidahist',
                             db.Column('data_saida', db.Date, nullable=False, default=date.today),
                             db.Column('saida_id', db.Integer, db.ForeignKey('cse_saida.id_saida'), primary_key=True),
                             db.Column('item_id', db.Integer, db.ForeignKey('sis_item.id_patrimonio'),
                                       primary_key=True),
                             mariadb_engine="TokuDB",
                             mysql_engine="TokuDB",
                             )