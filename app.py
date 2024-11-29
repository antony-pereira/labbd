import streamlit as st
from menu import menu
from pages.login import login_page
from pages.cadastro import cadastro_page
import mysql.connector



# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Controla o estado da página de cadastro
if 'show_cadastro' not in st.session_state:
    st.session_state['show_cadastro'] = False


def logout():
    st.session_state['logged_in'] = False
    st.session_state['show_cadastro'] = False
    st.session_state.role = None
    st.rerun()

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role

def get_db_connection(perfil):
    return conn = mysql.connector.connect(
                    host=st.secrets["DB_HOST"],
                    user=st.secrets["DB_USERNAME"],
                    password=st.secrets["DB_PASSWORD"],
                    port=st.secrets["DB_PORT"],
                    db=st.secrets["DB_NAME"]
                )

if not st.session_state['logged_in']:
    if st.session_state['show_cadastro']:
        cadastro_page()  # Mostra a página de cadastro
    else:
    # Selectbox to choose role
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
                    st.session_state._role = perfil  # Guarda o perfil do usuário
                    set_role()
                    
                    # Use a função get_db_connection com base no perfil
                    conn = get_db_connection(perfil)
                    st.session_state['db_connection'] = conn
                    
                    st.rerun()  # Recarrega a aplicação para mostrar as páginas protegidas
                else:
                    st.error("Email ou senha incorretos!")
            
        if st.button("Não tem uma conta? Cadastre-se aqui"):
                st.session_state['show_cadastro'] = True
   
menu() # Render the dynamic menu!
