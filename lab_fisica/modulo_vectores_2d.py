import math

import streamlit as st
import plotly.graph_objects as go

from utils import _md_html, glass_card

# ============================================================
# PALETA DE COLORES
# ============================================================
COLOR_A = "#00F0FF"   # Cyan neón — Vector A
COLOR_B = "#FF2EC4"   # Rosa neón — Vector B
COLOR_R = "#00FF66"   # Verde neón — Vector Resultante (Suma o Resta)
COLOR_TEXTO_SEC = "#8FA3C0"


# ============================================================
# HELPERS INTERNOS
# ============================================================
def _tarjeta_resultado(titulo: str, valor: str, color: str = "#00F0FF"):
    """Mini tarjeta glassmorphism para un resultado numérico individual."""
    _md_html(
        f"""
        <div class="glass-card" style="padding:1rem 1.2rem; text-align:center; margin-bottom:0;">
            <div class="glass-subtext" style="font-size:0.78rem; letter-spacing:1px; text-transform:uppercase;">
                {titulo}
            </div>
            <div style="font-family:'Orbitron', sans-serif; font-size:1.5rem; color:{color};
                        text-shadow:0 0 12px {color}66; margin-top:0.3rem;">
                {valor}
            </div>
        </div>
        """
    )


def _crear_flecha_vector(fig, origen, destino, color, nombre, ancho=4):
    """Agrega un vector como línea + punta de flecha (annotation) a una figura Plotly."""
    ox, oy = origen
    dx, dy = destino

    fig.add_trace(
        go.Scatter(
            x=[ox, dx],
            y=[oy, dy],
            mode="lines",
            line=dict(color=color, width=ancho),
            name=nombre,
            hovertemplate=f"{nombre}<br>x=%{{x:.2f}}<br>y=%{{y:.2f}}<extra></extra>",
        )
    )

    fig.add_annotation(
        x=dx, y=dy, ax=ox, ay=oy,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.6,
        arrowwidth=ancho * 0.6,
        arrowcolor=color,
    )


def _componente_input(label: str, key_prefix: str, default: float, color: str):
    """Renderiza un par slider + number_input SINCRONIZADOS bidireccionalmente."""
    slider_key = f"{key_prefix}_slider"
    num_key = f"{key_prefix}_num"

    if slider_key not in st.session_state:
        st.session_state[slider_key] = default
    if num_key not in st.session_state:
        st.session_state[num_key] = default

    def _on_slider_change():
        st.session_state[num_key] = st.session_state[slider_key]

    def _on_num_change():
        st.session_state[slider_key] = st.session_state[num_key]

    _md_html(
        f"""
        <div style="color:{color}; font-family:'Rajdhani', sans-serif;
                    font-weight:600; font-size:0.85rem; letter-spacing:0.5px;
                    margin-bottom:-0.6rem;">
            {label}
        </div>
        """
    )

    col_slider, col_num = st.columns([3, 1.3])
    with col_slider:
        st.slider(
            label, min_value=-10.0, max_value=10.0, step=0.1,
            key=slider_key, on_change=_on_slider_change,
            label_visibility="collapsed",
        )
    with col_num:
        st.number_input(
            label, min_value=-10.0, max_value=10.0, step=0.1,
            key=num_key, on_change=_on_num_change,
            label_visibility="collapsed",
        )

    return st.session_state[slider_key]


# ============================================================
# FUNCIONES MATEMÁTICAS AUXILIARES
# ============================================================
def _mag_ang(x: float, y: float):
    mag = math.hypot(x, y)                 # CÁLCULO: Magnitud |V| = √(x² + y²) usando el Teorema de Pitágoras
    ang = math.degrees(math.atan2(y, x))   # CÁLCULO: Dirección θ = arctan(y/x) convertida de radianes a grados sexagesimales
    if ang < 0:
        ang += 360                         # CÁLCULO: Ajuste de ángulo negativo -> θ = θ + 360° para mantener rango [0°, 360°)
    return mag, ang


