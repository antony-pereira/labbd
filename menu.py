import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/total.py", label="Total de alunos, professores e turmas")
    st.sidebar.page_link("pages/Agrupar.py", label="Agrupar pelo nivel de ensino")
    st.sidebar.page_link("pages/CodPessoa.py", label="Cod Pessoa")
    st.sidebar.page_link("pages/Turma.py", label="Todas as turmas por escola")
    st.sidebar.page_link("pages/notasideb.py", label="Notas IDEB")
    st.sidebar.page_link("pages/bookmark.py", label="Lista de escolas")
    if st.session_state.role in ["Gerencial"]:
        st.sidebar.page_link("pages/CRUD.py", label="Lista de Bookmarks")
        


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()
