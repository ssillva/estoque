class Itens(db.Model):
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