from unittest import TestCase

from carl import db
from carl.db import Recipe
from mock import Mock, MagicMock


class TestDb(TestCase):
    def setUp(self):
        self.recipe = Recipe("title", "description")

    def test_add_recipe(self):
        mock_db = Mock()
        cursor = Mock()
        mock_db.cursor = MagicMock(return_value=cursor)
        db.add_recipe(mock_db, self.recipe)
        cursor.execute.assert_called_with('insert into recipes (title, description) values (%s, %s)',
                                          ['title', 'description'])
        mock_db.commit.assert_called_with()
