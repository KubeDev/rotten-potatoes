from re import A
from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
import os 
from flask_mongoengine import json
from models.review import Review
from mongodb import db
from models.filme import Filme
import bson
from prometheus_flask_exporter import PrometheusMetrics
from middleware import set_unhealth, set_unready_for_seconds, middleware
from datetime import datetime

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.wsgi_app = middleware(app.wsgi_app)

metrics = PrometheusMetrics(app, default_labels={'version': '1.0'})


app.config['MONGODB_DB'] = os.getenv("MONGODB_DB", "admin")
app.config['MONGODB_HOST'] = os.getenv("MONGODB_HOST", "localhost")
app.config['MONGODB_PORT'] = int(os.getenv("MONGODB_PORT", "27017"))
app.config['MONGODB_USERNAME'] = os.getenv("MONGODB_USERNAME", "mongouser")
app.config['MONGODB_PASSWORD'] = os.getenv("MONGODB_PASSWORD", "mongopwd") 

db.init_app(app)  

@app.route('/')
def index():

    filmes = Filme.objects
    app.logger.info('Obtendo a lista de filmes no MongoDB')      
    sliders = sorted(filmes, key=lambda x: len(x.reviews), reverse=False)
    sliders = sliders[-3:]
    return render_template('index.html', filmes=filmes, sliders=sliders)

@app.route('/review')
def review():       
    return render_template('review.html', filmes=Filme.objects)

@app.route('/joinus')
def joinus():
    return render_template('joinus.html')

@app.route('/single/<string:oid>', methods=['GET','POST'])
def single(oid):

    filme = Filme.objects.get(id=bson.objectid.ObjectId(oid))
    filme.reviews = sorted(filme.reviews, key=lambda x: x.data_review, reverse=True)

    if request.method == 'GET':  
        app.logger.info('Entrando na pagina de review do filme %s', filme.titulo)      
        return render_template('single.html', filme = filme)
    else:
        app.logger.info('Efetuando cadastro de review no filme %s', filme.titulo)
        nome = request.form['nome']
        review = request.form['review']  
        o_review = Review(nome=nome, review=review, data_review=datetime.now())        
        filme.add_review(o_review)
        filme.save()
        return redirect(url_for('single', oid=oid))

@app.route('/host')
def host():
    return jsonify({"host": os.uname().nodename})

@app.route('/stress/<int:seconds>')
def stress(seconds):
    #pystress(seconds, 1)
    return Response('OK')

@app.route('/about')
def about():
    return render_template('about.html')  

@app.route('/contact')
def contact():
    return render_template('contact.html')  

@app.route('/unreadyfor/<int:seconds>', methods=['PUT'])
def unready_for(seconds):
    set_unready_for_seconds(seconds)
    return Response('OK')

@app.route('/health', methods=['GET'])
def heath():
    return Response('OK')

@app.route('/unhealth', methods=['PUT'])
def unhealth():
    set_unhealth()
    return Response('OK')
    
@app.route('/ready', methods=['GET'])
def ready():
    return Response('OK')

if __name__ == '__main__':
    app.run()
