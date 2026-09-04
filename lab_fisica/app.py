import textwrap
import streamlit as st

# ==========================================
# IMPORTACIÓN DE LOS MÓDULOS DEL PROYECTO
# ==========================================

import modulo_vectores_2d


# ==========================================
# FUNCIÓN AUXILIAR PARA APLICAR ESTILOS VISUALES
# ==========================================
def _md_html(html: str):
    """
    # Esta función soluciona un problema de Streamlit:
    # Cuando escribimos código de diseño (HTML/CSS) dentro de Python, si tiene espacios al inicio,
    # Streamlit se confunde y lo muestra como texto feo en lugar de aplicar el diseño.
    'textwrap.dedent' quita esos espacios extra para que el diseño neón se aplique perfectamente.
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


# ==========================================
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA WEB
# ==========================================
# # Le decimos a la aplicación cómo debe mostrarse en la pestaña del navegador web.
st.set_page_config(
    page_title="Laboratorio Virtual de Física Mecánica",  # # Nombre que sale en la pestaña del navegador
    page_icon="⚛️",                                      # # Ícono que acompaña al título
    layout="wide",                                        # # Hace que la página use todo el ancho de la pantalla (modo ancho)
    initial_sidebar_state="expanded",                     # # La barra lateral izquierda aparecerá abierta por defecto
)


# ==========================================
# 2. CSS PERSONALIZADO — TEMA OSCURO FUTURISTA / NEÓN
# ==========================================
def inject_custom_css():
    """
    # Esta función inyecta las reglas de diseño visual (CSS) para transformar el aspecto predeterminado de Streamlit
    # en una interfaz moderna de laboratorio: fondo oscuro, bordes neón brillantes y cajas de cristal (glassmorphism).
    """
    css = """
        <style>

        /* ---------- IMPORTAR TIPOGRAFÍA DESDE GOOGLE FONTS ---------- */
        /* # Traemos dos fuentes tipográficas de aspecto futurista y técnico: Orbitron (para títulos) y Rajdhani (para texto) */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

        /* ---------- VARIABLES DE COLOR (PALETA DE COLORES) ---------- */
        /* # Definimos los colores principales en un solo lugar para usarlos fácilmente en toda la app */
        :root {
            --bg-primary: #0B0F19;         /* # Azul muy oscuro casi negro para el fondo principal */
            --bg-secondary: #10182B;       /* # Azul oscuro para paneles secundarios */
            --neon-blue: #00F0FF;          /* # Azul cian neón para resaltar elementos activos */
            --neon-blue-soft: rgba(0, 240, 255, 0.15); /* # Azul neón suave e iluminado */
            --neon-blue-border: rgba(0, 240, 255, 0.35); /* # Color brillante para bordes */
            --text-primary: #E6F1FF;       /* # Blanco azulejo para que las letras se lean bien en fondo oscuro */
            --text-secondary: #8FA3C0;     /* # Gris azulado para textos secundarios y notas pequeñas */
        }

        /* ---------- FONDO GENERAL DE LA APLICACIÓN ---------- */
        /* # Crea un degradado circular en el fondo que da la sensación de una pantalla encendida de laboratorio */
        .stApp {
            background: radial-gradient(circle at 15% 0%, #101a30 0%, #0B0F19 45%, #05070c 100%);
            color: var(--text-primary);
            font-family: 'Rajdhani', sans-serif;
        }

        /* ---------- ESTILO DE LOS TÍTULOS ---------- */
        /* # Le da a todos los títulos la letra 'Orbitron' con un resplandor azul neón tipo pantalla holográfica */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: var(--text-primary);
            text-shadow: 0 0 12px rgba(0, 240, 255, 0.35);
            letter-spacing: 1px;
        }

        /* # El título principal H1 tiene un degradado de color que va de azul neón a morado */
        h1 {
            background: linear-gradient(90deg, #00F0FF, #7B61FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* # Todos los párrafos, etiquetas y listas usarán la letra 'Rajdhani' */
        p, span, label, li, div {
            font-family: 'Rajdhani', sans-serif;
        }

        /* ---------- ESTILO DE LA BARRA LATERAL (SIDEBAR) ---------- */
        /* # Diseña el panel izquierdo de navegación con bordes brillantes y sombras neón */
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

        /* ---------- CAJAS CON EFECTO DE CRISTAL (GLASSMORPHISM) ---------- */
        /* # Crea tarjetas semitransparentes que parecen paneles de vidrio con bordes de neón */
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

        /* # Cuando el usuario pasa el cursor sobre la tarjeta, esta brilla más y flota levemente */
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

        /* ---------- BOTONES INTERACTIVOS ---------- */
        /* # Personaliza los botones para que parezcan botones táctiles de una consola futurista */
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

        /* # Efecto de brillo intenso al pasar el ratón sobre los botones */
        .stButton > button:hover {
            border: 1px solid var(--neon-blue);
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.45);
            color: #FFFFFF;
            transform: scale(1.02);
        }

        /* ---------- OPCIONES DE MENÚ DE NAVEGACIÓN ---------- */
        /* # Le da forma de tarjeta seleccionable a las opciones del menú de la barra lateral */
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

        /* ---------- PESTAÑAS (TABS) ---------- */
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

        /* ---------- ALERTAS / MENSAJES DE INFORMACIÓN ---------- */
        div[data-testid="stNotification"] {
            background: rgba(0, 240, 255, 0.06);
            border: 1px solid var(--neon-blue-border);
            border-radius: 12px;
            backdrop-filter: blur(8px);
        }

        /* ---------- BARRA DE DESLIZAMIENTO (SLIDERS) ---------- */
        /* # Pinta los controles deslizantes numéricos del color neón principal */
        div[data-testid="stSlider"] > div > div > div > div {
            background-color: var(--neon-blue) !important;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
        }

        /* ---------- BARRA DE DESPLAZAMIENTO (SCROLLBAR) ---------- */
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

        /* ---------- LÍNEA SEPARADORA GLOW/NEÓN ---------- */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
            margin: 1.5rem 0;
        }

        /* ---------- CRÉDITOS AL FINAL DE LA BARRA LATERAL ---------- */
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
    # # Llamamos a la función auxiliar para inyectar todo este estilo CSS a la pantalla
    _md_html(css)


