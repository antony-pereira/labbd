import streamlit as st
import pandas as pd
import mysql.connector
from app import get_db_connection
from app import logout

from menu import menu_with_redirect

menu_with_redirect()

st.header("Tabela de notas IDEB")


conn = get_db_connection(st.session_state.role)

cursor = conn.cursor()

cursor.execute("select * from notas_ideb;")
res = cursor.fetchall()
df2 = pd.DataFrame(res, columns=cursor.column_names)

st.dataframe(df2, use_container_width=True)

if st.session_state.role in ["Gerencial"]:
    # Botão para baixar os dados como CSV
    csv = df2.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar tabela como CSV",
        data=csv,
        file_name='dados.csv',
        mime='text/csv',
        key=30
    )

if st.sidebar.button("Logout"):
    logout()
