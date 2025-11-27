import streamlit as st
from twilio.rest import Client
import random

ACCOUNT_SID = st.secrets["ACCOUNT_SID"]
AUTH_TOKEN = st.secrets["AUTH_TOKEN"]
TWILIO_NUMBER = st.secrets["TWILIO_NUMBER"]
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def enviar_codigo_sms(telefone):
    codigo = random.randint(100000, 999999)
    try:
        client.messages.create(
            body=f"Seu código de verificação é {codigo}",
            from_=TWILIO_NUMBER,
            to=telefone
        )
        st.session_state.codigo_enviado = codigo
        st.success("Enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro: {e}")