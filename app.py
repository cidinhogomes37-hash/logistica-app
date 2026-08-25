import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel de Logística", layout="wide")

# Conexão com o banco SQLite
def conectar():
    return sqlite3.connect('logistica.db')

# Inicializar tabela no banco
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

# --- BARRA LATERAL: CADASTRO ---
with st.sidebar:
    st.header("Novo Cadastro")
    cliente = st.text_input("Nome do Cliente")
    endereco = st.text_input("Endereço de Entrega")
    status = st.selectbox("Status Inicial", ["Pendente", "Em Trânsito", "Entregue"])
    
    if st.button("Salvar Entrega", type="primary"):
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

# --- CARREGAR DADOS ---
conn = conectar()
df = pd.read_sql_query("SELECT id AS ID, cliente AS Cliente, endereco AS Endereço, status AS Status FROM entregas", conn)
conn.close()

# --- CARDS DE MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)
total = len(df)
pendentes = len(df[df['Status'] == 'Pendente']) if not df.empty else 0
em_transito = len(df[df['Status'] == 'Em Trânsito']) if not df.empty else 0
entregues = len(df[df['Status'] == 'Entregue']) if not df.empty else 0

col1.metric("Total de Entregas", total)
col2.metric("Pendentes", pendentes)
col3.metric("Em Trânsito", em_transito)
col4.metric("Entregues", entregues)

st.divider()

# --- TABELA E GERENCIAMENTO ---
if not df.empty:
    st.subheader("📋 Lista de Entregas")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    
    # Gerenciar Entregas (Atualizar Status / Excluir)
    st.subheader("⚙️ Gerenciar Entrega")
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        id_selecionado = st.selectbox("Selecione o ID", df['ID'].tolist())
    
    with c2:
        novo_status = st.selectbox("Novo Status", ["Pendente", "Em Trânsito", "Entregue"])
        if st.button("Atualizar Status"):
            conn = conectar()
            c = conn.cursor()
            c.execute("UPDATE entregas SET status = ? WHERE id = ?", (novo_status, id_selecionado))
            conn.commit()
            conn.close()
            st.success("Status atualizado!")
            st.rerun()
            
    with c3:
        st.write("")
        st.write("")
        if st.button("🗑️ Excluir Registrada", type="secondary"):
            conn = conectar()
            c = conn.cursor()
            c.execute("DELETE FROM entregas WHERE id = ?", (id_selecionado,))
            conn.commit()
            conn.close()
            st.warning("Entrega removida!")
            st.rerun()
else:
    st.info("Nenhuma entrega cadastrada ainda. Use a barra lateral para adicionar!")
