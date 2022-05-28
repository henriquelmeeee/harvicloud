"""
---------------------------------------------
feito por Henrique (github.com/henriquelmeeee)
abril de 2022
---------------------------------------------
"""

from flask import Flask, render_template, url_for, redirect, request, session
from flaskext.mysql import MySQL
import os, random
from datetime import datetime

import subprocess

template_dir = os.path.abspath('.')
static_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = "secret_key_here"

import mysql.connector
from mysql.connector import Error
cursor = None
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'db'
app.config['MYSQL_DATABASE_HOST'] = 'host'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user text, password text, token text, plano text);")
cursor.execute("CREATE TABLE IF NOT EXISTS gitea (user text, id text, porta text, name text, online text)")
cursor.execute("CREATE TABLE IF NOT EXISTS nextcloud (user text, id text, porta text, name text, online text)")

def turn_on_containers():
    pass
    # Em produção...
turn_on_containers()

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
        
@app.route('/')
def home():
    return redirect(url_for('explore'))

@app.route('/explore/')
def explore():
    return render_template('explore.html')

@app.route('/v1/auth/login/', methods=["POST"])
def autenticar():
    if not "user" in session:
        content = request.json; user=str(content["user"]); password=str(content["password"])
        if is_alphanum(user) and is_alphanum(password):
            cursor.execute(f"SELECT token FROM users WHERE user='{user}' AND password='{password}'")
            token = cursor.fetchall()
            if str(token) == '()':
                return 401
            else:
                session["user"] = user
                return 200
        else:
            return 202
    else:
        return False


def discord_send_log(mensagem):
    # tem que checar se existe a pasta do ano, do mes e o txt do dia
    today = datetime.now()
    file = open(f'./v1/logs/{today.year}/{today.month}/discord/{str(today.day)}.txt', "a")
    file.write(f'{mensagem}')
    file.write('\n')
    file.close()

# Sistema de envio de logs do bot do Discord
# a key secret é a senha que o bot do Discord usa para se identificar e poder enviar o post
# a key mensagem é a mensagem da log

@app.route('/v1/logs/discord/send', methods=["POST"])
def send_log():
    if request.method == 'POST':
        content = request.json
        if str(content["secret"]) == 'ASKOGSDITR574569JFG6':
            discord_send_log(
                mensagem=str(content["mensagem"]), 
                )
            return ''
        else:
            return 'Não autorizado', 401


os.system('rm ./v1/discord/bot/logs/logs.txt'); os.system('touch ./v1/discord/bot/logs/logs.txt')
@app.route('/v1/discord/get/logs/', methods=["GET", "POST"])
def logs():
    if request.method == 'POST':
        content = request.json
        if not str(content["secret"]) == 'ASKOGSDITR574569JFG6':
            return 'Não autorizado', 401
        else:
            logs = str(content["logs"])
            f = open('./v1/discord/bot/logs/logs.txt', "a")
            f.write(logs + '\n')
            f.close()
            return 'Logs enviadas com sucesso', 200
    else:
        if "user" in session and not str(session["user"]) == 'henrique': 
            return 'Não autorizado', 403
        elif not "user" in session:
            return 'Não autorizado', 401
        else:
            return render_template('./v1/discord/bot/logs/index.html', log="a")

# Aqui o usuário poderá pegar seu token de autenticação
# é usado para se autenticar no bot do Discord

import secrets
@app.route('/v1/auth/token/', methods=['GET'])
def gerar_token():
    if not checar_autenticacao():
        return redirect(f'http://harvicloud.com/login?redirect=/token')
    else:
        # Pedir para colocar a senha antes de mandar o token
        token = str(secrets.token_hex())
        return token

# Sistema de validação de Token
# Cada usuário tem um token único, e este sistema é usado pelo bot do Discord
# para validar um token dado pelo usuário
# ele cai em um JSON com 2 keys: secret e token
# a secret é uma key com uma senha para poder usar este sistema
# e o token é onde coloca o valor do token

@app.route('/v1/auth/token/validate', methods=['POST'])
def validar_token():
    if request.method == "POST":
        content = request.json
        if not str(content["secret"]) == 'ASKOGSDITR574569JFG6':
            return 'Não autorizado', 401
        else:
            token = str(content["token"])
            cursor.execute("SELECT token FROM users WHERE token='"+str(token)+"';")
            checar = cursor.fetchall()
            if str(checar) == '()':
                return 'Token incorreto', 401
            else:
                return 'Autorizado', 200

@app.route('/v1/web/gitea/views')
def views_gitea():
    try:
        id_view = int(request.args.get('id'))
    except:
        return 'ID inválido', 400
    else:
        print(id_view)
        # continuar

@app.route('/v1/web/create/<id_site>', methods=["GET"])
def create_website(id_site):
    id_site = str(id_site)
    if id_site == 'nextcloud' or id_site == 'gitea':
        website_name = request.args.get('website_name')
        if website_name is None or len(website_name) > 18 or website_name == '':
            return 'Nome do site inválido'
        else:
            if is_alphanum(str(website_name)):
                if "user" in session:
                    id_container = 0; porta = 0
                    while True:
                        ids = ['gitea', 'nextcloud']
                        porta = random.randint(81, 60000)
                        n = 0
                        gitea_sites = []; nextcloud_sites = []
                        for name in ids:
                            n += 1
                            if n == 1500:
                                return 'Um erro ocorreu, tente novamente', 500
                            else:
                                cursor.execute(f"SELECT porta FROM {name} WHERE porta='{porta}' AND user='"+str(session["user"])+"';")
                                valor = cursor.fetchall()
                                if name == 'gitea':
                                    gitea_sites = valor
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
                            return 'Limite de websites atingido', 403
                        break
                    while True:
                        id_container = random.randint(10, 100000)
                        cursor.execute(f"SELECT id FROM {id_site} WHERE id='{id_container}' AND user='"+str(session["user"])+"';")
                        valor = cursor.fetchall()
                        if str(valor) == '()' and id_container != 443:
                            break
                        else:
                            continue
                    valor = '-'
                    for n in range(0, 7):
                        valor += random.choice(["_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
                    id_container = str(id_container)
                    os.system(f'mkdir ./v1/containers/web/data/{id_site}/{id_container + valor}')
                    if id_site == 'nextcloud':
                        os.system(f'docker container run --name {id_container + valor} -v {os.getcwd()}/v1/containers/web/data/nextcloud/{id_container + valor}:/var/www/html --memory="110m" -d -p {porta}:80 nextcloud')
                    elif id_site == 'gitea':
                        os.system(f'docker container run --name {id_container + valor} -v {os.getcwd()}/v1/containers/web/data/gitea/{id_container + valor}:/data --memory="160m" -d -p {porta}:3000 gitea/gitea')
                    id_container = subprocess.check_output(f"docker ps -aqf \"name={id_container + valor}\"", shell=True)
                    id_container = str(id_container).replace('b', '').replace('\\n', '').replace('\'', '')
                    return id_container
                  # Em produção...
                else:
                    return redirect('http://harvicloud.com/login/')
            else:
                return 'O nome do site deve ser apenas alfanumérico'
    else:
        return redirect('http://harvicloud.com/')

app.run(host='0.0.0.0', port=80, debug=False)
