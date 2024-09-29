from db.db_connection import get_connection
from auth.password_utils import hash_password, verify_password
from db.tables import create_users_table
import streamlit as st

def username_exists(username):
    create_users_table()  
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

def add_user(username, hashed_password):
    create_users_table()  
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cur.close()
    conn.close()

def authenticate_user(username, password):
    create_users_table()  
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    stored_password = cur.fetchone()
    cur.close()
    conn.close()
    if stored_password:
        return verify_password(stored_password[0], password)
    return False

def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if authenticate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

def signup():
    st.title("Signup")
    username = st.text_input("Create a Username", key="signup_username")
    password = st.text_input("Create a Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Signup", key="signup_button"):
        if username_exists(username):
            st.error("Username already exists. Please choose another one.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            add_user(username, hash_password(password))
            st.success("Account created successfully! You can now log in.")
