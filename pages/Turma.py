import streamlit as st
import pandas as pd
import mysql.connector
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
def load_turmas(co_entidade):
    conn = get_db_connection(st.session_state.role)
    cursor = conn.cursor()
    query = """
    SELECT NO_TURMA,
           IN_DISC_QUIMICA,
           IN_DISC_FISICA,
           IN_DISC_MATEMATICA,
           IN_DISC_BIOLOGIA,
           IN_DISC_CIENCIAS,
           IN_DISC_LINGUA_PORTUGUESA,
           IN_DISC_LINGUA_INGLES,
           IN_DISC_LINGUA_ESPANHOL,
           IN_DISC_LINGUA_FRANCES,
           IN_DISC_LINGUA_OUTRA,
           IN_DISC_LINGUA_INDIGENA,
           IN_DISC_ARTES,
           IN_DISC_EDUCACAO_FISICA,
           IN_DISC_HISTORIA,
           IN_DISC_GEOGRAFIA,
           IN_DISC_FILOSOFIA,
           IN_DISC_ENSINO_RELIGIOSO,
           IN_DISC_ESTUDOS_SOCIAIS,
           IN_DISC_SOCIOLOGIA,
           IN_DISC_EST_SOCIAIS_SOCIOLOGIA,
           IN_DISC_INFORMATICA_COMPUTACAO,
           IN_DISC_PROFISSIONALIZANTE,
           IN_DISC_ATENDIMENTO_ESPECIAIS,
           IN_DISC_DIVER_SOCIO_CULTURAL,
           IN_DISC_LIBRAS,
           IN_DISC_PEDAGOGICAS,
           IN_DISC_OUTRAS
    FROM turma
    WHERE CO_ENTIDADE = %s;
    """
    cursor.execute(query, (co_entidade,))
    res = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(res, columns=columns)
    conn.close()
    
  
    disciplina_map = {
        'IN_DISC_QUIMICA': 'Química',
        'IN_DISC_FISICA': 'Física',
        'IN_DISC_MATEMATICA': 'Matemática',
        'IN_DISC_BIOLOGIA': 'Biologia',
        'IN_DISC_CIENCIAS': 'Ciências',
        'IN_DISC_LINGUA_PORTUGUESA': 'Língua Portuguesa',
        'IN_DISC_LINGUA_INGLES': 'Inglês',
        'IN_DISC_LINGUA_ESPANHOL': 'Espanhol',
        'IN_DISC_LINGUA_FRANCES': 'Francês',
        'IN_DISC_LINGUA_OUTRA': 'Outra Língua Estrangeira',
        'IN_DISC_LINGUA_INDIGENA': 'Língua Indígena',
        'IN_DISC_ARTES': 'Artes',
        'IN_DISC_EDUCACAO_FISICA': 'Educação Física',
        'IN_DISC_HISTORIA': 'História',
        'IN_DISC_GEOGRAFIA': 'Geografia',
        'IN_DISC_FILOSOFIA': 'Filosofia',
        'IN_DISC_ENSINO_RELIGIOSO': 'Ensino Religioso',
        'IN_DISC_ESTUDOS_SOCIAIS': 'Estudos Sociais',
        'IN_DISC_SOCIOLOGIA': 'Sociologia',
        'IN_DISC_EST_SOCIAIS_SOCIOLOGIA': 'Estudos Sociais ou Sociologia',
        'IN_DISC_INFORMATICA_COMPUTACAO': 'Informática',
        'IN_DISC_PROFISSIONALIZANTE': 'Profissionalizante',
        'IN_DISC_ATENDIMENTO_ESPECIAIS': 'Atendimento Especial',
        'IN_DISC_DIVER_SOCIO_CULTURAL': 'Diversidade Sociocultural',
        'IN_DISC_LIBRAS': 'Libras',
        'IN_DISC_PEDAGOGICAS': 'Disciplinas Pedagógicas',
        'IN_DISC_OUTRAS': 'Outras Disciplinas'
    }
    
    
    df["Disciplinas"] = df.apply(lambda row: ', '.join([disciplina_map[col] for col in disciplina_map if row[col] == 1]), axis=1)
    
   
    df = df[['NO_TURMA', 'Disciplinas']]
    
    
    df["Disciplinas"] = df["Disciplinas"].replace("", "Nenhuma")
    
    return df


st.title("Consulta de Turmas por Escola")


escolas_df = load_escolas()
escola_selecionada = st.selectbox("Selecione uma escola:", escolas_df["NO_ENTIDADE"])
co_entidade = escolas_df[escolas_df["NO_ENTIDADE"] == escola_selecionada]["CO_ENTIDADE"].values[0]


if st.button("Listar turmas e disciplinas"):
    turmas_df = load_turmas(int(co_entidade))
    st.write("Turmas e disciplinas disponíveis:")
    st.write(turmas_df)


if st.sidebar.button("Logout"):
    logout()