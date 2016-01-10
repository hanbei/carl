# -*- coding: utf-8 -*-
from carl import db as sql_db


def list_recipes():
    return Recipe.query.all()


def add_recipe(recipe):
    sql_db.session.add(recipe)
    sql_db.session.commit()


def update_recipe(recipe):
    old_recipe = Recipe.query.get(recipe.id)
    old_recipe.title = recipe.title
    old_recipe.description = recipe.description
    sql_db.session.commit()
    return old_recipe


def get_recipe(id):
    return Recipe.query.get(id)


def delete_recipe(id):
    recipe = get_recipe(id)
    sql_db.session.delete(recipe)
    sql_db.session.commit()


class Recipe(sql_db.Model):
    __tablename__ = 'recipes'
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    title = sql_db.Column(sql_db.String(80), unique=True)
    description = sql_db.Column(sql_db.String(120), unique=True)

    def __init__(self, title, description, id=None):
        self.title = title
        self.description = description
        self.id = id

    def __repr__(self):
        return '<Recipe %r>' % self.title
