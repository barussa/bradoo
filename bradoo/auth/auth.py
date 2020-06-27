import functools

from flask import Blueprint, redirect, request, session

auth = Blueprint("auth",__name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):        
        if not "nome" in session.keys():
            return redirect("/login")
        return view(**kwargs)
    return wrapped_view

@auth.route('/login',)
def login():
    try:
        username = request.args['username']
        password = request.args['password']
    except Exception as e:
        print(e)
        return "Passe o username e o password na query string ex: ?username=alisson&password=12345"
    if username != 'alisson' and password != '12345':
        return 'Incorrect username.'                    

    session['nome'] = username
    return "usuario logado: %s"%session['nome']

@auth.route('/logout')
def logout():
    session.clear()
    return "deslogado"