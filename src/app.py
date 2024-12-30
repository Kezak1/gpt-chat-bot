import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import sqlite3
import hashlib

load_dotenv()

def init_db():
    with sqlite3.connect("accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                user_query TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
        conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_chat_to_db(username, user_query, ai_response):
    with sqlite3.connect("accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (username, user_query, ai_response) 
            VALUES (?, ?, ?)
        """, (username, user_query, ai_response))
        conn.commit()

def get_user_chat_history(username):
    with sqlite3.connect("accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_query, ai_response 
            FROM chat_history 
            WHERE username = ?
        """, (username,))
        return cursor.fetchall()


def authenticate_user(username, password):
    with sqlite3.connect("accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE username = ? AND password = ?
        """, (username, hash_password(password)))
        return cursor.fetchone() is not None


def register_user(username, password):
    with sqlite3.connect("accounts.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password) VALUES (?, ?)
            """, (username, hash_password(password)))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


init_db()

if "username" not in st.session_state:
    st.session_state.username = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Chat Bot", page_icon="💀")

st.title("Chat Bot 💀")


if not st.session_state.username:
    st.sidebar.title("Login/Register")

    login_tab, register_tab = st.sidebar.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        st.subheader("Register")
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")
        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists.")

else:
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        st.session_state.username = None
        st.session_state.chat_history = []
        st.rerun()

    user_chat_history = get_user_chat_history(st.session_state.username)
    if user_chat_history:
        st.write("Chat History:")
        for query, response in user_chat_history:
            with st.chat_message("Human"):
                st.markdown(query)
            with st.chat_message("AI"):
                st.markdown(response)

    user_query = st.chat_input("Your message")
    if user_query:
        with st.chat_message("Human"):
            st.markdown(user_query)
            
        def get_response(query, chat_history):
            template = """
                You are a helpful assistant. Answer the following questions considering the history of the conversation:

                Chat history: {chat_history}

                User question: {user_question}
            """
            prompt = ChatPromptTemplate.from_template(template)
            llm = ChatOpenAI(model_name="gpt-4o")
            chain = prompt | llm | StrOutputParser()
            return chain.stream({
                "chat_history": chat_history,
                "user_question": query
            })
        with st.chat_message("AI"):
            ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))
        st.session_state.chat_history.append(AIMessage(ai_response))

        save_chat_to_db(st.session_state.username, user_query, ai_response)
