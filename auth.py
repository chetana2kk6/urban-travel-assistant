import streamlit as st
import json
import os

USER_FILE = "users.json"


# ---------- USER STORAGE ----------
def load_users():

    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):

    with open(USER_FILE, "w") as f:
        json.dump(users, f)


# ---------- LOGIN PAGE ----------
def login():

    users = load_users()

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # HERO HEADER
    st.markdown("""
    <div class="hero">
    <h1>Urban Travel Assistant</h1>
    <p>Plan your trips intelligently with AI assistance.</p>
    </div>
    """, unsafe_allow_html=True)


    # ---------------- LOGIN FORM ----------------
    if st.session_state.auth_mode == "login":

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        remember = st.checkbox("Remember me")

        if st.button("Sign in"):

            if username in users and users[username] == password:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()

            else:
                st.error("Invalid username or password")

        st.write("")

        if st.button("Don't have an account? Sign Up"):
            st.session_state.auth_mode = "signup"
            st.rerun()


    # ---------------- SIGNUP FORM ----------------
    elif st.session_state.auth_mode == "signup":

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            st.subheader("Create Account")

            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")

            if st.button("Create Account"):

                if new_user in users:
                    st.error("Username already exists")

                elif new_pass != confirm:
                    st.error("Passwords do not match")

                elif new_user == "" or new_pass == "":
                    st.warning("Fill all fields")

                else:

                    users[new_user] = new_pass
                    save_users(users)

                    st.success("Account created successfully!")
                    st.session_state.auth_mode = "login"
                    st.rerun()

            if st.button("Back to Login"):
                st.session_state.auth_mode = "login"
                st.rerun()