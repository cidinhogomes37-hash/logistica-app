import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão Logística", layout="wide")

# Inicialização do banco de dados na sessão
if "entregas" not in st.session_state:
    st.session_state.entregas = pd.DataFrame(columns=[
        "ID", "Cliente", "Telefone", "Endereço", "Entregador", "Valor (R$)", "Status", "Data/Hora"
    ])

# -----------------------------------------------------------------------------
# BARRA LATERAL: Novo Cadastro
# -----------------------------------------------------------------------------
st.sidebar.title("📌 Novo Cadastro")

with st.sidebar.form("form_cadastro", clear_on_submit=True):
    nome_cliente = st.text_input("Nome do Cliente")
    telefone_cliente = st.text_input("Telefone / WhatsApp")
    endereco_entrega = st.text_area("Endereço de Entrega", height=80)
    nome_entregador = st.text_input("Nome do Entregador")
    valor_frete = st.number_input("Valor do Pedido/Frete (R$)", min_value=0.0, format="%.2f", step=1.0)
    status_inicial = st.selectbox("Status Inicial", ["Pendente", "Em Trânsito", "Entregue", "Cancelado"])
    
    btn_salvar = st.form_submit_button("Salvar Entrega")

if btn_salvar:
    if nome_cliente.strip() == "" or endereco_entrega.strip() == "":
        st.sidebar.error("Preencha pelo menos o Nome do Cliente e o Endereço!")
    else:
        novo_id = len(st.session_state.entregas) + 1
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        nova_linha = {
            "ID": novo_id,
            "Cliente": nome_cliente,
            "Telefone": telefone_cliente,
            "Endereço": endereco_entrega,
            "Entregador": nome_entregador if nome_entregador else "Não Atribuído",
            "Valor (R$)": f"{valor_frete:.2f}",
            "Status": status_inicial,
            "Data/Hora": data_hora
        }
        
        st.session_state.entregas = pd.concat(
            [st.session_state.entregas, pd.DataFrame([nova_linha])], 
            ignore_index=True
        )
        st.sidebar.success(f"Entrega #{novo_id} registrada!")
        st.rerun()

# -----------------------------------------------------------------------------
# PAINEL PRINCIPAL
# -----------------------------------------------------------------------------
st.title("📋 Dashboard de Entregas")

if not st.session_state.entregas.empty:
    df = st.session_state.entregas

    # Métricas no Topo
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de Pedidos", len(df))
    c2.metric("Pendentes", len(df[df["Status"] == "Pendente"]))
    c3.metric("Em Trânsito", len(df[df["Status"] == "Em Trânsito"]))
    c4.metric("Concluídas", len(df[df["Status"] == "Entregue"]))

    st.divider()

    # Tabela Completa
    st.subheader("📋 Lista Geral de Registros")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Rotas no Google Maps
    st.subheader("🗺️ Rotas no Google Maps")
    for idx, row in df.iterrows():
        col_info, col_btn = st.columns([4, 1])
        with col_info:
            st.write(f"**#{row['ID']} - {row['Cliente']}** | {row['Endereço']} (*{row['Status']}*)")
        with col_btn:
            endereco_encoded = urllib.parse.quote(row['Endereço'])
            maps_url = f"https://www.google.com/maps/search/?api=1&query={endereco_encoded}"
            st.link_button("📍 Abra no Maps", maps_url)

    st.divider()

    # Gerenciamento de Status
    st.subheader("⚙️ Gerenciar Entrega")
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    ids_disponiveis = df["ID"].tolist()
    
    with col1:
        id_selecionado = st.selectbox("Selecione o ID", ids_disponiveis)
    
    status_atual = df.loc[df["ID"] == id_selecionado, "Status"].values[0]
    
    with col2:
        novo_status = st.selectbox(
            "Novo Status", 
            ["Pendente", "Em Trânsito", "Entregue", "Cancelado"],
            index=["Pendente", "Em Trânsito", "Entregue", "Cancelado"].index(status_atual)
        )
    
    with col3:
        st.write("")
        st.write("")
        if st.button("Atualizar Status"):
            st.session_state.entregas.loc[
                st.session_state.entregas["ID"] == id_selecionado, "Status"
            ] = novo_status
            st.success(f"Status da entrega #{id_selecionado} alterado para {novo_status}!")
            st.rerun()

    with col4:
        st.write("")
        st.write("")
        if st.button("🗑️ Excluir", type="primary"):
            st.session_state.entregas = st.session_state.entregas[
                st.session_state.entregas["ID"] != id_selecionado
            ]
            st.warning(f"Entrega #{id_selecionado} removida!")
            st.rerun()

else:
    st.info("Nenhuma entrega cadastrada até o momento.")