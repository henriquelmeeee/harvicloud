"""

feito por Henrique (github.com/henriquelmeeee)
abril de 2022

"""

from flask import Flask, render_template, url_for, redirect, request, session
import os
from datetime import datetime

template_dir = os.path.abspath('.')
static_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = "YAS5453278FDSHDWE456"
import mysql.connector
from mysql.connector import Error
cursor = None
try:
    connection = mysql.connector.connect(
        
        host = "localhost",
        database="api",
        user="root",
        password="123"
        
    )
    if connection.is_connected():
        print('---------------------')
        print(f"Conectado no servidor MySQL da API\n{connection.get_server_info()}")
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        print('---------------------')
except Error as e:
    print(f"Ocorreu um erro ao tentar conectar no banco de dados:\n{e}")

cursor.execute("CREATE TABLE IF NOT EXISTS users (user text, password text, token text, premium text);")

def checar_autenticacao():
    if "password" in session and "user" in session:
        user = str(session["user"]); password = str(session["password"])
        cursor.execute("SELECT token FROM users WHERE user='"+str(str(session["user"]))+"' AND password='"+str(str(session["password"]))+"';")
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
    if not checar_autenticacao(): # aqui verificar se quem está tentando acessar já não tem uma sessão logada
        return 'nao autenticado' # caso tenha, renderizar outro template
    else:
        return render_template('./v1/auth/login/index.html')

ip_discord_bot = '' # IP do bot do Discord, só esse IP pode fazer requisições na API em logs/discord

def discord_send_log(tipo_log, user_log, comando):
    # tem que checar se existe a pasta do ano, do mes e o txt do dia
    # e também checar se o IP de quem ta fazendo a requisição é o bot do discord
    today = datetime.now()
    file = open(f'./v1/logs/{today.year}/{today.month}/discord/{str(today.day)}.txt', "a")
    if str(tipo_log) == '1':
        file.write(f'[{datetime.now()}] ERRO: O usuário "{user_log}" executou o comando "{comando}" sem permissões')
    file.write('\n')
    file.close()

@app.route('/v1/logs/discord/send')
def send_log():
    tipo_log = request.args.get('type')
    user_log = request.args.get('user')
    comando = request.args.get('comando')
    today = datetime.now()
    if str(tipo_log) == '1' and comando is None:
        file = open(f'./v1/logs/{today.year}/{today.month}/api/errors.txt', "a")
        file.write(f'[{datetime.now()}] ERRO: Requisição não aceita; Parâmetro "comando" não definido para o tipo "1"\n')
        file.close()
    discord_send_log(
        user_log=str(user_log), 
        tipo_log=str(tipo_log),
        comando=str(comando), 
        )
    return ''
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
        if False: # caso não tenha a senha no corpo do request
            return 'Não autorizado', 401
        else:
            return render_template('./v1/discord/bot/logs/index.html', log="a")

import secrets
@app.route('/v1/auth/token/', methods=['GET'])
def gerar_token():
    if False: # caso o usuário não esteja autenticado no website
        pass # passar para o url de login com o param ?redirect=/v1/auth/token/
    else:
        # Pedir para colocar a senha antes de mandar o token
        token = str(secrets.token_hex())
        return token

@app.route('/v1/auth/token/validate', methods=['GET'])
def validar_token():
    token = request.args.get('token')
    if False: # caso o token não seja associado a nenhum usuario
        return 'Não autorizado', 401
    else:
        return 'Autorizado', 200

app.run(host='0.0.0.0', port=33, debug=True)
