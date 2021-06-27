from mongodb import db

class Filme(db.Document):


    titulo = db.StringField()
    resumo = db.StringField()
    duracao = db.StringField()
    lancamento = db.StringField()
    categoria = db.StringField()
    elenco = db.StringField()
    direcao = db.StringField()
    reviews = db.ListField()
    slide = db.StringField()
    thumb = db.StringField()

    def add_review(self, review):
        self.reviews.append(review)