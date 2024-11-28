import streamlit as st
import pandas as pd
import mysql.connector
from menu import menu_with_redirect
from app import get_db_connection
from app import logout

menu_with_redirect()

@st.cache_data
def load_data():
    
    conn = get_db_connection(st.session_state.role)
    
    cursor = conn.cursor()
    cursor.execute("select * from v2_total;")
    res = cursor.fetchall()
    
    
    df = pd.DataFrame(res, columns=cursor.column_names)
    conn.close()
    
    return df


st.title("Lista de Escolas com Filtros Personalizados")


df = load_data()


st.sidebar.header("Filtros de Quantidade Mínima")

min_alunos = st.sidebar.slider("Quantidade mínima de alunos", 0, int(df["total_alunos"].max()), 0)
min_professores = st.sidebar.slider("Quantidade mínima de professores", 0, int(df["total_professores"].max()), 0)
min_turmas = st.sidebar.slider("Quantidade mínima de turmas", 0, int(df["total_turmas"].max()), 0)


filtered_df = df[
(df["total_alunos"] >= min_alunos) &
(df["total_professores"] >= min_professores) &
(df["total_turmas"] >= min_turmas)
]


if st.button("Ordenar por número de alunos"):
    filtered_df = filtered_df.sort_values(by="total_alunos", ascending=False)


st.write("Escolas filtradas com base nos critérios selecionados:")
st.write(filtered_df)

if st.session_state.role in ["Gerencial"]:
    # Botão para baixar os dados como CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar tabela como CSV",
        data=csv,
        file_name='dados.csv',
        mime='text/csv'
    )


if st.sidebar.button("Logout"):
    logout()