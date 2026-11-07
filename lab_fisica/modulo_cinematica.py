import math
import streamlit as st
import plotly.graph_objects as go

# Dependencias globales del proyecto
from utils import _md_html, glass_card

# PALETA DE COLORES ESPECÍFICA DEL MÓDULO
# ==========================================
COLOR_TRAYECTORIA = "#00F0FF"
COLOR_PUNTO_MAX = "#FF2EC4"
COLOR_IMPACTO = "#00FF66"
COLOR_TEXTO_SEC = "#8FA3C0"


# COMPONENTES DE UI Y ESTADO
# ==========================================
def _tarjeta_resultado(etiqueta, valor, unidad, color):
    """
    Renderiza un output numérico individual formateado.
    Evita redundancia de HTML en el layout principal.
    """
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
    """
    Control de input dual (Slider + NumberBox).
    Mantiene sincronización de estado utilizando session_state callbacks.
    """
    if key not in st.session_state:
        st.session_state[key] = default

    def _sync(origen):
        # Handler bidireccional para actualizar el componente inactivo
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

# NÚCLEO DE FÍSICA COMPUTACIONAL
# ==========================================
def _calcular(v0, theta_deg, y0, g):
    """
    Motor de cinemática. 
    Resuelve componentes, tiempo de vuelo (considerando Y0), altura y alcance.
    Devuelve un diccionario plano con resultados.
    """
    theta_rad = math.radians(theta_deg)
    
    # 1. Componentes iniciales
    v0x = v0 * math.cos(theta_rad)
    v0y = v0 * math.sin(theta_rad)
    
    # 2. Resolución de ecuación cuadrática para TVuelo
    disc = v0y ** 2 + 2 * g * y0
    t_vuelo = (v0y + math.sqrt(disc)) / g if g > 0 else 0.0
    
    # 3. Y Máximo y X Máximo
    y_max = y0 + (v0y ** 2) / (2 * g) if g > 0 else y0
    x_max = v0x * t_vuelo
    
    return {"v0x": v0x, "v0y": v0y, "t_vuelo": t_vuelo, "y_max": y_max, "x_max": x_max}

def _puntos_trayectoria(v0x, v0y, y0, g, t_vuelo, n=200):
    """Generador de la matriz de puntos (x, y) para renderizado de Plotly."""
    if t_vuelo <= 0:
        return [0.0], [max(y0, 0.0)]
        
    dt = t_vuelo / (n - 1) # Delta de tiempo iterativo
    xs, ys = [], []
    
    for i in range(n):
        t = i * dt
        xs.append(v0x * t)
        ys.append(max(y0 + v0y * t - 0.5 * g * t * t, 0.0))
        
    return xs, ys

