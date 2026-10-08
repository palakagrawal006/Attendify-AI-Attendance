import streamlit as st


def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&family=Plus+Jakarta+Sans:wght@200..800&display=swap');

            :root {
                --bg:      #0B0C10;
                --surface: #1F2833;
                --gold:    #D4AF37;
                --text:    #FFFFFF;
                --muted:   rgba(255, 255, 255, 0.72);
                --line:    rgba(212, 175, 55, 0.35);
            }

            /* Hide Streamlit chrome */
            #MainMenu, footer, header,
            [data-testid="stDecoration"] {
                visibility: hidden;
                display: none;
            }
            

            .block-container {
                padding-top: 1.5rem !important;
            }

            .stApp {
                background: var(--bg) !important;
                color: var(--text);
            }

            h1, h2 {
                font-family: "Plus Jakarta Sans", sans-serif !important;
                font-weight: 800 !important;
                font-size: 2rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0 !important;
                color: var(--text) !important;
            }

            h3, h4, p, label, .stMarkdown {
                font-family: "Lato", sans-serif;
                color: var(--text);
            }

            /* Center content inside bordered containers (cards)
            [data-testid="stVerticalBlockBorderWrapper"] > div,
            [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
                align-items: center;
                text-align: center;
            } */

            /* ---------- Buttons: shared ---------- */
            button[kind="primary"],
            button[kind="secondary"],
            button[kind="tertiary"],
            [data-testid="stBaseButton-primary"],
            [data-testid="stBaseButton-secondary"],
            [data-testid="stBaseButton-tertiary"] {
                border-radius: 1.5rem !important;
                padding: 10px 20px !important;
                font-family: "Plus Jakarta Sans", sans-serif !important;
                font-weight: 600 !important;
                transition: all 0.25s ease-in-out !important;
            }

            /* Primary: solid gold */
            button[kind="primary"],
            [data-testid="stBaseButton-primary"] {
                background: var(--gold) !important;
                color: var(--bg) !important;
                border: 2px solid var(--gold) !important;
            }
            button[kind="primary"] p,
            [data-testid="stBaseButton-primary"] p {
                color: var(--bg) !important;
            }

            /* Secondary: gold outline */
            button[kind="secondary"],
            [data-testid="stBaseButton-secondary"] {
                background: transparent !important;
                color: var(--text) !important;
                border: 2px solid var(--gold) !important;
            }
            button[kind="secondary"] p,
            [data-testid="stBaseButton-secondary"] p {
                color: var(--text) !important;
            }

            /* Tertiary: quiet */
            button[kind="tertiary"],
            [data-testid="stBaseButton-tertiary"] {
                background: transparent !important;
                color: var(--text) !important;
                border: 2px solid var(--line) !important;
            }
            button[kind="tertiary"] p,
            [data-testid="stBaseButton-tertiary"] p {
                color: var(--text) !important;
            }

            /* ---------- Hover ---------- */
            button[kind="primary"]:hover,
            [data-testid="stBaseButton-primary"]:hover {
                background: var(--text) !important;
                border-color: var(--text) !important;
                transform: scale(1.05) !important;
            }
            button[kind="primary"]:hover p,
            [data-testid="stBaseButton-primary"]:hover p {
                color: var(--bg) !important;
            }

            button[kind="secondary"]:hover,
            [data-testid="stBaseButton-secondary"]:hover {
                background: var(--gold) !important;
                transform: scale(1.05) !important;
            }
            button[kind="secondary"]:hover p,
            [data-testid="stBaseButton-secondary"]:hover p {
                color: var(--bg) !important;
            }

            button[kind="tertiary"]:hover,
            [data-testid="stBaseButton-tertiary"]:hover {
                border-color: var(--gold) !important;
                transform: scale(1.05) !important;
            }
            button[kind="tertiary"]:hover p,
            [data-testid="stBaseButton-tertiary"]:hover p {
                color: var(--gold) !important;
            }
        </style>
    """, unsafe_allow_html=True)