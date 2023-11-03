from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:derly.,.01@localhost:3306/estoque'
    #'sqlite:///estoque.db'
app.config['SECRET_KEY'] = 'secret-key'

db = SQLAlchemy(app)


class Equipamentos(db.Model):
    id_patrimonio = db.Column(db.Integer, primary_key=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    nome = db.Column(db.String(80), nullable=False)
    mac = db.Column(db.String(12), nullable=False)
    fonte = db.Column(db.String(80), nullable=False)
    volts = db.Column(db.Integer, primary_key=False)
    ampere = db.Column(db.Float, primary_key=False)
    categoria = db.Column(db.String(80), nullable=False)

    def __init__(self, nome, mac, fonte, volts, ampere, categoria):
        self.nome = nome
        self.mac = mac
        self.fonte = fonte
        self.volts = volts
        self.ampere = ampere
        self.categoria = categoria

@app.route("/")
def Index():
    all_data = Equipamentos.query.all()
    return render_template("index.html", employees=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        nome = request.form['nome']
        mac = request.form['mac']
        fonte = request.form['fonte']
        volts = request.form['volts']
        ampere = request.form['ampere']
        categoria = request.form['categoria']

        my_data = Equipamentos(nome, mac, fonte, volts, ampere, categoria)

        db.session.add(my_data)
        db.session.commit()

        flash("Item adicionado com sucesso")

        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Equipamentos.query.get(request.form.get('id_patrimonio'))
        my_data.nome = request.form['nome']
        my_data.mac = request.form['mac']
        my_data.fonte = request.form['fonte']
        my_data.volts = request.form['volts']
        my_data.ampere = request.form['ampere']
        my_data.categoria = request.form['categoria']
        db.session.commit()

        flash("Item atualizado com sucesso")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Equipamentos.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Item deletado com sucesso")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)