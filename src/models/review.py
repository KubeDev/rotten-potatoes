from mongodb import db
from datetime import datetime

class Review(db.EmbeddedDocument):

    nome = db.StringField()
    review = db.StringField()
    data_review = db.DateTimeField(default=datetime.now())
