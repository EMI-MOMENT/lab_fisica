import math
import streamlit as st
import plotly.graph_objects as go

from utils import _md_html, glass_card

COLOR_RAMPA = "#8FA3C0"
COLOR_BLOQUE = "#00F0FF"
COLOR_PESO = "#FF2EC4"
COLOR_NORMAL = "#00FF66"
COLOR_FRICCION = "#FFA500"
COLOR_TEXTO_SEC = "#8FA3C0"

def _tarjeta_resultado(etiqueta, valor, unidad, color):
    _md_html(f"""
    <div class="glass-card" style="padding:1rem 1.2rem; text-align:center; margin-bottom:0; background:rgba(255,255,255,0.05); border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
        <div class="glass-subtext" style="font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; color:{COLOR_TEXTO_SEC};">
            {etiqueta}
        </div>
        <div style="font-family:'Orbitron',sans-serif; font-size:1.3rem; color:{color}; text-shadow:0 0 12px {color}66; margin-top:0.3rem;">
            {valor}<span style="font-size:0.7rem; color:{COLOR_TEXTO_SEC}; margin-left:3px;">{unidad}</span>
        </div>
    </div>
    """)

def _synced_pair(label, key, min_val, max_val, default, step=1.0, fmt="%.2f"):
    if key not in st.session_state:
        st.session_state[key] = default

    def _sync(origen):
        nuevo = st.session_state[f"{key}_{origen}"]
        st.session_state[key] = nuevo
        otro = "num" if origen == "sld" else "sld"
        st.session_state[f"{key}_{otro}"] = nuevo

    _md_html(
        f"<p style='color:{COLOR_TEXTO_SEC}; font-family:Rajdhani,sans-serif; "
        f"font-weight:600; font-size:0.85rem; margin-bottom:-0.6rem;'>{label}</p>"
    )
    c1, c2 = st.columns([3, 1])
    with c1:
        st.slider(label, min_val, max_val, value=st.session_state[key], step=step,
                  key=f"{key}_sld", on_change=_sync, args=("sld",), label_visibility="collapsed")
    with c2:
        st.number_input(label, min_val, max_val, value=st.session_state[key], step=step,
                         key=f"{key}_num", on_change=_sync, args=("num",), format=fmt,
                         label_visibility="collapsed")
    return st.session_state[key]

def _calcular(m, theta_deg, mu, g):
    theta_rad = math.radians(theta_deg)
    w = m * g
    wx = w * math.sin(theta_rad)
    wy = w * math.cos(theta_rad)
    n = wy
    
    fr_max = mu * n
    
    if wx > fr_max:
        fr = fr_max
        f_neta = wx - fr
        a = f_neta / m
    else:
        fr = wx
        f_neta = 0.0
        a = 0.0
        
    return {"w": w, "wx": wx, "wy": wy, "n": n, "fr": fr, "f_neta": f_neta, "a": a}

def _grafica_plano(datos):
    theta_deg = datos["theta_deg"]
    theta_rad = math.radians(theta_deg)
    
    base_longitud = 10
    altura_triangulo = base_longitud * math.tan(theta_rad)
    
    x_triangulo = [0, base_longitud, base_longitud, 0]
    y_triangulo = [0, 0, altura_triangulo, 0]
    
    pos_x_bloque = base_longitud / 2
    pos_y_bloque = pos_x_bloque * math.tan(theta_rad)
    
    tamano_bloque = 1.5
    
    dx_paralelo = tamano_bloque * math.cos(theta_rad)
    dy_paralelo = tamano_bloque * math.sin(theta_rad)
    dx_perpendicular = tamano_bloque * math.sin(theta_rad)
    dy_perpendicular = tamano_bloque * math.cos(theta_rad)
    
    x_bloque = [
        pos_x_bloque,
        pos_x_bloque - dx_paralelo,
        pos_x_bloque - dx_paralelo - dx_perpendicular,
        pos_x_bloque - dx_perpendicular,
        pos_x_bloque
    ]
    y_bloque = [
        pos_y_bloque,
        pos_y_bloque - dy_paralelo,
        pos_y_bloque - dy_paralelo + dy_perpendicular,
        pos_y_bloque + dy_perpendicular,
        pos_y_bloque
    ]
    
    cx = pos_x_bloque - dx_paralelo / 2 - dx_perpendicular / 2
    cy = pos_y_bloque - dy_paralelo / 2 + dy_perpendicular / 2
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_triangulo, y=y_triangulo, fill="toself",
        fillcolor=f"{COLOR_RAMPA}33", line=dict(color=COLOR_RAMPA, width=2),
        name="Plano Inclinado", hoverinfo="skip"
    ))
    
    fig.add_trace(go.Scatter(
        x=x_bloque, y=y_bloque, fill="toself",
        fillcolor=f"{COLOR_BLOQUE}66", line=dict(color=COLOR_BLOQUE, width=2),
        name="Bloque", hoverinfo="skip"
    ))
    
    escala_fuerza = 0.05
    w = datos["w"]
    n = datos["n"]
    fr = datos["fr"]
    wx = datos["wx"]
    
    fig.add_annotation(
        x=cx, y=cy - w * escala_fuerza, ax=cx, ay=cy,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=3, arrowcolor=COLOR_PESO,
        text="W", font=dict(color=COLOR_PESO)
    )
    
    n_dx = n * escala_fuerza * math.sin(theta_rad)
    n_dy = n * escala_fuerza * math.cos(theta_rad)
    fig.add_annotation(
        x=cx - n_dx, y=cy + n_dy, ax=cx, ay=cy,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=3, arrowcolor=COLOR_NORMAL,
        text="N", font=dict(color=COLOR_NORMAL)
    )
    
    if fr > 0:
        fr_dx = fr * escala_fuerza * math.cos(theta_rad)
        fr_dy = fr * escala_fuerza * math.sin(theta_rad)
        fig.add_annotation(
            x=cx + fr_dx, y=cy + fr_dy, ax=cx, ay=cy,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=3, arrowcolor=COLOR_FRICCION,
            text="Fr", font=dict(color=COLOR_FRICCION)
        )
        
    fig.update_layout(
        paper_bgcolor="#0B0F19", plot_bgcolor="#0B0F19",
        font=dict(family="Rajdhani, sans-serif", color=COLOR_TEXTO_SEC, size=13),
        margin=dict(l=10, r=10, t=10, b=10), height=400, showlegend=False,
        xaxis=dict(visible=False, range=[-2, base_longitud + 2]),
        yaxis=dict(visible=False, range=[-2, max(altura_triangulo + 2, 8)], scaleanchor="x", scaleratio=1),
    )
    return fig

