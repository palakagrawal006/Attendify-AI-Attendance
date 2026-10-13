import streamlit as st
from pathlib import Path
from src.components.header import header
from src.components.footer import footer
from src.ui.style_base_layout import style_base_layout


def home_style():
    css = (Path(__file__).parent.parent / "ui" / "home.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def home_screen():
    header()
    style_base_layout()
    home_style()

#     st.markdown(
#         """
# <div class="home-hero">
# <div class="home-badge">AI-POWERED ATTENDANCE</div>
# <div class="home-title">Smarter Attendance.<br>Simpler <span>Classrooms.</span></div>
# <div class="home-description">AI-powered attendance using face and voice recognition — built for modern classrooms.</div>
# </div>
# """,
#         unsafe_allow_html=True,
#     )

    _, mid, _ = st.columns([1, 6, 1])
    with mid:
        c1, c2 = st.columns(2, gap="large")

        with c1:
            with st.container(border=True, key="card_teacher"):
                st.markdown(
                    '<div class="portal-body">'
                    '<div class="portal-icon">👩‍🏫</div>'
                    '<div class="portal-title">For Teachers</div>'
                    '<div class="portal-text">Create classes, take attendance by face or voice, and view reports.</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                if st.button("Teacher Portal →", key="teacher", type="primary", width="stretch"):
                    st.session_state["login_type"] = "teacher"
                    st.rerun()

        with c2:
            with st.container(border=True, key="card_student"):
                st.markdown(
                    '<div class="portal-body">'
                    '<div class="portal-icon">🎓</div>'
                    '<div class="portal-title">For Students</div>'
                    '<div class="portal-text">Check your attendance, mark yourself present, and track your record.</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                if st.button("Student Portal →", key="student", type="secondary", width="stretch"):
                    st.session_state["login_type"] = "student"
                    st.rerun()

#     st.markdown(
#         """
# <div class="feature-strip">
# <div class="feature"><b>Face recognition</b><span>Mark a whole class in seconds</span></div>
# <div class="feature"><b>Voice recognition</b><span>Hands-free roll call</span></div>
# <div class="feature"><b>Instant reports</b><span>Attendance insights, always ready</span></div>
# </div>
# """,
#         unsafe_allow_html=True,
#     )

    footer()