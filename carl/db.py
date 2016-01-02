# -*- coding: utf-8 -*-
import psycopg2


def connect(connectString):
    return psycopg2.connect(connectString)


def init_db(app):
    db = connect(app.config['DATABASE_URL'])
    cursor = db.cursor()
    cursor.execute('drop table if exists recipes')
    cursor.execute(
            'create table recipes (id serial primary key, title text not null, description text not null)')
    db.commit()
    cursor.close()
    db.close()


def num_recipes(db):
    db_cursor = db.cursor()
    db_cursor.execute('select * from recipes')
    return len(db_cursor.fetchall())


def get_recipes(db):
    db_cursor = db.cursor()
    db_cursor.execute('select id, title, description from recipes order by id desc')
    recipes = [Recipe(title=row[1], description=row[2], id=row[0]) for row in db_cursor.fetchall()]
    db_cursor.close()
    return recipes


def add_recipe(db, recipe):
    db_cursor = db.cursor()
    db_cursor.execute('insert into recipes (title, description) values (%s, %s)', [recipe.title, recipe._description])
    db.commit()
    db_cursor.close()


def get_recipe(db, id):
    db_cursor = db.cursor()
    db_cursor.execute('select id, title, description from recipes where id=%s', [id])
    recipe = [Recipe(title=row[1], description=row[2], id=row[0]) for row in db_cursor.fetchall()]
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
