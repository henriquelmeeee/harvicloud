"""
---------------------------------------------
feito por Henrique (github.com/henriquelmeeee)
abril de 2022
---------------------------------------------
"""

from flask import Flask, render_template, url_for, redirect, request, session, jsonify
from flaskext.mysql import MySQL
import os, random, subprocess, platform
from datetime import datetime

from config import *
os.system('rm -rf ./__pycache__')

template_dir = os.path.abspath('.')
static_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = APP_SECRET_KEY
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
    cursor.execute("CREATE TABLE IF NOT EXISTS wordpress (user text, id text, porta text, name text, online text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS nextcloud (user text, id text, porta text, name text, online text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS bots (user text, id text, name text, main_file text, online text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS valid_tokens (token text, user text)")

except Exception as error:
    sql = False; print('---\nErro SQL: ' + str(error) + '\n---')

def is_alphanum(text):
    is_alphanum = True
    valores = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
        '4', '5', '6', '7', '8', '9'
        ]
    for s in str(text):
        if not str(s) in valores:
            is_alphanum = False
    if is_alphanum:
        return True
    else:
        return False

def generate_nonce(caracteres):
    nonce = ''
    for s in range (0, caracteres):
        valor = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        if random.randint(1, 3) == 1:
            valor = valor.upper()
        nonce += valor
    return nonce

def capture_number_of_users():
    if sql:
        cursor.execute("SELECT user FROM users"); v = cursor.fetchall(); n = 0
        while True:
            try:
                cursor.fetchall()[n]
            except:
                return n 
            n += 1
    return 'mysql is off'

def capture_mysql_version():
    cursor.execute("SELECT VERSION();")
    mysql_version = str(cursor.fetchall()[0]).replace('\'', '').replace(',)', '').replace('(', '')
    return mysql_version

@app.route('/')
def home():
    return redirect('http://harvicloud.com/')

@app.route('/v1/status/', methods=["GET"])
def server_status():
    return jsonify(
        {
            "mysql": "healthy" if sql else "off",
            "mysql-version": capture_mysql_version() if sql else "mysql is off",
            "registered-users": capture_number_of_users(),
            "online-time": str(datetime.now() - started),
            "os": str(platform.system() + '-' + platform.release())
        }
    )

@app.route('/v1/auth/login/', methods=["POST", "GET"])
def autenticar():
    if sql:
        conn = mysql.connect(); cursor = conn.cursor()
        if not "user" in session:
            content = request.json; user=str(content["user"]); password=str(content["password"])
            if is_alphanum(user) and is_alphanum(password):
                cursor.execute(f"SELECT token FROM users WHERE user='{user}' AND password='{password}'")
                token = cursor.fetchall()
                if str(token) == '()':
                    return jsonify({"error": "invalid credentials"}), 401
                else:
                    session["user"] = user
                    return jsonify({"status": "success", "message": "successfully authenticated"})
            else:
                return jsonify({"error": "credentials must be alphanumeric"}), 202
        else:
            return jsonify({"error": "you are already authenticated"})
    else:
        return jsonify({"error": "the server was unable to communicate with the database"}), 500

@app.route('/v1/users/change/', methods=["POST"])
def user_change():
    content = request.json; to_change = content["change"]
    if to_change == 'icon':
        if "user" in session:
            pass 
        else:
            return jsonify({"error": "unauthenticated user"}), 401
    else:
        return jsonify({"error": "invalid change type"}), 400

###

websites = ['nextcloud', 'wordpress']

def check_website_name(websites, website_name):
    for s in websites:
        cursor.execute(f"SELECT name FROM {s} WHERE name='{str(website_name)}'")
        valor = str(cursor.fetchall())
        if not str(valor) == '':
            return False
    return True

