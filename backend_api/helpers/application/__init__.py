from flask import Flask
from flask_restful import Api
from config import Config # <-- CORREÇÃO APLICADA AQUI

# Cria a instância da aplicação Flask
app = Flask(__name__)
# Carrega as configurações do ficheiro config.py
app.config.from_object(Config)

# Cria a instância da API
api = Api(app)