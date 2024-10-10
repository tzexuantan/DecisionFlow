import streamlit as st
import sqlite3
import hashlib

#Create a connection with the sql database users
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

#Function to create a new table users
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""
                CREATE TABLE IF NOT EXISTS users(
              username TEXT PRIMARY KEY,
              password TEXT NOT NULL
              )""")
    conn.commit()
    conn.close()

#Function to hash the password for more security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Function to register the user using username and password
def register_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        st.success(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different one.")
    finally:
        conn.close()

# Function to Login user based on username and password
def login_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    
    if user:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.success(f"Logged in as '{username}'!")
    else:
        st.error("Invalid username or password")

#Function to log out current user
def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("Logged out successfully!")