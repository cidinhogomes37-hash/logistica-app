import sqlite3
import streamlit as st

def conectar():
    conn = sqlite3.connect('logistica.db')
    return conn

# Criar tabela se não existir
conn = conectar()
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS entregas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        endereco TEXT,
        status TEXT
    )
''')
conn.commit()
conn.close()

st.title("🚚 Painel de Controle da Logística")
st.write("Sistema rodando com sucesso na nuvem!")
