import textwrap
import streamlit as st

# ==========================================
# CAPA DE UTILIDADES COMPARTIDAS (UI CORE)
# ==========================================

def _md_html(html: str):
    """
    Inyector de HTML crudo para Streamlit.
    Recibe un string de marcado, limpia los espacios en blanco iniciales de cada 
    línea generados por la identación de Python (textwrap.dedent) y fuerza su 
    evaluación HTML bypassando el formateo seguro de Markdown.
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

def glass_card(header: str = "", subtext: str = "", contenido_html: str = ""):
    """
    Componente de UI reutilizable basado en diseño Glassmorphism.
    Genera un contenedor translúcido con desenfoque de fondo y estilo neón.
    
    Args:
        header: Texto principal de la tarjeta.
        subtext: Descripción o subtítulo complementario.
        contenido_html: Carga útil interna en HTML (opcional).
    """
    # Base CSS en línea
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
    
    # Renderizado condicional de componentes internos
    if header:
        html += f'<div class="glass-header" style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">{header}</div>'
    if subtext:
        html += f'<div class="glass-subtext" style="color: #8FA3C0; font-size: 0.9rem; margin-bottom: 10px;">{subtext}</div>'
    if contenido_html:
        html += f'<div>{contenido_html}</div>'
    
    html += "</div>"
    _md_html(html)