def _explicacion_cuadrante(rx: float, ry: float) -> str:
    if rx >= 0 and ry >= 0:                # CÁLCULO LOGICO: (+, +) -> Cuadrante I (0° a 90°)
        return "Como Rx ≥ 0 y Ry ≥ 0, el vector resultante cae en el <b>Cuadrante I</b> (0°–90°)."
    elif rx < 0 and ry >= 0:               # CÁLCULO LOGICO: (−, +) -> Cuadrante II (90° a 180°)
        return "Como Rx &lt; 0 y Ry ≥ 0, el vector resultante cae en el <b>Cuadrante II</b> (90°–180°)."
    elif rx < 0 and ry < 0:                # CÁLCULO LOGICO: (−, −) -> Cuadrante III (180° a 270°)
        return "Como Rx &lt; 0 y Ry &lt; 0, el vector resultante cae en el <b>Cuadrante III</b> (180°–270°)."
    else:                                  # CÁLCULO LOGICO: (+, −) -> Cuadrante IV (270° a 360°)
        return "Como Rx ≥ 0 y Ry &lt; 0, el vector resultante cae en el <b>Cuadrante IV</b> (270°–360°)."


# ============================================================
# FUNCIÓN PRINCIPAL DEL MÓDULO
# ============================================================
def modulo_vectores_2d():
    glass_card(
        header="📐 Módulo 1 — Vectores en 2D",
        subtext="Suma, resta, producto escalar y producto cruz de vectores en el plano cartesiano.",
    )

    # ------------------------------------------------------------
    # 1. CONTROLES DE ENTRADA
    # ------------------------------------------------------------
    _md_html(
        """
        <div class="glass-card" style="margin-bottom:0.8rem;">
            <div class="glass-header" style="font-size:1.05rem;">🎛️ Componentes de los vectores</div>
            <div class="glass-subtext">Ajusta con el slider o escribe el valor exacto — ambos se sincronizan al instante.</div>
        </div>
        """
    )

    col_a, col_b = st.columns(2)

    with col_a:
        _md_html(
            f"""
            <div style="color:{COLOR_A}; font-family:'Orbitron', sans-serif;
                        font-size:0.95rem; margin-bottom:0.3rem; letter-spacing:1px;">
                ⬤ VECTOR A
            </div>
            """
        )
        ax = _componente_input("Ax", "ax", 6.0, COLOR_A)
        ay = _componente_input("Ay", "ay", 4.0, COLOR_A)

    with col_b:
        _md_html(
            f"""
            <div style="color:{COLOR_B}; font-family:'Orbitron', sans-serif;
                        font-size:0.95rem; margin-bottom:0.3rem; letter-spacing:1px;">
                ⬤ VECTOR B
            </div>
            """
        )
        bx = _componente_input("Bx", "bx", -3.0, COLOR_B)
        by = _componente_input("By", "by", 5.0, COLOR_B)

    # ------------------------------------------------------------
    # 2. MOTOR DE CÁLCULO VECTORIAL (CÁLCULOS QUE SE MUESTRAN EN PANTALLA)
    # ------------------------------------------------------------
    mag_a, ang_a = _mag_ang(ax, ay)  # CÁLCULO: |A| = √(Ax² + Ay²)  y  θ_A = arctan(Ay/Ax) -> Muestra Magnitud e Inclinación de A
    mag_b, ang_b = _mag_ang(bx, by)  # CÁLCULO: |B| = √(Bx² + By²)  y  θ_B = arctan(By/Bx) -> Muestra Magnitud e Inclinación de B

    sum_x, sum_y = ax + bx, ay + by # CÁLCULO: Rx = Ax + Bx  |  Ry = Ay + By -> Componentes del Vector Suma (R = A + B)
    mag_sum, ang_sum = _mag_ang(sum_x, sum_y)  # CÁLCULO: |R_suma| = √(Rx² + Ry²)  y  θ_suma = arctan(Ry/Rx) -> Magnitud y Ángulo de Suma

    dif_x, dif_y = ax - bx, ay - by            # CÁLCULO: Rx = Ax − Bx  |  Ry = Ay − By -> Componentes del Vector Resta (R = A − B)
    mag_dif, ang_dif = _mag_ang(dif_x, dif_y)  # CÁLCULO: |R_resta| = √(Rx² + Ry²)  y  θ_resta = arctan(Ry/Rx) -> Magnitud y Ángulo de Resta

    producto_escalar = ax * bx + ay * by       # CÁLCULO: A · B = (Ax * Bx) + (Ay * By) -> Producto Punto / Escalar
    producto_cruz_z = ax * by - ay * bx        # CÁLCULO: (A × B)_z = (Ax * By) − (Ay * Bx) -> Producto Cruz / Determinante 

    # ------------------------------------------------------------
    # 3. SELECTOR DE RESULTANTE A GRAFICAR
    # ------------------------------------------------------------
    modo_resultante = st.radio(
        "Resultante a graficar:",
        options=["Suma (A + B)", "Resta (A − B)"],
        horizontal=True,
    )

    if modo_resultante == "Suma (A + B)":
        res_x, res_y, res_mag, res_ang, nombre_res = sum_x, sum_y, mag_sum, ang_sum, "R = A + B"
    else:
        res_x, res_y, res_mag, res_ang, nombre_res = dif_x, dif_y, mag_dif, ang_dif, "R = A − B"

    # ------------------------------------------------------------
    # 4. GRÁFICO PLOTLY Y ESCALADO DINÁMICO INTERFAZ
    # ------------------------------------------------------------
    fig = go.Figure()

    limite = max(abs(ax), abs(ay), abs(bx), abs(by), abs(res_x), abs(res_y), 1) * 1.35
