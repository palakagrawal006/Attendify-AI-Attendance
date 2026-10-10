# import html
# import streamlit as st


# def subject_card(name, code, section, stats=None, footer_callback=None):
   
#     with st.container(border=True, key=f"subject_card_{code}"):
#         card = (
#             f'<h3 style="margin:0; color:#FFFFFF; font-size:1.3rem; '
#             f'font-family:\'Plus Jakarta Sans\',sans-serif; font-weight:800;">{html.escape(name)}</h3>'
#             f'<p style="color:rgba(255,255,255,0.72); margin:10px 0 0;">Code : '
#             f'<span style="background:rgba(212,175,55,0.15); color:#D4AF37; padding:2px 8px; '
#             f'border-radius:5px; font-weight:700; letter-spacing:0.5px;">{html.escape(str(code))}</span>'
#             f' &nbsp;·&nbsp; Section {html.escape(str(section))}</p>'
#         )

#         if stats:
#             card += '<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:12px;">'
#             for  label, value in stats:
#                 card += (
#                     f'<div style="background:rgba(212,175,55,0.12); padding:4px 8px; margin-bottom:8px; border-radius:12px; '
#                     f'font-size:0.9rem; color:rgba(255,255,255,0.8);">'
#                     f' <b style="color:##D4AF37;">{value}</b> {html.escape(str(label))}</div>'
#                 )
#             card += "</div>"

#         st.markdown(card, unsafe_allow_html=True)

#         if footer_callback:
#             footer_callback()
            
import html
import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    with st.container(border=True, key=f"subject_card_{code}"):
        left, mid, right = st.columns([5, 3, 2.5], vertical_alignment="center")

        with left:
            st.markdown(
                f'<div style="font-size:1.1rem; font-weight:800; color:#FFFFFF; '
                f'font-family:\'Plus Jakarta Sans\',sans-serif;">{html.escape(name)}</div>'
                f'<div style="margin-top:4px; font-size:0.85rem; color:rgba(255,255,255,0.72);">'
                f'<span style="background:rgba(212,175,55,0.15); color:#D4AF37; padding:1px 7px; '
                f'border-radius:5px; font-weight:700; letter-spacing:0.5px;">{html.escape(str(code))}</span>'
                f' &nbsp;·&nbsp; Section {html.escape(str(section))}</div>',
                unsafe_allow_html=True,
            )

        with mid:
            chips = "".join(
                f'<div style="background:rgba(212,175,55,0.12); padding:4px 11px; border-radius:12px; '
                f'font-size:0.85rem; color:rgba(255,255,255,0.8);">'
                f'<b style="color:#D4AF37;">{value}</b> {html.escape(str(label))}</div>'
                for label, value in (stats or [])
            )
            st.markdown(
                f'<div style="display:flex; gap:8px; flex-wrap:wrap;">{chips}</div>',
                unsafe_allow_html=True,
            )

        with right:
            if footer_callback:
                footer_callback()