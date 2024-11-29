import streamlit as st
from menu import menu
from pages.login import login_page
from pages.cadastro import cadastro_page
import mysql.connector




if "role" not in st.session_state:
    st.session_state.role = None


st.session_state._role = st.session_state.role

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False


if 'show_cadastro' not in st.session_state:
    st.session_state['show_cadastro'] = False


def logout():
    st.session_state['logged_in'] = False
    st.session_state['show_cadastro'] = False
    st.session_state.role = None
    st.rerun()

def set_role():
    
    st.session_state.role = st.session_state._role

def get_db_connection(perfil):
    return mysql.connector.connect(
                    host=st.secrets["DB_HOST"],
                    user=st.secrets["DB_USERNAME"],
                    password=st.secrets["DB_PASSWORD"],
                    port=st.secrets["DB_PORT"],
                    db=st.secrets["DB_NAME"]
                )

if not st.session_state['logged_in']:
    if st.session_state['show_cadastro']:
        cadastro_page()  
    else:
    
        st.title("Login")
            
        
        with st.form("login_form"):
                email = st.text_input("Email")
                senha = st.text_input("Senha", type="password")
                submit_button = st.form_submit_button("Entrar")
            
        if submit_button:
                
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
                    
                    perfil = result[5]  
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = result[0]  
                    st.session_state._role = perfil  
                    set_role()
                    
                   
                    conn = get_db_connection(perfil)
                    st.session_state['db_connection'] = conn
                    
                    st.rerun()  
                else:
                    st.error("Email ou senha incorretos!")
            
        if st.button("Não tem uma conta? Cadastre-se aqui"):
                st.session_state['show_cadastro'] = True
   
menu() # Render the dynamic menu!