# CÁLCULO: Límite = Máximo(|Ax|, |Ay|, |Bx|, |By|, |Rx|, |Ry|) * 1.35 -> Escala del marco gráfico

    fig.add_shape(type="line", x0=-limite, x1=limite, y0=0, y1=0,
                  line=dict(color="rgba(143,163,192,0.35)", width=1))
    fig.add_shape(type="line", x0=0, x1=0, y0=-limite, y1=limite,
                  line=dict(color="rgba(143,163,192,0.35)", width=1))

    _crear_flecha_vector(fig, (0, 0), (ax, ay), COLOR_A, "Vector A")
    _crear_flecha_vector(fig, (0, 0), (bx, by), COLOR_B, "Vector B")
    _crear_flecha_vector(fig, (0, 0), (res_x, res_y), COLOR_R, nombre_res, ancho=5)

    fig.update_layout(
        paper_bgcolor="#0B0F19",
        plot_bgcolor="#0B0F19",
        font=dict(color="#E6F1FF", family="Rajdhani"),
        showlegend=True,
        legend=dict(bgcolor="rgba(255,255,255,0.03)", bordercolor="rgba(0,240,255,0.25)", borderwidth=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=520,
        xaxis=dict(
            range=[-limite, limite], zeroline=False, showgrid=True,
            gridcolor="rgba(143,163,192,0.12)", title="x",
            scaleanchor="y", scaleratio=1,
        ),
        yaxis=dict(
            range=[-limite, limite], zeroline=False, showgrid=True,
            gridcolor="rgba(143,163,192,0.12)", title="y",
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------
    # 5. RESULTADOS — VECTORES INDIVIDUALES A y B INTERFAZ
    # ------------------------------------------------------------
    _md_html(
        """
        <div class="glass-header" style="font-size:1.05rem; margin-top:0.5rem;">
            📊 Magnitud e inclinación individual
        </div>
        """
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _tarjeta_resultado("Magnitud |A|", f"{mag_a:.2f}", color=COLOR_A)            # MOSTRAR CÁLCULO: Muestra mag_a en pantalla
    with c2:
        _tarjeta_resultado("Ángulo θ_A", f"{ang_a:.2f}°", color=COLOR_A)             # MOSTRAR CÁLCULO: Muestra ang_a en pantalla
    with c3:
        _tarjeta_resultado("Magnitud |B|", f"{mag_b:.2f}", color=COLOR_B)            # MOSTRAR CÁLCULO: Muestra mag_b en pantalla
    with c4:
        _tarjeta_resultado("Ángulo θ_B", f"{ang_b:.2f}°", color=COLOR_B)             # MOSTRAR CÁLCULO: Muestra ang_b en pantalla

    # ------------------------------------------------------------
    # 6. RESULTADOS — SUMA Y RESTA INTERFAZ
    # ------------------------------------------------------------
    _md_html(
        """
        <div class="glass-header" style="font-size:1.05rem; margin-top:1.2rem;">
            ➕➖ Vector Suma y Vector Resta
        </div>
        """
    )

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        _tarjeta_resultado("Suma → Rx, Ry", f"{sum_x:.2f}, {sum_y:.2f}", color=COLOR_R)                 # MOSTRAR CÁLCULO: Muestra (sum_x, sum_y)
    with s2:
        _tarjeta_resultado("Suma → |R|, θ", f"{mag_sum:.2f}  |  {ang_sum:.2f}°", color=COLOR_R)         # MOSTRAR CÁLCULO: Muestra (|R_suma|, θ_suma)
    with s3:
        _tarjeta_resultado("Resta → Rx, Ry", f"{dif_x:.2f}, {dif_y:.2f}", color=COLOR_R)                # MOSTRAR CÁLCULO: Muestra (dif_x, dif_y)
    with s4:
        _tarjeta_resultado("Resta → |R|, θ", f"{mag_dif:.2f}  |  {ang_dif:.2f}°", color=COLOR_R)         # MOSTRAR CÁLCULO: Muestra (|R_resta|, θ_resta)

    # ------------------------------------------------------------
    # 7. RESULTADOS — PRODUCTO ESCALAR Y PRODUCTO CRUZ INTERFAZ
    # ------------------------------------------------------------
    _md_html(
        """
        <div class="glass-header" style="font-size:1.05rem; margin-top:1.2rem;">
            ✳️ Producto Escalar y Producto Cruz (componente Z)
        </div>
        """
    )

    p1, p2 = st.columns(2)
    with p1:
        _tarjeta_resultado("A · B (escalar)", f"{producto_escalar:.2f}", color="#7B61FF")   # MOSTRAR CÁLCULO: Muestra producto_escalar
    with p2:
        _tarjeta_resultado("A × B (componente Z)", f"{producto_cruz_z:.2f}", color="#7B61FF") # MOSTRAR CÁLCULO: Muestra producto_cruz_z

    # ------------------------------------------------------------
    # 8. DESGLOSE DIDÁCTICO
    # ------------------------------------------------------------
    with st.expander("🧮 Ver explicación paso a paso de todos los resultados"):
        cuadrante_txt = _explicacion_cuadrante(res_x, res_y)
        _md_html(
            f"""
            <div class="glass-card" style="margin-top:0.4rem;">
                <div class="glass-subtext">
                    <b>1. RESULTANTE DE LA OPERACIÓN SELECCIONADA ({nombre_res}):</b><br>
                    • <b>Componente en X (Rx):</b> Se operan las X → {res_x:.2f}<br>
                    • <b>Componente en Y (Ry):</b> Se operan las Y → {res_y:.2f}<br>
                    • <b>Magnitud |R|:</b> Aplicando Pitágoras √(Rx² + Ry²) = √({res_x:.2f}² + {res_y:.2f}²) = <b style="color:{COLOR_R};">{res_mag:.2f}</b><br>
                    • <b>Ángulo θ:</b> Aplicando arcotangente arctan(Ry / Rx) = arctan({res_y:.2f} / {res_x:.2f}) = <b style="color:{COLOR_R};">{res_ang:.2f}°</b><br>
                    • <b>Ubicación:</b> {cuadrante_txt}<br><br>
                    <b>2. PRODUCTO ESCALAR / PUNTO (A · B):</b><br>
                    Mide la proyección entre ambos vectores. Se multiplican componentes X y se suman con el producto de las Y:<br>
                    • (Ax · Bx) + (Ay · By) = ({ax:.2f} · {bx:.2f}) + ({ay:.2f} · {by:.2f}) = <b style="color:#7B61FF;">{producto_escalar:.2f}</b><br><br>
                    <b>3. PRODUCTO CRUZ EN 2D (A × B):</b><br>
                    Calcula el área del paralelogramo o vector resultante en el eje Z:<br>
                    • (Ax · By) − (Ay · Bx) = ({ax:.2f} · {by:.2f}) − ({ay:.2f} · {bx:.2f}) = <b style="color:#7B61FF;">{producto_cruz_z:.2f}</b>
                </div>
            </div>
            """
        )