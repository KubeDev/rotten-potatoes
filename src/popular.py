import yaml
from models.filme import Filme
import time
import random

def popular():

    n = random.randint(0,5)
    time.sleep(n/10)
    if not len(Filme.objects) > 0:
        with open('movies.yaml') as arquivo:
            documento = yaml.full_load(arquivo)

            for item, doc in documento.items():       
                for item_filme in doc:
                    filme = Filme(titulo=item_filme['titulo'],
                                resumo=item_filme['resumo'],
                                duracao=item_filme['duracao'],
                                lancamento=item_filme['lancamento'],
                                categoria=item_filme['categoria'],
                                elenco=item_filme['elenco'],
                                slide=item_filme['slide'],
                                thumb=item_filme['thumb'])
                    
                    filme.save()
                    
            arquivo.close() 