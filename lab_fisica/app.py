import textwrap
import streamlit as st

#IMPORTACION DE LOS MODULOS
import modulo_vectores_2d

def _md_html(html: str):
    """Renderiza HTML/CSS con st.markdown de forma segura.

    Streamlit (y el parser Markdown que usa por debajo) interpreta cualquier
    línea que empiece con 4 o más espacios como un BLOQUE DE CÓDIGO en vez de
    HTML. Como en este archivo las cadenas HTML/CSS están sangradas para
    respetar la identación de Python, hay que "desindentarlas" con
    textwrap.dedent() antes de enviarlas, o de lo contrario se muestran como
    texto plano en pantalla en lugar de aplicarse como estilo.
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA

st.set_page_config(
    page_title="Laboratorio Virtual de Física Mecánica",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2. CSS PERSONALIZADO — TEMA OSCURO FUTURISTA / NEÓN
def inject_custom_css():
    """Inyecta el CSS personalizado para el tema oscuro futurista con
    detalles en azul neón y cajas tipo glassmorphism."""
    css = """
        <style>

        /* ---------- IMPORTAR TIPOGRAFÍA ---------- */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

        :root {
            --bg-primary: #0B0F19;
            --bg-secondary: #10182B;
            --neon-blue: #00F0FF;
            --neon-blue-soft: rgba(0, 240, 255, 0.15);
            --neon-blue-border: rgba(0, 240, 255, 0.35);
            --text-primary: #E6F1FF;
            --text-secondary: #8FA3C0;
        }

        /* ---------- FONDO GENERAL DE LA APP ---------- */
        .stApp {
            background: radial-gradient(circle at 15% 0%, #101a30 0%, #0B0F19 45%, #05070c 100%);
            color: var(--text-primary);
            font-family: 'Rajdhani', sans-serif;
        }

        /* ---------- TÍTULOS ---------- */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: var(--text-primary);
            text-shadow: 0 0 12px rgba(0, 240, 255, 0.35);
            letter-spacing: 1px;
        }

        h1 {
            background: linear-gradient(90deg, #00F0FF, #7B61FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p, span, label, li, div {
            font-family: 'Rajdhani', sans-serif;
        }

        /* ---------- SIDEBAR ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0D1220 0%, #080B14 100%);
            border-right: 1px solid var(--neon-blue-border);
            box-shadow: 4px 0 25px rgba(0, 240, 255, 0.08);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: var(--neon-blue);
        }

        /* ---------- CAJAS GLASSMORPHISM ---------- */
        .glass-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--neon-blue-border);
            border-radius: 18px;
            padding: 1.6rem 1.8rem;
            box-shadow: 0 0 25px rgba(0, 240, 255, 0.08),
                        inset 0 0 40px rgba(0, 240, 255, 0.03);
            margin-bottom: 1.2rem;
            transition: all 0.3s ease-in-out;
        }

        .glass-card:hover {
            border: 1px solid var(--neon-blue);
            box-shadow: 0 0 35px rgba(0, 240, 255, 0.25),
                        inset 0 0 50px rgba(0, 240, 255, 0.05);
            transform: translateY(-2px);
        }

        .glass-header {
            font-family: 'Orbitron', sans-serif;
            color: var(--neon-blue);
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        }

        .glass-subtext {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        /* ---------- BOTONES ---------- */
        .stButton > button {
            background: linear-gradient(90deg, rgba(0,240,255,0.12), rgba(123,97,255,0.12));
            color: var(--neon-blue);
            border: 1px solid var(--neon-blue-border);
            border-radius: 10px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            letter-spacing: 1px;
            padding: 0.5rem 1.2rem;
            transition: all 0.25s ease-in-out;
        }

        .stButton > button:hover {
            border: 1px solid var(--neon-blue);
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.45);
            color: #FFFFFF;
            transform: scale(1.02);
        }

        /* ---------- RADIO / MENÚ DE NAVEGACIÓN (SIDEBAR) ---------- */
        div[role="radiogroup"] > label {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(0, 240, 255, 0.15);
            border-radius: 10px;
            padding: 0.6rem 0.8rem;
            margin-bottom: 0.5rem;
            transition: all 0.2s ease-in-out;
            width: 100%;
        }

        div[role="radiogroup"] > label:hover {
            border: 1px solid var(--neon-blue);
            background: rgba(0, 240, 255, 0.06);
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        }

        /* ---------- TABS NATIVOS (por si se usan) ---------- */
        button[data-baseweb="tab"] {
            font-family: 'Orbitron', sans-serif;
            color: var(--text-secondary);
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--neon-blue) !important;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
        }

        div[data-baseweb="tab-highlight"] {
            background-color: var(--neon-blue) !important;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.8);
        }

        /* ---------- ALERTAS / st.info, st.warning, etc ---------- */
        div[data-testid="stNotification"] {
            background: rgba(0, 240, 255, 0.06);
            border: 1px solid var(--neon-blue-border);
            border-radius: 12px;
            backdrop-filter: blur(8px);
        }

        /* ---------- SLIDERS ---------- */
        div[data-testid="stSlider"] > div > div > div > div {
            background-color: var(--neon-blue) !important;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
        }

        /* ---------- SCROLLBAR ---------- */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #0B0F19;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 240, 255, 0.35);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 240, 255, 0.6);
        }

        /* ---------- SEPARADOR NEÓN ---------- */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
            margin: 1.5rem 0;
        }

        /* ---------- FOOTER / CRÉDITOS EN SIDEBAR ---------- */
        .sidebar-footer {
            font-size: 0.8rem;
            color: var(--text-secondary);
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(0, 240, 255, 0.15);
        }

        </style>
        """
    _md_html(css)


# 3. BARRA LATERAL (SIDEBAR)

def render_sidebar():
    """Construye la barra lateral: título, créditos y menú de navegación.
    Retorna la opción de módulo seleccionada por el usuario."""

    with st.sidebar:
        _md_html(
            """
            <div style="text-align:center; padding: 0.5rem 0 1.2rem 0;">
                <h1 style="font-size:1.6rem; margin-bottom:0;">⚛️ LAB FÍSICA</h1>
                <p style="color:#8FA3C0; font-size:0.85rem; letter-spacing:2px; margin-top:-8px;">
                    MECÁNICA · SIMULACIÓN INTERACTIVA
                </p>
            </div>
            <hr>
            """
        )

        st.markdown("### 🧭 Navegación")

        menu_opcion = st.radio(
            label="Selecciona un módulo:",
            options=[
                "Módulo 1: Vectores en 2D",
                "Módulo 2: Cinemática (Tiro Parabólico)",
                "Módulo 3: Dinámica (Plano Inclinado)",
            ],
            label_visibility="collapsed",
        )

        _md_html("<hr>")

        # ---------- CRÉDITOS ----------
        _md_html(
            """
            <div class="sidebar-footer">
                <b style="color:#00F0FF;">Créditos</b><br>
                Grupo de Desarrollo — Física Mecánica<br>
                <b>Integrantes:</b><br>
                • Juan Esteban Benavides Mantilla<br>
                • Nicolás Joshue Jiménez Sanabria<br>
                • Víctor Alfonso Ruiz Ferrer<br>
                • Yorguin Rolando Celis Almeida<br>
                • Iverson Stiven Herrera Jaimes<br>
                • Duvan Libardo Jimenez Rodriguez<br>
                <br>
                <span style="opacity:0.6;">v0.1 · Streamlit + Plotly</span>
            </div>
            """
        )

    return menu_opcion


# 4. COMPONENTE REUTILIZABLE: TARJETA GLASSMORPHISM
def glass_card(header: str, subtext: str = ""):
    """Renderiza una cabecera tipo tarjeta glassmorphism para
    encabezar cada módulo de forma consistente."""
    _md_html(
        f"""
        <div class="glass-card">
            <div class="glass-header">{header}</div>
            <div class="glass-subtext">{subtext}</div>
        </div>
        """
    )


# 6. MÓDULO 2: CINEMÁTICA (TIRO PARABÓLICO)
def modulo_cinematica_tiro_parabolico():
    glass_card(
        header="🚀 Módulo 2 — Cinemática: Tiro Parabólico",
        subtext="Análisis de trayectoria, alcance máximo y tiempo de vuelo.",
    )

    st.info("🚧 Próximamente: simulación interactiva de tiro parabólico.")


# 7. MÓDULO 3: DINÁMICA (PLANO INCLINADO)
def modulo_dinamica_plano_inclinado():
    glass_card(
        header="⚙️ Módulo 3 — Dinámica: Plano Inclinado",
        subtext="Fuerzas, fricción y aceleración de un cuerpo sobre un plano inclinado.",
    )

    st.info("🚧 Próximamente: simulación interactiva de plano inclinado.")


# 8. FUNCIÓN PRINCIPAL (main)
def main():
    inject_custom_css()

    # ---------- ENCABEZADO PRINCIPAL ----------
    st.markdown("# ⚛️ Laboratorio Virtual de Física Mecánica")
    _md_html(
        """
        <p style="color:#8FA3C0; margin-top:-10px;">
            Explora, simula y comprende los principios fundamentales de la mecánica clásica
            a través de módulos interactivos.
        </p>
        <hr>
        """
    )

# ---------- SIDEBAR Y SELECCIÓN DE MÓDULO ----------
    opcion = render_sidebar()

    # ---------- ENRUTAMIENTO DE MÓDULOS ----------
    if opcion == "Módulo 1: Vectores en 2D":
        modulo_vectores_2d.modulo_vectores_2d()
    elif opcion == "Módulo 2: Cinemática (Tiro Parabólico)":
        modulo_cinematica_tiro_parabolico()
    elif opcion == "Módulo 3: Dinámica (Plano Inclinado)":
        modulo_dinamica_plano_inclinado()

if __name__ == "__main__":
    main()