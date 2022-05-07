"""

feito por Henrique (github.com/henriquelmeeee)
abril de 2022

"""

from flask import Flask, render_template, url_for, redirect, request, session
from flaskext.mysql import MySQL
import os
from datetime import datetime

template_dir = os.path.abspath('.')
static_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = "YAS5453278FDSHDWE456"
import mysql.connector
from mysql.connector import Error
cursor = None
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'api'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user text, password text, token text, premium text);")

def checar_autenticacao():
    if "user" in session:
        cursor.execute("SELECT token FROM users WHERE user='"+str(str(session["user"]))+"';")
        token = cursor.fetchall()
        if str(token) == '[]':
            return False
        else:
            return True
    else:
        return False

@app.route('/')
def home():
    return redirect(url_for('explore'))

@app.route('/explore/')
def explore():
    return render_template('explore.html')

@app.route('/v1/auth/login/')
def autenticar():
    if checar_autenticacao():
        return 'a' # redirecionar para a home ou para o q tem nos args do request
    else:
        return render_template('./v1/auth/login/index.html')


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
            today = datetime.now()
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

###

# Aqui fazer um sistema onde você pode pegar um link gerado e colocar ele no Gitea
# tipo em um README.md de um repositório
# como vai ficar no README, ele vai fazer um request pro link gerado, e no banco de dados vai atualizar
# e adicionar uma visualização
# e lá no README do repositório vai mostrar as visualizações

# colocar essa API na parte do /explore, explicando detalhadamente como funciona

@app.route('/v1/web/gitea/views')
def views_gitea():
    try:
        id_view = int(request.args.get('id'))
    except:
        return 'ID inválido', 400
    else:
        print(id_view)
        # continuar

###

@app.route('/v1/web/create/gitea/', methods=["POST"])
def criar_gitea():
    content = request.json
    cursor.execute(f"SELECT user FROM users WHERE token='{str(content['token'])}';")
    token = cursor.fetchall()
    if str(token) != '()':
        cursor.execute(f"SELECT gitea FROM web WHERE token='{str(content['token'])}';")
        gitea = cursor.fetchall()
        if str(gitea) == '()':
            pass
        else:
            return 'Você já tem este website', 406
    else:
        return 'Token incorreto', 401

app.run(host='0.0.0.0', port=33, debug=True)
