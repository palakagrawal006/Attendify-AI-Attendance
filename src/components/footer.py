import streamlit as st


def footer():
    st.markdown(
        """
<style>
.app-footer {
    text-align: center;
    padding: 32px 0 24px;
    font-family: "Lato", sans-serif;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
}
</style>
<div class="app-footer">© 2026 Attendify · Made for smarter classrooms</div>
""",
        unsafe_allow_html=True,
    )