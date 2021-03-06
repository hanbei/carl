# -*- coding: utf-8 -*-
import random

import carl.db as db
from carl import app
from carl.db import Recipe
from flask import g, render_template, session, request, flash, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


@app.route('/')
def random_recipe():
    recipes = db.list_recipes(g.db)
    random_id = random.randint(0, len(recipes) - 1)
    return render_template('random_recipe.html', recipe=recipes[random_id])


@app.route('/recipe', methods=['GET'])
def list_recipes():
    recipes = db.list_recipes(g.db)
    return render_template('list_recipes.html', recipes=recipes)


@app.route('/recipe', methods=['POST'])
def add_recipe():
    if not session.get('logged_in'):
        abort(401)

    db.add_recipe(g.db, Recipe(request.form['title'], request.form['text']))
    flash('New entry was successfully added')
    return redirect(url_for('list_recipes'))


@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    recipe = db.get_recipe(g.db, id)
    return render_template('show_recipe.html', recipe=recipe)


@app.route('/recipe/<id>', methods=['POST'])
def update_recipe(id):
    if not session.get('logged_in'):
        abort(401)

    recipe = Recipe(request.form['title'], request.form['description'], id)
    db.update_recipe(g.db, recipe)
    return redirect(url_for('list_recipes'))


@app.route('/recipe/<id>/edit', methods=['GET'])
def edit_recipe(id):
    if not session.get('logged_in'):
        abort(401)

    recipe = db.get_recipe(g.db, id)
    return render_template('edit_recipe.html', recipe=recipe)


# --------------------- delete --------------------

@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    if not session.get('lo gged_in'):
        abort(401)

    recipe = db.delete_recipe(g.db, id)
    if recipe:
        flash(str(recipe.id) + ' deleted')
    return redirect(url_for('list_recipes'))


@app.route('/recipe/<id>/delete', methods=['GET'])
def get_delete_recipe(id):
    return delete_recipe(id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('list_recipes'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('list_recipes'))


@app.before_request
def before_request():
    db_url = app.config['DATABASE_URL']
    app.logger.info("Connecting to " + str(db_url))
    g.db = db.connect(db_url)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
