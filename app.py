import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ps4')
def ps4():
    return render_template('ps4.html',
                           playstation4=mongo.db.playstation4.find())


@app.route('/xbox')
def xbox():
    return render_template('xbox.html',
                           xbox=mongo.db.xbox.find())


@app.route('/nintendo')
def nintendo():
    return render_template('nintendo.html',
                           nintendo=mongo.db.nintendo.find())


@app.route('/pc')
def pc():
    return render_template('pc.html',
                           pc=mongo.db.pc.find())


@app.route('/suggested')
def suggested():
    return render_template('suggested.html',
                           suggested=mongo.db.suggested.find())


@app.route('/add_game')
def add_game():
    return render_template('add_game.html',
                            genre=mongo.db.genre.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