def check_ports():
    porta = 0
    while True:
        ids = ['wordpress', 'nextcloud']
        porta = random.randint(81, 60000)
        n = 0
        wordpress_sites = []; nextcloud_sites = []
        for name in ids:
            n += 1
            if n == 1500:
                return '1'
            else:
                cursor.execute(f"SELECT porta FROM {name} WHERE porta='{porta}' AND user='"+str(session["user"])+"';")
                valor = cursor.fetchall()
                if name == 'wordpress':
                    wordpress_sites = valor
                elif name == 'nextcloud':
                    nextcloud_sites = valor
                    if str(valor) == '()' and n == len(ids):
                        break
                    else:
                        continue
    cursor.execute(f"SELECT plano FROM users WHERE user='{str(session['user'])}'")
    plano = cursor.fetchall()
    total = len(gitea_sites) + len(nextcloud_sites)
    if 'free' in plano and total > 0 or 'profissional' in plano and total > 1 or 'empreendedor' in plano and total > 4:
        return '2'
    if porta == '443' or porta == '80' or porta == '3306':
        return '1'
    return porta

def check_id(id_site):
    nonce = '-'
    for n in range(0, 7):
        nonce += random.choice(["_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
    while True:
        id_container = random.randint(10, 100000)
        cursor.execute(f"SELECT id FROM {id_site} WHERE id='{id_container + nonce}'")
        valor = cursor.fetchall()
        if str(valor) == '()':
            return id_container + nonce
        else:
            continue
    return False

def create_website_commands(id_site, id_container, porta, website_name):
    try:
        os.system(f'mkdir ./v1/containers/web/data/{id_site}/{id_container + valor}')
        if id_site == 'nextcloud':
            os.system(f'docker container run --name {id_container} -v {os.getcwd()}/v1/containers/web/data/nextcloud/{id_container + valor}:/var/www/html --memory="110m" --memory-reservation="100m" --memory-swap="200m" --cpus="1" --restart=on-failure:10 --security-opt no-new-privileges -d -p {porta}:80 nextcloud')
        elif id_site == 'wordpress':
            os.system(f'docker container run --name {id_container} -v {os.getcwd()}/v1/containers/web/data/wordpress/{id_container + valor}:/data --memory="160m" --memory-reservation="150m" --memory-swap="200m" --cpus="1" --restart=on-failure:10 --security-opt no-new-privileges -d -p {porta}:3000 wordpress')
        id_container = subprocess.check_output(f"docker ps -aqf \"name={id_container}\"", shell=True)
        id_container = str(id_container).replace('b', '').replace('\\n', '').replace('\'', '')
        cursor.execute(f"INSERT INTO {id_site} VALUES ('{str(session['user'])}', '{id_container}', '{porta}', '{website_name}', 'true')")
        conn.commit()
        return True
    except:
        return False

@app.route('/v1/web/create/', methods=["POST"])
def create_website():
    if not "user" in session:
        return jsonify({"error": "you need to authenticate"}), 401
    if sql:
        content = request.json
        conn = mysql.connect(); cursor = conn.cursor()
        id_site = content["id"]
        if id_site == 'nextcloud' or id_site == 'wordpress':
            website_name = content['website_name']
            if website_name is None or len(website_name) > 18 or website_name == '':
                return jsonify({"error": "invalid website name"})
            else:
                if is_alphanum(str(website_name)):
                    if check_website_name(websites=websites, website_name=website_name):
                        if "user" in session:
                            id_container = check_id(); porta = check_ports()
                            if not porta == '1' and not porta == '2' and id_container != False:
                                if create_website_commands(id_site, id_container, porta, website_name):
                                    return jsonify({"status": "request accepted successfully"})
                                else:
                                    return jsonify({"error": "an error has occurred, please try again"})
                            else:
                                if porta == '1':
                                    return jsonify({"error": "the back end did not find a valid port for your application after several attempts, please try again"}), 500
                                else:
                                    return jsonify({"error": "website limit reached"}), 403
                        else:
                            return redirect('http://harvicloud.com/login/')
                    else:
                        return jsonify({"error": "there is already a website with this name"}), 406
                else:
                    return jsonify({"error": "invalid site name, it needs to be alphanumeric"}), 406
        else:
            return jsonify({"error": "invalid website type"}), 400
    else:
        return jsonify({"error": "the server was unable to communicate with the database"}), 500

###

def check_bot_name(bot_name):
    cursor.execute(f"SELECT name FROM bots WHERE name='{bot_name}'")
    if str(cursor.fetchall()) == '()':
        return True
    return False

def check_user_bot_create():
    cursor.execute(f"SELECT plano FROM users WHERE user='{session['user']}'")
    plano = cursor.fetchall()[0]; bots = 0
    cursor.execute(f"SELECT name FROM bots WHERE user='{session['user']}'")
    while True:
        try:
            cursor.fetchall()[bots]
        except:
            break
        else:
            bots += 1
    if 'free' in plano and bots > 0 or 'profissional' in plano and bots > 1 or 'empreendedor' in plano and bots > 4:
        return False
    return True

@app.route('/v1/bot/create/', methods=["POST"])
def create_bot():
    if sql:
        content = request.json
        conn = mysql.connect(); cursor = conn.cursor()
        bot_name = content["bot_name"]
        main_file = content["main_file"]
        if bot_name is None or main_file is None:
            return jsonify({"error": "bad request"}), 400
        if "user" in session:
            if is_alphanum(bot_name) and check_bot_name(bot_name):
                if check_user_bot_create():
                    os.system(f'docker container run --name bot_{bot_name} -v {os.getcwd()}/v1/containers/bot/data/{bot_name}/:/data --memory="160m" --memory-reservation="150m" --memory-swap="200m" --cpus="1" --restart=on-failure:10 --security-opt no-new-privileges -d ubuntu')
                    id_container = subprocess.check_output(f"docker ps -aqf \"name={bot_name}\"", shell=True)
                    id_container = str(id_container).replace('b', '').replace('\\n', '').replace('\'', '')
                    cursor.execute(f"INSERT INTO bots VALUES ('{str(session['user'])}', '{id_container}', '{bot_name}', '{main_file}', 'true')")
                    conn.commit()
                    return jsonify({"status": "bot container created successfully"})
                else:
                    return jsonify({"error": "bot limit reached"}), 403
            else:
                return jsonify({"error": "invalid bot name"})
        else:
            return jsonify({"error": "you need to authenticate"}), 401
    else:
        return jsonify({"error": "the server was unable to communicate with the database"}), 500

def validate_file(filename):
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/v1/bot/upload-files/', methods=["POST"])
def bot_upload_files():
    content = request.json
    if sql:
        if "id" in content:
            if 'file' not in request.files:
                return jsonify({"error": "no files were sent"}), 400
            else:
                cursor.execute(f"SELECT id FROM bots WHERE id='{content['id']}'")
                if len(cursor.fetchall()) == 0:
                    return jsonify({"error": "container ID not found in database"})
                else:
                    f = request.files["file"]
                    if f.filename == '':
                        return jsonify({"error": "invalid file name"}), 400
                    else:
                        if f and allowed_file(f.filename):
                            filename = secure_filename(f.filename)
                            f.save(os.path.join(f'./v1/containers/discord/bot/data/{content["id"]}/', name=filename))
                            return jsonify({"status": "file saved successfully"})
        else:
            return jsonify({"error": "container ID not specified"})
    else:
        return jsonify({"error": "the server was unable to communicate with the database"}), 500

maintenance = True

@app.before_request
def before_request():
    method = request.method 
    path = request.path 
    if maintenance:
        if not session.get("maintenance"):
            if path == "/(pass)":
                session["maintenance"] = "true"
            else:
                return 'Autentique-se primeiro!'

started = datetime.now()
app.run(host='0.0.0.0', port=9000)
