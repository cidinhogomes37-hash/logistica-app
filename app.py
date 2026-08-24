import streamlit as st
import pyodbc

# conexão com SQL Server
def conectar():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;" # ou o nome do seu servidor no SSMS (ex: .\SQLEXPRESS ou JOSE777\imperion)
        "DATABASE=LogisticaDB;"
        "Trusted_Connection=yes;"

    )

st.title("🚚 Painel de Controle da Logística")

# 1. Visualizar Entregas
st.subheader("Entregas Cadastradas")
conn = conectar()
cursor = conn.cursor()
cursor.execute("""
    SELECT
        E.EntregasID, E.Cliente, E.Endereco, E.Valor, E.Status,
        M.Nome AS Motorista, V.Placa AS Veiculo
    FROM Entregas E
    LEFT JOIN Motoristas M ON E.Motorista = M.MotoristaID
    LEFT JOIN Veiculos V ON E.VeiculoID = V.VeiculoID
    """)
dados =cursor.fetchall()    
conn.close()

# Exibe na tela em formato de tabela
st.dataframe(dados)

# 2. Alertar Dados de uma Entrega
st.subheader("✏️ Alertar Entrega")

id_entrega = st.number_input("Digite o ID da Entrega:", min_value=1, step=1)
novo_endereco = st.text_input("Novo Endereço")
novo_status = st.selectbox("Novo Status:", ["Pendente", "Em Trâsito", "Entregue", "Cancelado"])

if st.button("Atualizar Entrega"):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Entregas
        SET Endereco = ?, Status = ?
        WHERE EntregasID = ?
        """, (novo_endereco, novo_status, id_entrega))
    conn.commit()
    conn.close()
    st.success(f"Entregas {id_entrega} atualizada com sucesso!")
    
