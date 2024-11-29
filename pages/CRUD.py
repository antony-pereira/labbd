import streamlit as st
import pandas as pd
import mysql.connector
from menu import menu_with_redirect
from app import get_db_connection
from app import logout

menu_with_redirect()

def buscar_bookmarks(usuario_id):
   
    try:
        conn = get_db_connection(st.session_state.role)
        cursor = conn.cursor()

        
        query = "SELECT CO_ENTIDADE, NO_ENTIDADE FROM bookmark WHERE ID_USUARIO = %s;"
        cursor.execute(query, (usuario_id,))
        resultados = cursor.fetchall()

        
        bookmarks = [{"CO_ENTIDADE": row[0], "NO_ENTIDADE": row[1]} for row in resultados]
        return bookmarks

    except Exception as e:
        st.error(f"Erro ao buscar bookmarks: {e}")
        return []
    finally:
        conn.close()

def remover_bookmark(usuario_id, co_entidade):
    
    try:
        conn = get_db_connection(st.session_state.role)
        cursor = conn.cursor()

        usuario_id = int(usuario_id)
        co_entidade = int(co_entidade)
        
        query = "DELETE FROM bookmark WHERE ID_USUARIO = %s AND CO_ENTIDADE = %s;"
        cursor.execute(query, (usuario_id, co_entidade))
        conn.commit()

        if cursor.rowcount > 0:
            st.success("Bookmark removido com sucesso!")
        else:
            st.warning("Nenhum bookmark encontrado para remover.")

    except Exception as e:
        st.error(f"Erro ao remover bookmark: {e}")
    finally:
        conn.close()


st.title("Lista de Bookmarks salvos")



if 'user_id' in st.session_state:
    bookmarks = buscar_bookmarks(st.session_state['user_id'])

    if bookmarks:
        st.write("Seus bookmarks:")
        
        
        bookmarks_df = pd.DataFrame(bookmarks)
        
        
        for bookmark in bookmarks:
            st.write(f"- {bookmark['NO_ENTIDADE']} (Código: {bookmark['CO_ENTIDADE']})")

        
        bookmark_selecionado = st.selectbox(
            "Selecione uma escola para remover:", 
            bookmarks_df["NO_ENTIDADE"]
        )

        
        if st.button("Remover Bookmark"):
            
            co_entidade = bookmarks_df.loc[bookmarks_df["NO_ENTIDADE"] == bookmark_selecionado, "CO_ENTIDADE"].values[0]
            remover_bookmark(st.session_state['user_id'], co_entidade)

            
            st.rerun()
    else:
        st.info("Você ainda não tem bookmarks salvos.")
else:
    st.error("Você precisa estar logado para visualizar os bookmarks!")


if st.sidebar.button("Logout"):
    logout()
