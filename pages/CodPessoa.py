import streamlit as st
import mysql.connector
import pandas as pd
from app import get_db_connection
from menu import menu_with_redirect
from app import logout

menu_with_redirect()

@st.cache_data
def load_escolas():
    conn = get_db_connection(st.session_state.role)
    cursor = conn.cursor()
    cursor.execute("SELECT CO_ENTIDADE, NO_ENTIDADE FROM escola;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=["CO_ENTIDADE", "NO_ENTIDADE"])
    conn.close()
    return df


@st.cache_data
def load_docentes(co_entidade):
    conn = get_db_connection(st.session_state.role)
    cursor = conn.cursor()
    
    
    query_docentes = """
    SELECT DISTINCT d.CO_PESSOA_FISICA AS docente
    FROM docente d
    LEFT JOIN turma t ON d.ID_TURMA = t.ID_TURMA
    WHERE t.CO_ENTIDADE = %s
    """
    cursor.execute(query_docentes, (co_entidade,))
    docentes = cursor.fetchall()
    df_docentes = pd.DataFrame(docentes, columns=["Docente"])
    
    
    query_alunos = "SELECT CO_PESSOA_FISICA AS aluno FROM matricula WHERE CO_ENTIDADE = %s"
    cursor.execute(query_alunos, (co_entidade,))
    alunos = cursor.fetchall()
    df_alunos = pd.DataFrame(alunos, columns=["Aluno"])
    
    conn.close()
    return df_docentes, df_alunos


st.title("Consulta de Professores e Alunos por Escola")


escolas_df = load_escolas()
escola_selecionada = st.selectbox("Selecione uma escola:", escolas_df["NO_ENTIDADE"])
co_entidade = escolas_df[escolas_df["NO_ENTIDADE"] == escola_selecionada]["CO_ENTIDADE"].values[0]

if st.button("Listar professores e alunos"):
    df_docentes, df_alunos = load_docentes(int(co_entidade))
    
    if df_docentes.empty and df_alunos.empty:
        st.write("Nenhum professor ou aluno encontrado para a escola selecionada.")
    else:
        if not df_docentes.empty:
            st.write("Professores disponíveis:")
            st.dataframe(df_docentes)
            if st.session_state.role in ["Gerencial"]:
                # Botão para baixar os dados como CSV
                csv = df_docentes.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Baixar tabela como CSV",
                    data=csv,
                    file_name='dados.csv',
                    mime='text/csv',
                    key=12
                )
            
        
        if not df_alunos.empty:
            st.write("Alunos disponíveis:")
            st.dataframe(df_alunos)
            if st.session_state.role in ["Gerencial"]:
                # Botão para baixar os dados como CSV
                csv = df_alunos.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Baixar tabela como CSV",
                    data=csv,
                    file_name='dados.csv',
                    mime='text/csv',
                    key=15
                )


if st.sidebar.button("Logout"):
    logout()