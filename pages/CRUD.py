import streamlit as st
import pandas as pd
import mysql.connector
from menu import menu_with_redirect
from app import get_db_connection
from app import logout

menu_with_redirect()

@st.cache_data
def load_usuario():
    conn = get_db_connection(st.session_state.role)
    cursor = conn.cursor()
    cursor.execute("SELECT NOME, EMAIL, DATA_DE_CADASTRO, PERFIL FROM usuario;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    conn.close()
    return df

def buscar_bookmarks(usuario_id):
    """
    Busca os bookmarks salvos por um usuário específico.

    Retorna:
        Uma lista de dicionários com 'CO_ENTIDADE' e 'NO_ENTIDADE'.
    """
    try:
        conn = get_db_connection(st.session_state.role)
        cursor = conn.cursor()

        # Query para buscar os bookmarks
        query = "SELECT CO_ENTIDADE, NO_ENTIDADE FROM bookmark WHERE ID_USUARIO = %s;"
        cursor.execute(query, (usuario_id,))
        resultados = cursor.fetchall()

        # Formatar resultados como uma lista de dicionários
        bookmarks = [{"CO_ENTIDADE": row[0], "NO_ENTIDADE": row[1]} for row in resultados]
        return bookmarks

    except Exception as e:
        st.error(f"Erro ao buscar bookmarks: {e}")
        return []
    finally:
        conn.close()

def remover_bookmark(usuario_id, co_entidade):
    """
    Remove um bookmark específico baseado no ID do usuário e código da entidade.
    """
    try:
        conn = get_db_connection(st.session_state.role)
        cursor = conn.cursor()

        usuario_id = int(usuario_id)
        co_entidade = int(co_entidade)
        # Query para deletar o bookmark
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

# Título e exibição dos usuários
st.title("Lista de Usuários")
df = load_usuario()
st.dataframe(df, use_container_width=True)

# Exibição e manipulação de bookmarks
if 'user_id' in st.session_state:
    bookmarks = buscar_bookmarks(st.session_state['user_id'])

    if bookmarks:
        st.write("Seus bookmarks:")
        
        # Convertendo para um DataFrame para o selectbox
        bookmarks_df = pd.DataFrame(bookmarks)
        
        # Exibe lista de bookmarks
        for bookmark in bookmarks:
            st.write(f"- {bookmark['NO_ENTIDADE']} (Código: {bookmark['CO_ENTIDADE']})")

        # Selecione um bookmark para remover
        bookmark_selecionado = st.selectbox(
            "Selecione uma escola para remover:", 
            bookmarks_df["NO_ENTIDADE"]
        )

        # Botão para remover o bookmark selecionado
        if st.button("Remover Bookmark"):
            # Obtendo o CO_ENTIDADE do bookmark selecionado
            co_entidade = bookmarks_df.loc[bookmarks_df["NO_ENTIDADE"] == bookmark_selecionado, "CO_ENTIDADE"].values[0]
            remover_bookmark(st.session_state['user_id'], co_entidade)

            # Atualiza a lista de bookmarks
            st.rerun()
    else:
        st.info("Você ainda não tem bookmarks salvos.")
else:
    st.error("Você precisa estar logado para visualizar os bookmarks!")

# Botão de Logout
if st.sidebar.button("Logout"):
    logout()
