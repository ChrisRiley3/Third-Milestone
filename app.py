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


@app.route('/insert_game', methods=['POST'])
def insert_game():
    suggested = mongo.db.suggested
    suggested.insert_one(request.form.to_dict())
    return redirect(url_for('suggested'))


@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.suggested.find_one({"_id": ObjectId(game_id)})
    all_genres = mongo.db.genre.find()
    return render_template('edit_game.html', game=the_game,
                           genre=all_genres)


@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    suggested = mongo.db.suggested
    suggested.update({'_id': ObjectId(game_id)},
                     {
                     'first_name': request.form.get('first_name'),
                     'last_name': request.form.get('last_name'),
                     'game_title': request.form.get('game_title'),
                     'game_description': request.form.get('game_description')
                     })
    return redirect(url_for('suggested'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
