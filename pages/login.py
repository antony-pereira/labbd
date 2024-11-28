import streamlit as st
import mysql.connector

def get_db_connection(perfil):
    if perfil == 'Aberto':
        return mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            user='user_aberto',
            password='senha_aberto',  # Senha do usuário 'usuario_aberto'
            db=st.secrets["DB_NAME"]
        )
    elif perfil == 'Gerencial':
        return mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            user='user_gerencial',
            password='senha_gerencial',  # Senha do usuário 'usuario_gerencial'
            db=st.secrets["DB_NAME"]
        )
    else:
        raise ValueError("Perfil desconhecido")

def login_page():
    st.title("Login")
    
    # Formulário de login
    with st.form("login_form"):
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Entrar")
    
    if submit_button:
        # Conectar ao banco de dados para autenticação usando credenciais padrão
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            user=st.secrets["DB_USERNAME"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets["DB_PORT"],
            db=st.secrets["DB_NAME"]
        )
        cursor = conn.cursor()
        query = "SELECT * FROM usuario WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Usuário autenticado, armazena informações no session_state
            perfil = result[5]  # O perfil está na coluna PERFIL
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = result[0]  # Guarda o ID do usuário logado
            st.session_state['perfil'] = perfil  # Guarda o perfil do usuário
            st.session_state.sidebar_state = 'expanded'
            
            # Use a função get_db_connection com base no perfil
            conn = get_db_connection(perfil)
            st.session_state['db_connection'] = conn
            
            st.rerun()  # Recarrega a aplicação para mostrar as páginas protegidas
        else:
            st.error("Email ou senha incorretos!")
    
    if st.button("Não tem uma conta? Cadastre-se aqui"):
        st.session_state['show_cadastro'] = True
