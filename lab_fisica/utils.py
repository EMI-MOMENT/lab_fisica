import textwrap
import streamlit as st

def _md_html(html: str):
    """Renderiza HTML/CSS de forma limpia en Streamlit."""
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

def glass_card(header: str = "", subtext: str = "", contenido_html: str = ""):
    """Renderiza una tarjeta futurista tipo glassmorphism."""
    html = f"""
    <div class="glass-card" style="
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    ">
    """
    if header:
        html += f'<div class="glass-header" style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">{header}</div>'
    if subtext:
        html += f'<div class="glass-subtext" style="color: #8FA3C0; font-size: 0.9rem; margin-bottom: 10px;">{subtext}</div>'
    if contenido_html:
        html += f'<div>{contenido_html}</div>'
    
    html += "</div>"
    _md_html(html)