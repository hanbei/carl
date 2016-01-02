from flask import session
from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()


@nav.navigation()
def top_bar():
    navbar = Navbar('Carl', View('Random', 'random_recipe'), View('List', 'list_recipes'), View('Login', 'login'))
    if session.get('logged_in'):
        return Navbar('Carl', View('Random', 'random_recipe'), View('List', 'list_recipes'), View('Logout', 'logout'))
    else:
        return navbar
