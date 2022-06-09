from flask import Flask, render_template, url_for, redirect, request, jsoinfy
from flaskext.mysql import MySQL
import os
from datetime import datetime

import requests, time

template_dir = os.path.abspath('.')
static_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

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

@app.route('/')
def home():
    return render_template('./create.html')

@app.route('/create/gitea/')
def create_gitea():
    return render_template('./static/gitea/form.html')

@app.route('/s/<site_name>/', methods=["GET"])
def view_website(site_name):
    if sql:
        conn = mysql.connect(); cursor = conn.cursor()
        websites = ['wordpress', 'nextcloud']
        valor = '()'
        for s in websites:
            if is_alphanum(str(site_name)):
                cursor.execute(f"SELECT porta FROM {s} WHERE name='{site_name}';")
                var = cursor.fetchall()
                if str(var) != '()':
                    valor = var
                    break
            else:
                return jsonify({"error": "the site name must be alphanumeric only"}), 406
        if not str(valor) == '()':
            porta = str(valor).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
            try:
                r = requests.get(f'http://api.harvicloud.com:{porta}')
            except:
                for s in websites:
                    cursor.execute(f"SELECT id FROM {s} WHERE name='{str(site_name)}'")
                    valor = cursor.fetchall()
                    if not str(valor) == '()':
                        valor = str(valor[0]).replace(')', '').replace('(', '').replace('\'', '').replace(',', '')
                        os.system(f"docker container start {valor}")
                        time.sleep(5)
            return render_template('./static/websee/index.html', porta=porta)
        else:
            return jsonify({"error": "website not found"}), 404
    else:
        return jsonify({"error": "the server was unable to communicate with the database"}), 500

app.run(host='0.0.0.0', port=33, debug=True)