# RENDERIZADO DE GRÁFICOS INTERACTIVOS
# ==========================================
def _grafica_trayectoria(datos, historial):
    """Construye y devuelve un objeto de figura Plotly con la simulación montada y su historial."""
    v0x, v0y, y0, g = datos["v0x"], datos["v0y"], datos["y0"], datos["g"]
    t_vuelo, y_max, x_max = datos["t_vuelo"], datos["y_max"], datos["x_max"]
    theta_deg = datos["theta_deg"]
    
    # Escalamiento dinámico: buscar los máximos entre la trayectoria actual y todo el historial
    max_x_plot = max([x_max] + [h["x_max"] for h in historial])
    max_y_plot = max([y_max] + [h["y_max"] for h in historial])
    max_y0_plot = max([y0] + [h["y0"] for h in historial])

    x_pad = max(max_x_plot, 1.0) * 1.15
    y_lim = max(max_y_plot * 1.25, max_y0_plot * 1.1, 5)

    fig = go.Figure()
    
    # Eje base estructural
    fig.add_shape(type="line", x0=0, x1=x_pad, y0=0, y1=0, line=dict(color=f"{COLOR_TEXTO_SEC}90", width=2))

    # --- DIBUJAR HISTORIAL (Fantasmas) ---
    for i, h_dat in enumerate(historial):
        h_xs, h_ys = _puntos_trayectoria(h_dat["v0x"], h_dat["v0y"], h_dat["y0"], h_dat["g"], h_dat["t_vuelo"])
        opacidad = 0.25 + (i * 0.15) # Ajuste visual para distinguir la antigüedad
        
        fig.add_trace(go.Scatter(
            x=h_xs, y=h_ys, mode="lines",
            line=dict(color=f"rgba(255, 255, 255, {opacidad})", width=2, dash="dash"),
            name=f"Intento {i+1} (V₀={h_dat['v0']}, θ={h_dat['theta_deg']}°)",
            hovertemplate="x=%{x:.1f} m<br>y=%{y:.1f} m<extra>Historial</extra>",
        ))
        # Punto de impacto sutil para el historial
        fig.add_trace(go.Scatter(
            x=[h_dat["x_max"]], y=[0], mode="markers",
            marker=dict(size=8, color=f"rgba(255, 255, 255, {opacidad})", symbol="diamond"),
            showlegend=False, hoverinfo="skip"
        ))

    # --- DIBUJAR TRAYECTORIA ACTUAL ---
    xs, ys = _puntos_trayectoria(v0x, v0y, y0, g, t_vuelo)
    
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines",
        line=dict(color=COLOR_TRAYECTORIA, width=3, dash="dot"),
        name="Trayectoria actual", hovertemplate="x=%{x:.1f} m<br>y=%{y:.1f} m<extra></extra>",
    ))

    # Vector inicial V0
    largo = 0.18 * x_pad
    px = largo * math.cos(math.radians(theta_deg))
    py = y0 + largo * math.sin(math.radians(theta_deg))
    
    fig.add_annotation(x=px, y=py, ax=0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=3, arrowsize=1.4, arrowwidth=3, arrowcolor=COLOR_TRAYECTORIA)

    # Marcador de Ymax (Cúspide)
    t_apice = v0y / g if g > 0 else 0.0
    x_apice = v0x * t_apice
    fig.add_trace(go.Scatter(x=[x_apice], y=[y_max], mode="markers",
                              marker=dict(size=24, color=COLOR_PUNTO_MAX, opacity=0.25),
                              showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[x_apice], y=[y_max], mode="markers",
                              marker=dict(size=11, color=COLOR_PUNTO_MAX, symbol="diamond", line=dict(color="white", width=1)),
                              name="Y máx", hovertemplate=f"Y máx = {y_max:.2f} m<extra></extra>"))

    # Marcador de Xmax (Impacto)
    fig.add_trace(go.Scatter(x=[x_max], y=[0], mode="markers",
                              marker=dict(size=24, color=COLOR_IMPACTO, opacity=0.25),
                              showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[x_max], y=[0], mode="markers",
                              marker=dict(size=11, color=COLOR_IMPACTO, symbol="diamond", line=dict(color="white", width=1)),
                              name="X máx", hovertemplate=f"X máx = {x_max:.2f} m<extra></extra>"))

    # Ajustes de Layout e interfaz visual
    fig.update_layout(
        paper_bgcolor="#0B0F19", plot_bgcolor="#0B0F19",
        font=dict(family="Rajdhani, sans-serif", color=COLOR_TEXTO_SEC, size=13),
        margin=dict(l=10, r=10, t=10, b=10), height=460, showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12, x=0),
        xaxis=dict(title="distancia horizontal (m)", range=[0, x_pad], gridcolor=f"{COLOR_TEXTO_SEC}25", zerolinecolor=f"{COLOR_TEXTO_SEC}55"),
        yaxis=dict(title="altura (m)", range=[0, y_lim], gridcolor=f"{COLOR_TEXTO_SEC}25", zerolinecolor=f"{COLOR_TEXTO_SEC}55"),
    )
    return fig


