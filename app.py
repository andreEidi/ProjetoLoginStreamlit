import streamlit as st
import streamlit_authenticator as stauth
from time import sleep

def config():
    # Configuration for the authenticator
    try:
        consulta_geral()
    except:
        cria_tabela()

    db_query = consulta_geral()

    registros = {'usernames': {}}
    for data in db_query:
        registros['usernames'][data[1]] = {'name' : data[0], 'password' : data[2]}

    COOKIE_EXPIRY_DAYS = 30
    authenticator = stauth.Authenticate(
        registros,
        'my_cookie',
        'key_cookie',
        COOKIE_EXPIRY_DAYS,
    )
    return authenticator

def main():
    authenticator = config()

    if 'clicou_registrar' not in st.session_state:
        st.session_state['clicou_registrar'] = False

    if st.session_state['clicou_registrar'] == False:
        login_form(authenticator=authenticator)
    else:
        usuario_form()
    

def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login')
    if authentication_status:
        st.success(f'Bem-vindo {name}')
        authenticator.logout('Logout', 'sidebar')
        sleep(1)
        st.session_state['clicou_registrar'] = True
        st.rerun()
    elif authentication_status is False:
        st.error('Usuário ou senha incorretos')
    elif authentication_status is None:
        clicou_em_registrar = st.button('Registrar')
        if clicou_em_registrar:
            st.session_state['clicou_registrar'] = True
            st.rerun()
        st.warning('Por favor, faça o login')


