from werkzeug.datastructures import ContentSecurityPolicy
import yaml
from models.filme import Filme
import time
import random
from pymongo import MongoClient
import os

MONGODB_DB = os.getenv("MONGODB_DB", "admin")
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", "27017"))
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "mongouser")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "mongopwd") 

def on_starting(server):    

    CONNECTION_STRING = "mongodb://" + MONGODB_USERNAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOST 

    client = MongoClient(CONNECTION_STRING)

    db = client[MONGODB_DB]
    collection = db["filme"]

    if not collection.find().count() > 0:
        with open('movies.yaml') as arquivo:
            documento = yaml.full_load(arquivo)

            for item, doc in documento.items():       
                for item_filme in doc:


                    filme = { "titulo": item_filme['titulo'],
                                "resumo": item_filme['resumo'],
                                "duracao": item_filme['duracao'],
                                "lancamento": item_filme['lancamento'],
                                "categoria": item_filme['categoria'],
                                "elenco": item_filme['elenco'],
                                "slide": item_filme['slide'],
                                "thumb": item_filme['thumb'] }


                    # filme = Filme(titulo=item_filme['titulo'],
                    #             resumo=item_filme['resumo'],
                    #             duracao=item_filme['duracao'],
                    #             lancamento=item_filme['lancamento'],
                    #             categoria=item_filme['categoria'],
                    #             elenco=item_filme['elenco'],
                    #             slide=item_filme['slide'],
                    #             thumb=item_filme['thumb'])
                    
                    collection.insert_one(filme)
                    
            arquivo.close() 