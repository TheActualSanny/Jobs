import streamlit as st
from preferences.preferences import handle_job_preferences, handle_auth

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'username' not in st.session_state:
        st.session_state['username'] = ''

    if not st.session_state['logged_in']:
        handle_auth()
    else:
        handle_job_preferences()

        if st.button("Logout", key="logout_button"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.rerun()  

if __name__ == "__main__":
    main()
