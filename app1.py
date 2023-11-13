from imp import reload
from sqlalchemy import inspect
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:vertrigo@192.168.1.5/mkradius'

    #'sqlite:///estoque.db'
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


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

class Sis_produto(db.Model):
    __tablename__ = 'sis_produto'
    id = db.Column(db.Integer, primary_key=True)
    fk_id_item = db.relationship('Sis_item', backref='sis_produto', lazy=True)#primaryjoin="Sis_produto.id == Sis_item.produto_id")

    def toDict(self):
	    return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
class Sis_acesso(db.Model):
    __tablename__ = 'sis_acesso'
    idacesso = db.Column(db.Integer, primary_key=True)
    id_user_entrada = db.relationship('Cse_entrada', backref='sis_acesso', lazy=True)#primaryjoin="Sis_produto.id == Sis_item.produto_id")
    id_user_saida = db.relationship('Cse_saida', backref='sis_acesso', lazy=True)

class Sis_item(db.Model):
    __tablename__ = 'sis_item'
    id_patrimonio = db.Column(db.Integer, primary_key=True)
    data_cadastro = db.Column(db.Date, nullable=False, default=date.today)

    mac = db.Column(db.String(12), nullable=False)
    fonte = db.Column(db.String(80), nullable=False)
    volts = db.Column(db.Integer, primary_key=False)
    ampere = db.Column(db.Float(2), primary_key=False)
    cse_entradahist = db.relationship('Cse_entrada', secondary=cse_entradahist, lazy='subquery',
                                      backref=db.backref('sis_item', lazy=True))
    produto_id = db.Column(db.Integer, db.ForeignKey('sis_produto.id'))

    def __init__(self, mac, fonte, volts, ampere, produto_id):

        self.mac = mac
        self.fonte = fonte
        self.volts = volts
        self.ampere = ampere
        self.produto_id = produto_id
    def toDict(self):
	    return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Cse_entrada(db.Model):
    __tablename__ = 'cse_entrada'

    id_entrada = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(45), nullable=False)
    qtd = db.Column(db.Integer, primary_key=False)
    motivo = db.Column(db.String(100), nullable=False)
    origem = db.Column(db.String(80), nullable=False)
    obs_entrada = db.Column(db.String(455), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('sis_acesso.idacesso'))

    def __init__(self, documento, qtd, motivo, origem, obs_entrada, user_id):

        self.documento = documento
        self.qtd = qtd
        self.motivo = motivo
        self.origem = origem
        self.obs_entrada = obs_entrada
        self.user_id = user_id

class Cse_saida (db.Model):
    __tablename__ = 'cse_saida'
    id_saida = db.Column(db.Integer, primary_key=True)
    qtd = db.Column(db.Integer, primary_key=False)
    motivo = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(80), nullable=False),
    obs_saida = db.Column(db.String(455), nullable=False),
    user_id = db.Column(db.Integer, db.ForeignKey('sis_acesso.idacesso'))


"""class Cse_entradahist (db.Model):
    __tablename__ = 'cse_entradahist'
    data_entrada = db.Column(db.Date, nullable=False, default=date.today)
    entrada_id = db.Column(db.Integer, db.ForeignKey('cse_entrada.id_entrada'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('sis_item.id_patrimonio'), primary_key=True)

    def __init__(self, entrada_id, item_id):

        self.entrada_id = entrada_id
        self.item_id = item_id
"""

"""class Cse_saidahist(db.Model):
    __tablename__ = 'cse_saidahist'

    data_saida = db.Column(db.Date, nullable=False, default=date.today)
    saida_id = db.Column(db.Integer, db.ForeignKey('Cse_saida.id_saida'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('sis_item.id_patrimonio'),
                                   primary_key=True)
"""
@app.route("/teste", methods=['GET'])
def Teste():
    all_data = Sis_produto.query.all()
    all_dataArr = []
    for item in all_data:
	    all_dataArr.append(item.toDict())

    return jsonify(all_dataArr)

@app.route("/")
def Index():

    all_data = Sis_item.query.all()
    return render_template("index.html", employees=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        mac = request.form['mac']
        fonte = request.form['fonte']
        volts = request.form['volts']
        ampere = request.form['ampere']

        my_data = Sis_item(mac, fonte, volts, ampere, produto_id)

        db.session.add(my_data)
        db.session.commit()

        flash("Item adicionado com sucesso")

        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Sis_item.query.get(request.form.get('id_patrimonio'))
        my_data.produto_id = request.form['produto_id']
        my_data.mac = request.form['mac']
        my_data.fonte = request.form['fonte']
        my_data.volts = request.form['volts']
        my_data.ampere = request.form['ampere']
        db.session.commit()

        flash("Item atualizado com sucesso")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Sis_item.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Item deletado com sucesso")

    return redirect(url_for('Index'))

@app.route("/entrada")
def entrada():
    all_data = Cse_entrada.query.all()
    return render_template("entrada.html", employees=all_data)
@app.route('/entrada/insert', methods=['POST'])
def insert_entrada():
    if request.method == 'POST':
        documento = request.form['documento']
        qtd = request.form['qtd']
        motivo = request.form['motivo']
        origem = request.form['origem']
        obs_entrada = request.form['obs_entrada']
        user_id = request.form['user_id']
        mov_entrada = request.form['mov_entrada']
        mov_item = request.form['mov_item']

        my_data = Cse_entrada(documento, qtd, motivo, origem, obs_entrada, user_id)

        db.session.add(my_data)
        db.session.commit()

        statement = cse_entradahist.insert().values(entrada_id=mov_entrada, user_id=mov_item)
        db.session.execute(statement)
        db.session.commit()


        flash("Tarefa realizada com sucesso")

        return redirect(url_for('entrada'))

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        #db.create_all()
        db.reflect()
    app.run(debug=True)
    reload(sys)