import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel de Logística", layout="wide")

# Conexão com o banco SQLite
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

# Formulário para cadastrar novas entregas
with st.sidebar:
    st.header("Cadastrar Nova Entrega")
    cliente = st.text_input("Nome do Cliente")
    endereco = st.text_input("Endereço de Entrega")
    status = st.selectbox("Status", ["Pendente", "Em Trânsito", "Entregue"])
    
    if st.button("Salvar Entrega"):
        if cliente and endereco:
            conn = conectar()
            c = conn.cursor()
            c.execute("INSERT INTO entregas (cliente, endereco, status) VALUES (?, ?, ?)", (cliente, endereco, status))
            conn.commit()
            conn.close()
            st.success("Entrega cadastrada com sucesso!")
            st.rerun()
        else:
            st.warning("Preencha todos os campos!")

# Exibição dos dados
st.subheader("Entregas Cadastradas")
conn = conectar()
df = pd.read_sql_query("SELECT * FROM entregas", conn)
conn.close()

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhuma entrega cadastrada ainda. Use a barra lateral para adicionar!")
