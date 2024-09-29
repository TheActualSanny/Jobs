import hashlib
import psycopg2
import streamlit as st
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

def create_users_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

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

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = ''

def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if authenticate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}!")
            return True
        else:
            st.error("Invalid username or password.")
            return False

def signup():
    st.title("Signup")
    username = st.text_input("Create a Username", key="signup_username")
    password = st.text_input("Create a Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Signup", key="signup_button"):
        st.write(f"Username: {username}, Password: {password}, Confirm Password: {confirm_password}")
        
        if username_exists(username):
            st.error("Username already exists. Please choose another one.")
            return False
        elif password != confirm_password:
            st.error("Passwords do not match.")
            return False
        else:
            add_user(username, hash_password(password))
            st.success("Account created successfully! You can now log in.")
            return True