def _explicacion_formulas():
    with st.expander("📚 Ver el paso a paso de las ecuaciones (Leyes de Newton)"):
        _md_html(f"""
        <div style="font-family:'Rajdhani',sans-serif; color:#E6F1FF; line-height:1.8; font-size:0.95rem;">
        <p><b style="color:{COLOR_PESO};">1. Peso (W) y Componentes</b><br>
        W = m · g <br>
        W<sub>x</sub> = W · sen(θ) (Componente paralela al plano)<br>
        W<sub>y</sub> = W · cos(θ) (Componente perpendicular al plano)</p>
        <p><b style="color:{COLOR_NORMAL};">2. Fuerza Normal (N)</b><br>
        ΣF<sub>y</sub> = N - W<sub>y</sub> = 0 ⇒ N = W<sub>y</sub></p>
        <p><b style="color:{COLOR_FRICCION};">3. Fuerza de Fricción (Fr)</b><br>
        Fr<sub>máx</sub> = μ · N <br>
        Si W<sub>x</sub> ≤ Fr<sub>máx</sub>, entonces Fr = W<sub>x</sub> (el bloque no desliza).<br>
        Si W<sub>x</sub> > Fr<sub>máx</sub>, entonces Fr = Fr<sub>máx</sub> (el bloque desliza).</p>
        <p><b style="color:{COLOR_BLOQUE};">4. Fuerza Neta y Aceleración</b><br>
        ΣF<sub>x</sub> = W<sub>x</sub> - Fr = F<sub>neta</sub><br>
        F<sub>neta</sub> = m · a ⇒ a = F<sub>neta</sub> / m</p>
        </div>
        """)

def modulo_dinamica_plano_inclinado():
    glass_card(
        header="⚙️ Módulo 3 — Dinámica: Plano Inclinado",
        subtext="Simulación de fuerzas, fricción y aceleración de un bloque.",
    )

    with st.container(border=True):
        m = _synced_pair("Masa m (kg)", "masa", 1.0, 50.0, 10.0, step=0.5)
        theta_deg = _synced_pair("Ángulo de inclinación θ (°)", "theta_plano", 0.0, 89.0, 30.0, step=1.0)
        mu = _synced_pair("Coeficiente de rozamiento μ", "mu", 0.0, 1.0, 0.2, step=0.01, fmt="%.2f")
        g = _synced_pair("Gravedad g (m/s²)", "g_plano", 1.0, 20.0, 9.81, step=0.01, fmt="%.2f")

    resultados = _calcular(m, theta_deg, mu, g)
    datos = {"m": m, "theta_deg": theta_deg, "mu": mu, "g": g, **resultados}

    cols = st.columns(4)
    valores = [
        ("Aceleración", f"{datos['a']:.2f}", "m/s²", COLOR_BLOQUE),
        ("Fuerza Normal", f"{datos['n']:.2f}", "N", COLOR_NORMAL),
        ("Fricción", f"{datos['fr']:.2f}", "N", COLOR_FRICCION),
        ("Fuerza Neta", f"{datos['f_neta']:.2f}", "N", COLOR_PESO),
    ]
    for col, (etiqueta, valor, unidad, color) in zip(cols, valores):
        with col:
            _tarjeta_resultado(etiqueta, valor, unidad, color)

    with st.container(border=True):
        st.plotly_chart(_grafica_plano(datos), use_container_width=True)

    _explicacion_formulas()
    return datos

if __name__ == "__main__":
    st.set_page_config(page_title="Dinámica", layout="wide")
    modulo_dinamica_plano_inclinado()