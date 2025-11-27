import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def conectar_mongo():
    try:
        uri = st.secrets["uri"]
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Pinged. Conexão bem-sucedida!")
        db = client["cadastro_aluno"]
        collection = db["aluno"]
        return collection
    except Exception as e:
        print(e)
        return None

def inserir_aluno(nome, idade, telefone, email, cpf):
    collection = conectar_mongo()
    if collection is not None:
        doc = {
            "nome": nome,
            "idade": idade,
            "telefone": telefone,
            "email": email,
            "cpf": cpf
        }
        collection.insert_one(doc)

def inserir_aluno_menor(nome, idade, responsavel, telefone_responsavel, email_responsavel, cpf_responsavel):
    collection = conectar_mongo()
    if collection is not None:
        doc = {
            "nome": nome,
            "idade": idade,
            "responsavel": responsavel,
            "telefone_responsavel": telefone_responsavel,
            "email_responsavel": email_responsavel,
            "cpf_responsavel": cpf_responsavel
        }
        collection.insert_one(doc)