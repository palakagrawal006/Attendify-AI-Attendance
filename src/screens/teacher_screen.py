import streamlit as st
from pathlib import Path
from src.components.header import header   # make sure this name matches header.py
from src.components.footer import footer
from src.ui.style_base_layout import style_base_layout
from src.database.db import create_teacher, check_teacher_exists, teacher_login

def auth_style():
    css = (Path(__file__).parent.parent / "ui" / "auth.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def set_mode(mode):
    st.session_state["teacher_mode"] = mode


def go_home():
    st.session_state["login_type"] = None


def register_form():
    st.markdown(
        """
<div class="auth-head">
<div class="auth-badge">TEACHER PORTAL</div>
<div class="auth-title">Register your <span>teacher</span> profile</div>
<div class="auth-sub">Create an account to start taking attendance by face and voice.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.container(border=True, key="card_auth"):
        username = st.text_input("Username", placeholder="@palak", key="reg_username")
        name = st.text_input("Full name", placeholder="Palak Agrawal", key="reg_name")
        password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="reg_password")
        confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter your password", key="reg_confirm")

        st.markdown('<div class="auth-divider"></div>', unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            register = st.button("Register", type="primary", width="stretch", key="reg_submit", icon=":material/person_add:")
            
        with b2:
            st.button("Login instead", type="secondary", width="stretch",
                      key="to_login", icon=":material/login:",
                      on_click=set_mode, args=("login",))

        if register:
            if not (username and name and password and confirm):
                st.error("Fill in all the fields.")
            elif(check_teacher_exists(username)) :
                st.error("Username already taken")
            elif len(password) < 8:
                st.error("Your password needs at least 8 characters.")
            elif password != confirm:
                st.error("The passwords don't match.")
            else:
                try:
                    create_teacher(username, password, name)
                    st.toast("Profile created. You can log in now.")
                    
                    st.session_state.teacher_mode = "login"
                    st.rerun()
                    
                except Exception as e:
                    st.error(str(e))


def login_form():
    st.markdown(
        """
<div class="auth-head">
<div class="auth-badge">TEACHER PORTAL</div>
<div class="auth-title">Welcome <span>back</span></div>
<div class="auth-sub">Log in to manage your classes and attendance.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.container(border=True, key="card_auth"):
        username = st.text_input("Username", placeholder="@palak", key="log_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="log_password")

        st.markdown('<div class="auth-divider"></div>', unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            login = st.button("Login", type="primary", width="stretch",
                              key="log_submit", icon=":material/login:")
        with b2:
            st.button("Register instead", type="secondary", width="stretch",
                      key="to_register", icon=":material/person_add:",
                      on_click=set_mode, args=("register",))

        if login:
            if not (username and password):
                st.error("Enter your username and password.")
            else:
                teacher_data = teacher_login(username, password) 
                
                if teacher_data:
                    st.session_state.user_role = 'teacher'
                    st.session_state.teacher_data = teacher_data
                    st.session_state.is_logged_in = True
                    st.toast("Logged in.")
                    st.rerun()
                    
                else:
                    st.error("Invalid username or password")
        
        
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.header(f"""Welcome {teacher_data['name']}""")
    

def teacher_screen():
    header()
    style_base_layout()
    auth_style()

    # back link: top-left, under the header, in its own narrow row
    back_col, _ = st.columns([1, 5])
    with back_col:
        st.button("Back to home", key="back_home", type="tertiary",
                  icon=":material/arrow_back:", on_click=go_home)
 
    # form: centered column
    _, mid, _ = st.columns([1, 3, 1])
    with mid:
        if "teacher_data" in st.session_state :
            teacher_dashboard() 
        elif st.session_state.get("teacher_mode", "login") == "register":
            register_form()
        else:
            login_form()

    footer()