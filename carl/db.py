# -*- coding: utf-8 -*-
import psycopg2
from carl import db


def connect(connectString):
    return psycopg2.connect(connectString)


def list_recipes(db):
    db_cursor = db.cursor()
    db_cursor.execute('select id, title, description from recipes order by id')
    recipes = [Recipe(title=row[1], description=row[2], id=row[0]) for row in db_cursor.fetchall()]
    db_cursor.close()
    return recipes


def add_recipe(db, recipe):
    db_cursor = db.cursor()
    db_cursor.execute('insert into recipes (title, description) values (%s, %s)', [recipe.title, recipe._description])
    db.commit()
    db_cursor.close()


def update_recipe(db, recipe):
    db_cursor = db.cursor()
    db_cursor.execute('update recipes set title=%s, description=%s where id=%s',
                      [recipe.title, recipe._description, recipe.id])
    db.commit()
    db_cursor.close()
    return recipe


def get_recipe(db, id):
    db_cursor = db.cursor()
    db_cursor.execute('select id, title, description from recipes where id=%s', [id])
    recipe = [Recipe(title=row[1], description=row[2], id=row[0]) for row in db_cursor.fetchall()]
    db_cursor.close()
    if len(recipe) > 0:
        return recipe[0]
    else:
        return None


def delete_recipe(db, id):
    db_cursor = db.cursor()
    db_cursor.execute('delete from recipes where id=%s RETURNING *', [id])
    recipe = [Recipe(title=row[1], description=row[2], id=row[0]) for row in db_cursor.fetchall()]
    db.commit()
    db_cursor.close()

    if len(recipe) > 0:
        return recipe[0]
    else:
        return None


class Recipe(object):
    def __init__(self, title, description, id=None):
        self._id = id
        self._title = title
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description


class Recipe2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), unique=True)

    def __init__(self, title, description):
        self._title = title
        self._description = description

    def __repr__(self):
        return '<Recipe %r>' % self.title
