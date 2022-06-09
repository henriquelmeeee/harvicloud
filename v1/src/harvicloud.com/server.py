"""
---------------------------------------------
feito por Henrique (github.com/henriquelmeeee)
abril de 2022
---------------------------------------------
"""

from flask import Flask, render_template, url_for, redirect, session, jsonify
import os
from flaskext.mysql import MySQL

template_dir = os.path.abspath('.')
static_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = "YAS5453278FDSHDWE456"

def is_sqli(text):
    # todo
    return False

sql = True
try:

    import mysql.connector
    from mysql.connector import Error
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = DB_USER
    app.config['MYSQL_DATABASE_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DATABASE_DB'] = DB_NAME
    app.config['MYSQL_DATABASE_HOST'] = DB_HOST
    mysql.init_app(app)

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (user text, password text, token text, plano text);")
    cursor.execute("CREATE TABLE IF NOT EXISTS gitea (user text, id text, porta text, name text, online text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS nextcloud (user text, id text, porta text, name text, online text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS bots (user text, id text, name text, main_file text, online text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS valid_tokens (token text, user text)")

except Exception as error:
    sql = False; print('---\nErro SQL: ' + str(error) + '\n---')

@app.route('/')
def home():
    os.system('pwd')
    return render_template('static/index.html')

@app.route('/app/')
def application():
    return redirect(url_for('dashboard'))

@app.route('/app/painel/')
def dashboard():
    session["user"] = 'a'
    if "user" in session:
        return render_template('./static/dashboard/dashboard.html', user=str(session["user"]))
    else:
        return redirect(url_for('home'))

def check_if_app_exists(app_id):
    if not is_sqli(app_id):
        apps = ['wordpress', 'nextcloud', 'bots']
        for app in apps:
            cursor.execute(f"SELECT id FROM {apps} WHERE id='{id_app}'")
            check = cursor.fetchall()
            if not str(check) == '()':
                return False 
        return True
    else:
        return False

@app.route('/app/painel/<id_app>/')
def dashboard_app(id_app):
    if sql:
        if check_if_app_exists(id_app):
            if "user" in session:
                return render_template('./static/dashboard/app/web/dashboard.html',
                    user=str(session["user"]),
                    imagem_user_src='default.png',
                    numero_erros = 5,
                    numero_acessos = 5,
                    email_confirmation = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Você precisa <b>confirmar seu email</b>. <a href="/suporte/confirmar-email/" class="alert-link">Clique aqui</a> para saber como confirmá-lo e desbloquear todos os recursos.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button><div></div><div></div><div></div></div>')
            else:
                return redirect(url_for('home'))
        else:
            return jsonify({"error": "application ID is invalid"}), 400
    else:
        return jsonify({"error": "the server was unable to communicate with the database"}), 500

@app.route('/app/logs/')
def homelogs():
    #todo
    if False:
        pass
    else: #
        return render_template('./static/logs/index.html')

@app.route('/app/logs/<id>')
def getlogs(id):
    # todo
    if False:
        pass
    else:
        return render_template('./static/logs/get.html', id=str(id))

# Termos (todo)

@app.route('/termos-de-servico/')
def redirecionar_termos():
    return redirect(url_for('termospt'))

@app.route('/pt/termos/')
def termospt():
    return render_template('./static/termos/pt/termos.html'), 200

@app.route('/en/termos/')
def termosen():
    return render_template('./static/termos/en/termos.html'), 200

# Planos

@app.route('/planos/')
def planos():
    return render_template('./static/planos.html')

# Autenticação

@app.route('/login/')
def login():
    # todo
    if not "user" in session:
        return render_template('')
    else:
        return redirect(url_for('dashboard'))

app.run(host='0.0.0.0', port=33, debug=True)
