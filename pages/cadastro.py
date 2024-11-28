import streamlit as st
import mysql.connector
from datetime import datetime

def validar(nome, email, senha):
	if nome=="" or email=="" or senha=="":
		return False
	return True

# Defina uma senha mestra para validar o cadastro de usuários gerenciais
SENHA_MESTRA_GERENCIAL = "admin"

def cadastro_page():
    st.title("Cadastro")

    # Inicializa as variáveis do session_state se não existirem
    if 'perfil' not in st.session_state:
        st.session_state['perfil'] = 'Aberto'  # Valor inicial do perfil
    if 'nome' not in st.session_state:
        st.session_state['nome'] = ""
    if 'email' not in st.session_state:
        st.session_state['email'] = ""
    if 'senha' not in st.session_state:
        st.session_state['senha'] = ""
    if 'senha_gerencial' not in st.session_state:
        st.session_state['senha_gerencial'] = ""

    # Seletor de perfil
    perfil = st.radio("Perfil", options=["Aberto", "Gerencial"], index=0 if st.session_state['perfil'] == 'Aberto' else 1)
    
    # Atualiza o perfil no session_state
    st.session_state['perfil'] = perfil
    
    # Formulário de cadastro
    with st.form("cadastro_form"):
        nome = st.text_input("Nome", value=st.session_state["nome"])
        email = st.text_input("Email", value=st.session_state["email"])
        senha = st.text_input("Senha", type="password", value=st.session_state["senha"])

        # Se o perfil for "Gerencial", exibe um campo de senha para verificação
        senha_gerencial = None
        if perfil == "Gerencial":
            senha_gerencial = st.text_input("Senha de Verificação para Perfil Gerencial", type="password", value=st.session_state["senha_gerencial"])

        # Salva o valor da senha de verificação
        st.session_state['senha_gerencial'] = senha_gerencial
        
        submit_button = st.form_submit_button("Cadastrar")

    # Quando o usuário submete o formulário
    if submit_button and validar(nome, email, senha):
        # Valida a senha para perfil gerencial, se selecionado
        if perfil == "Gerencial" and senha_gerencial != SENHA_MESTRA_GERENCIAL:
            st.error("Senha de verificação incorreta! Cadastro de perfil gerencial não permitido.")
            return
        
        # Se tudo estiver correto, registra o usuário
        data_cadastro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Conectar ao banco de dados para inserir novo usuário
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            user=st.secrets["DB_USERNAME"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets["DB_PORT"],
            db=st.secrets["DB_NAME"]
        )
        cursor = conn.cursor()
        # Insere o perfil no banco de dados também
        query = "INSERT INTO usuario (NOME, EMAIL, DATA_DE_CADASTRO, SENHA, PERFIL) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, email, data_cadastro, senha, perfil))
        conn.commit()
        conn.close()

        st.success("Cadastro realizado com sucesso! Volte para a página de login.")
        st.session_state['show_cadastro'] = False

    elif submit_button:
         st.warning("Dados inválidos")
        
    if st.button("Já tem uma conta? Faça login"):
        st.session_state['show_cadastro'] = False
