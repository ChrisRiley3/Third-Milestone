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


# This will render the index page first
@app.route('/')
def index():
    return render_template('index.html')


# This will go through my mongodb and find the ps4 data then display it on the ps4.html page
@app.route('/ps4')
def ps4():
    return render_template('ps4.html',
                           playstation4=mongo.db.playstation4.find())


# This will go through my mongodb and find the xbox data then display it on the xbox.html page
@app.route('/xbox')
def xbox():
    return render_template('xbox.html',
                           xbox=mongo.db.xbox.find())


# This will go through my mongodb and find the nintendo data then display it on the nintendo.html page
@app.route('/nintendo')
def nintendo():
    return render_template('nintendo.html',
                           nintendo=mongo.db.nintendo.find())


# This will go through my mongodb and find the pc data then display it on the pc.html page
@app.route('/pc')
def pc():
    return render_template('pc.html',
                           pc=mongo.db.pc.find())


# This will go through my mongodb and find the suggested data then display it on the suggested.html page
@app.route('/suggested')
def suggested():
    vals = list(mongo.db.suggested.find())
    for v in vals:
        v['html_game_id'] = v['game_title'].replace(" ", "")
    print(update_game)
    return render_template('suggested.html',
                           suggested=vals)


# This will go through my mongodb and find the genre data then display it on the add_game.html page
@app.route('/add_game')
def add_game():
    return render_template('add_game.html',
                           genre=mongo.db.genre.find())


# This will allow the user to insert a game suggestion when they click the submit button
@app.route('/insert_game', methods=['POST'])
def insert_game():
    suggested = mongo.db.suggested
    suggested.insert_one(request.form.to_dict())
    return redirect(url_for('suggested'))


# This will allow the user to edit a game suggestion
@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.suggested.find_one({"_id": ObjectId(game_id)})
    all_genres = mongo.db.genre.find()
    print(edit_game)
    return render_template('edit_game.html', game=the_game,
                           genre=all_genres)


# This will allow the previous suggestion to be edited and not post a new suggestion
@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    suggested = mongo.db.suggested
    suggested.update({'_id': ObjectId(game_id)},
                     {
                     'game_genre': request.form.get('game_genre'),
                     'first_name': request.form.get('first_name'),
                     'last_name': request.form.get('last_name'),
                     'game_title': request.form.get('game_title'),
                     'game_description': request.form.get('game_description')
                     })
    return redirect(url_for('suggested'))


# This will allow the user to delete their suggestion
@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    mongo.db.suggested.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('suggested'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