# METADATA DIDÁCTICA
# ==========================================
def _explicacion_formulas():
    with st.expander("📚 Ver el paso a paso de las ecuaciones"):
        _md_html(f"""
        <div style="font-family:'Rajdhani',sans-serif; color:#E6F1FF; line-height:1.8; font-size:0.95rem;">
        <p><b style="color:{COLOR_TRAYECTORIA};">1. Componentes de V₀</b><br>
        V₀x = V₀·cos(θ) &nbsp; V₀y = V₀·sin(θ)</p>
        <p><b style="color:{COLOR_TRAYECTORIA};">2. Tiempo de vuelo</b><br>
        t<sub>vuelo</sub> = (V₀y + √(V₀y² + 2·g·Y₀)) / g</p>
        <p><b style="color:{COLOR_PUNTO_MAX};">3. Altura máxima</b><br>
        Y<sub>max</sub> = Y₀ + V₀y² / (2·g)</p>
        <p><b style="color:{COLOR_IMPACTO};">4. Alcance horizontal</b><br>
        X<sub>max</sub> = V₀x · t<sub>vuelo</sub></p>
        </div>
        """)

# CONTROLADOR PRINCIPAL DEL MÓDULO
# ==========================================
def modulo_cinematica():
    """Ejecuta el ciclo de vida de la vista del módulo 2."""
    
    # Iniciar variable de estado para el historial si no existe
    if "historial_cinematica" not in st.session_state:
        st.session_state.historial_cinematica = []

    glass_card(
        header="🚀 Módulo 2 — Cinemática: Tiro Parabólico",
        subtext="Simulación pura de movimiento proyectil.",
    )

    # Pipeline de Entrada
    with st.container(border=True):
        v0 = _synced_pair("Velocidad inicial V₀ (m/s)", "v0", 0.0, 100.0, 25.0, step=0.5)
        theta_deg = _synced_pair("Ángulo de lanzamiento θ (°)", "theta", 0.0, 90.0, 45.0, step=0.5)
        y0 = _synced_pair("Altura inicial Y₀ (m)", "y0", 0.0, 50.0, 0.0, step=0.5)
        g = _synced_pair("Gravedad g (m/s²)", "g", 1.0, 20.0, 9.81, step=0.01, fmt="%.2f")

    # Pipeline de Procesamiento
    resultados = _calcular(v0, theta_deg, y0, g)
    datos = {"v0": v0, "theta_deg": theta_deg, "y0": y0, "g": g, **resultados}

    # Pipeline de Salida UI (Resultados Numéricos)
    cols = st.columns(5)
    valores = [
        ("Tiempo de vuelo", f"{datos['t_vuelo']:.2f}", "s", COLOR_TEXTO_SEC),
        ("Alcance X máx", f"{datos['x_max']:.2f}", "m", COLOR_IMPACTO),
        ("Altura Y máx", f"{datos['y_max']:.2f}", "m", COLOR_PUNTO_MAX),
        ("Velocidad V₀x", f"{datos['v0x']:.2f}", "m/s", COLOR_TRAYECTORIA),
        ("Velocidad V₀y", f"{datos['v0y']:.2f}", "m/s", COLOR_TRAYECTORIA),
    ]
    for col, (etiqueta, valor, unidad, color) in zip(cols, valores):
        with col:
            _tarjeta_resultado(etiqueta, valor, unidad, color)

    # Controles para el Historial (Guardar / Limpiar)
    st.write("") 
    col_btn1, col_btn2, _ = st.columns([2, 2, 5])
    
    with col_btn1:
        if st.button("💾 Guardar gráfica (Máx 3)", use_container_width=True):
            # Prevenir que el usuario guarde el mismo lanzamiento repetido varias veces
            if not st.session_state.historial_cinematica or st.session_state.historial_cinematica[-1] != datos:
                st.session_state.historial_cinematica.append(datos)
                # Mantener el límite estricto de 3 historiales (First-In, First-Out)
                if len(st.session_state.historial_cinematica) > 3:
                    st.session_state.historial_cinematica.pop(0)
                    
    with col_btn2:
        if st.button("🗑️ Limpiar historial", use_container_width=True):
            st.session_state.historial_cinematica.clear()

    # Pipeline de Salida Gráfica
    with st.container(border=True):
        st.plotly_chart(_grafica_trayectoria(datos, st.session_state.historial_cinematica), use_container_width=True)

    _explicacion_formulas()
    return datos

if __name__ == "__main__":
    st.set_page_config(page_title="Cinemática", layout="wide")
    modulo_cinematica()