# ==========================================
# 3. CONSTRUCCIÓN DE LA BARRA LATERAL (SIDEBAR)
# ==========================================
def render_sidebar():
    """
    # Esta función dibuja todo lo que está en la barra izquierda:
    # El título del proyecto, el menú con los 3 módulos y la lista de integrantes.
    # Devuelve cuál módulo seleccionó el usuario para mostrarlo en pantalla.
    """

    with st.sidebar:
        # # Dibujamos el encabezado de la barra lateral usando HTML estilizado
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

        # # 'st.radio' crea los botones de selección múltiple para cambiar entre laboratorios
        menu_opcion = st.radio(
            label="Selecciona un módulo:",
            options=[
                "Módulo 1: Vectores en 2D",
                "Módulo 2: Cinemática (Tiro Parabólico)",
                "Módulo 3: Dinámica (Plano Inclinado)",
            ],
            label_visibility="collapsed",  # # Ocultamos la etiqueta del menú porque ya pusimos un título arriba
        )

        _md_html("<hr>")

        # # Bloque que muestra la lista de los integrantes del equipo
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

    # # Retornamos la opción que eligió el usuario (ej. "Módulo 1: Vectores en 2D")
    return menu_opcion


# ==========================================
# 4. COMPONENTE REUTILIZABLE: TARJETA GLASSMORPHISM
# ==========================================
def glass_card(header: str, subtext: str = ""):
    """
    # Esta función es un 'molde' para crear tarjetas tipo vidrio en cualquier parte del código.
    # Recibe el título principal (header) y la descripción (subtext).
    """
    _md_html(
        f"""
        <div class="glass-card">
            <div class="glass-header">{header}</div>
            <div class="glass-subtext">{subtext}</div>
        </div>
        """
    )


# ==========================================
# 6. MÓDULO 2: CINEMÁTICA (TIRO PARABÓLICO)
# ==========================================
def modulo_cinematica_tiro_parabolico():
    """
    # Pantalla temporal para el Módulo 2.
    # Muestra un mensaje informando que se encuentra en desarrollo.
    """
    glass_card(
        header="🚀 Módulo 2 — Cinemática: Tiro Parabólico",
        subtext="Análisis de trayectoria, alcance máximo y tiempo de vuelo.",
    )

    st.info("🚧 Próximamente: simulación interactiva de tiro parabólico.")


# ==========================================
# 7. MÓDULO 3: DINÁMICA (PLANO INCLINADO)
# ==========================================
def modulo_dinamica_plano_inclinado():
    """
    # Pantalla temporal para el Módulo 3.
    # Muestra un mensaje informando que se encuentra en desarrollo.
    """
    glass_card(
        header="⚙️ Módulo 3 — Dinámica: Plano Inclinado",
        subtext="Fuerzas, fricción y aceleración de un cuerpo sobre un plano inclinado.",
    )

    st.info("🚧 Próximamente: simulación interactiva de plano inclinado.")


# ==========================================
# 8. FUNCIÓN PRINCIPAL DE LA APLICACIÓN (main)
# ==========================================
def main():
    """
    # Es el motor principal del programa. Se ejecuta de arriba hacia abajo:
    # 1. Aplica los colores y estilos neón.
    # 2. Dibuja el título de la parte superior.
    # 3. Carga la barra lateral y detecta el módulo seleccionado.
    # 4. Carga en pantalla el laboratorio que el usuario quiere ver.
    """
    # # Aplica el CSS neón a toda la app
    inject_custom_css()

    # # Dibuja el título principal en el centro de la pantalla
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

    # # Renderiza la barra lateral y guarda la elección del usuario en la variable 'opcion'
    opcion = render_sidebar()

    # # EVALUACIÓN DE RUTAS: Según lo que seleccionó el usuario, ejecuta el módulo correspondiente
    if opcion == "Módulo 1: Vectores en 2D":
        # # Llama al archivo 'modulo_vectores_2d.py' para mostrar la gráfica y los controles de vectores
        modulo_vectores_2d.modulo_vectores_2d()
        
    elif opcion == "Módulo 2: Cinemática (Tiro Parabólico)":
        # # Muestra la vista previa del Módulo 2
        modulo_cinematica_tiro_parabolico()
        
    elif opcion == "Módulo 3: Dinámica (Plano Inclinado)":
        # # Muestra la vista previa del Módulo 3
        modulo_dinamica_plano_inclinado()


# ==========================================
# PUNTO DE ENTRADA DEL ARCHIVO
# ==========================================
# # Esta línea le indica a Python que si ejecutamos este archivo directamente,
# # debe arrancar llamando a la función 'main()'.
if __name__ == "__main__":
    main()