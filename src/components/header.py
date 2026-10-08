import streamlit as st


def header():
    st.markdown(
        """
<style>
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 0;
    border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}
.app-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.app-logo-mark {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: #D4AF37;
    color: #0B0C10;
    font-size: 20px;
    font-weight: 800;
    line-height: 1;
}
.app-logo {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    line-height: 1;
}
.app-logo span {
    color: #D4AF37;
}
.app-tag {
    font-family: "Lato", sans-serif;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    letter-spacing: 0.3px;
}
.app-tag b {
    color: #D4AF37;
    font-weight: 700;
}
</style>
<div class="app-header">
<div class="app-brand">
<div class="app-logo-mark">✓</div>
<div class="app-logo">Attend<span>ify</span></div>
</div>
<div class="app-tag"><b>Face</b> · <b>Voice</b> · Reports</div>
</div>
""",
        unsafe_allow_html=True,
    )