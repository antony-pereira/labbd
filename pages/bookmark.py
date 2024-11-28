import pandas as pd
import streamlit as st
from app import get_db_connection
import mysql.connector
from app import logout

from menu import menu_with_redirect

menu_with_redirect()
# Função para carregar as escolas
def load_escolas():
    conn = get_db_connection(st.session_state.role)
    cursor = conn.cursor()
    cursor.execute("SELECT CO_ENTIDADE, NO_ENTIDADE FROM escola;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=["CO_ENTIDADE", "NO_ENTIDADE"])
    conn.close()
    return df

# Função para salvar no bookmark
def adicionar_bookmark(usuario_id, co_entidade, no_entidade):
    """
    Adiciona uma escola ao bookmark do usuário especificado.
    """
    try:
        conn = get_db_connection(st.session_state.role)
        cursor = conn.cursor()

        # Verificar se o bookmark já existe para evitar duplicatas
        query_verifica = "SELECT * FROM bookmark WHERE ID_USUARIO = %s AND CO_ENTIDADE = %s;"
        cursor.execute(query_verifica, (usuario_id, co_entidade))
        existe = cursor.fetchone()

        if existe:
            st.warning("Esta escola já está salva nos seus bookmarks.")
        else:
            # Inserir novo registro no bookmark
            query_insere = "INSERT INTO bookmark (ID_USUARIO, CO_ENTIDADE, NO_ENTIDADE) VALUES (%s, %s, %s);"
            cursor.execute(query_insere, (usuario_id, co_entidade, no_entidade))
            conn.commit()
            st.success("Escola adicionada ao bookmark com sucesso!")

    except Exception as e:
        st.error(f"Erro ao salvar bookmark: {e}")

# Carregar as escolas
st.header("Listar as escolas da cidade")
conn = get_db_connection(st.session_state.role)

cursor = conn.cursor()

cursor.execute("select * from v3_escola;")
res = cursor.fetchall()
df = pd.DataFrame(res, columns=cursor.column_names)

st.dataframe(df, use_container_width=True)
if st.session_state.role in ["Gerencial"]:
    # Botão para baixar os dados como CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar tabela como CSV",
        data=csv,
        file_name='dados.csv',
        mime='text/csv',
        key=24
    )
    escolas_df = load_escolas()
    # Selectbox para selecionar uma escola
    escola_selecionada_nome = st.selectbox("Selecione uma escola:", escolas_df["NO_ENTIDADE"])

    # Recuperar o código da escola selecionada
    if escola_selecionada_nome:
        escola_selecionada_codigo = escolas_df.loc[
            escolas_df["NO_ENTIDADE"] == escola_selecionada_nome, "CO_ENTIDADE"
        ].values[0]
        escola_selecionada_codigo = int(escola_selecionada_codigo)

        # Botão para salvar no bookmark
        if st.button("Salvar nos meus bookmarks"):
            if 'user_id' in st.session_state:  # Certificar que o usuário está logado
                adicionar_bookmark(st.session_state['user_id'], escola_selecionada_codigo, escola_selecionada_nome)
            else:
                st.error("Você precisa estar logado para salvar um bookmark!")



if st.sidebar.button("Logout"):
    logout()