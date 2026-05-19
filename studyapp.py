import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

st.set_page_config(page_title="StudyLab", page_icon="📚", layout="wide")

# ── CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0.3rem; }
    .sub-title { text-align: center; color: #888; margin-bottom: 2rem; }
    .formula-box { background: #1e1e2e; border-radius: 10px; padding: 1.2rem; margin: 1rem 0; text-align: center; font-size: 1.1rem; border-left: 4px solid #6366f1; }
    .result-box { background: #1a1a2e; border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0; border-left: 4px solid #10b981; }
    h2 { border-bottom: 1px solid #333; padding-bottom: 0.3rem; }
    .stApp { background: #0f0f1a; }
    .block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📚 StudyLab</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive learning tools for Math · Physics · Chemistry</div>', unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────
subject = st.sidebar.radio("Subject", ["📐 Math", "⚡ Physics", "🧪 Chemistry"], index=0)
st.sidebar.markdown("---")
st.sidebar.caption("Adjust sliders & inputs below to explore interactively.")

# ================================================================
#                         📐 MATH SECTION
# ================================================================
if subject == "📐 Math":
    topic = st.selectbox("Topic", [
        "Quadratic Equation", "Trigonometry Explorer", 
        "Derivative Visualizer", "Integral Area",
        "Unit Circle",
        "3D Geometry"
    ])

    # ── Quadratic ─────────────────────────────────────────────
    if topic == "Quadratic Equation":
        st.markdown("## ax² + bx + c = 0")
        st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")

        col1, col2, col3 = st.columns(3)
        with col1: a = st.slider("a", -10.0, 10.0, 1.0, 0.1)
        with col2: b = st.slider("b", -10.0, 10.0, 0.0, 0.1)
        with col3: c = st.slider("c", -10.0, 10.0, -4.0, 0.1)

        D = b**2 - 4*a*c
        st.markdown(f'<div class="result-box">Δ = {D:.2f}</div>', unsafe_allow_html=True)

        if D >= 0:
            x1 = (-b + math.sqrt(D)) / (2*a)
            x2 = (-b - math.sqrt(D)) / (2*a)
            st.success(f"**Roots:** x₁ = {x1:.4f},   x₂ = {x2:.4f}")
        else:
            real = -b / (2*a)
            imag = math.sqrt(-D) / (2*a)
            st.warning(f"**Complex roots:** {real:.4f} ± {imag:.4f}i")
            x1 = x2 = None

        x_vals = np.linspace(-10, 10, 500)
        y_vals = a*x_vals**2 + b*x_vals + c
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Parabola",
                                  line=dict(color="#6366f1", width=2)))
        if D >= 0 and x1 is not None:
            fig.add_trace(go.Scatter(x=[x1, x2], y=[0, 0], mode="markers",
                                      marker=dict(size=10, color="#ef4444", symbol="x"),
                                      name="Roots"))
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
        fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dash"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                          xaxis_title="x", yaxis_title="y", hovermode="x")
        st.plotly_chart(fig, use_container_width=True)

    # ── Trigonometry ──────────────────────────────────────────
    elif topic == "Trigonometry Explorer":
        st.markdown("## Interactive Trig Functions")
        func = st.selectbox("Function", ["sin(x)", "cos(x)", "tan(x)", "sin(x) & cos(x)"])
        amp = st.slider("Amplitude", 0.1, 5.0, 1.0, 0.1)
        freq = st.slider("Frequency", 0.1, 5.0, 1.0, 0.1)
        phase = st.slider("Phase shift", 0.0, 6.28, 0.0, 0.01)

        x = np.linspace(-2*np.pi, 2*np.pi, 600)
        fig = go.Figure()

        def add_fn(fn_name, y_fn, color, dash="solid"):
            y = amp * y_fn(freq * x + phase)
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=f"{amp}{fn_name}({freq}x+{phase:.2f})",
                                      line=dict(color=color, width=2, dash=dash)))

        if func == "sin(x)":
            add_fn("sin", np.sin, "#6366f1")
        elif func == "cos(x)":
            add_fn("cos", np.cos, "#10b981")
        elif func == "tan(x)":
            y = amp * np.tan(freq * x + phase)
            y = np.where(np.abs(y) > 10, np.nan, y)
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="tan(x)",
                                      line=dict(color="#f59e0b", width=2)))
        else:
            add_fn("sin", np.sin, "#6366f1")
            add_fn("cos", np.cos, "#10b981")

        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                          yaxis_range=[-5, 5], hovermode="x")
        st.plotly_chart(fig, use_container_width=True)

    # ── Derivative ────────────────────────────────────────────
    elif topic == "Derivative Visualizer":
        st.markdown("## Function & Its Derivative")
        fn_choice = st.selectbox("Function", ["x²", "x³", "sin(x)", "cos(x)", "e^x", "ln(x)"])
        x = np.linspace(-5, 5, 500)

        if fn_choice == "x²":
            f = x**2; df = 2*x; label = "x²"; dlabel = "2x"
        elif fn_choice == "x³":
            f = x**3; df = 3*x**2; label = "x³"; dlabel = "3x²"
        elif fn_choice == "sin(x)":
            f = np.sin(x); df = np.cos(x); label = "sin(x)"; dlabel = "cos(x)"
        elif fn_choice == "cos(x)":
            f = np.cos(x); df = -np.sin(x); label = "cos(x)"; dlabel = "-sin(x)"
        elif fn_choice == "e^x":
            f = np.exp(x); df = np.exp(x); label = "eˣ"; dlabel = "eˣ"
        elif fn_choice == "ln(x)":
            mask = x > 0
            x = x[mask]; f = np.log(x[mask]); df = 1/x[mask]; label = "ln(x)"; dlabel = "1/x"

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name=label, line=dict(color="#6366f1", width=2)))
        fig.add_trace(go.Scatter(x=x, y=df, mode="lines", name=f"d/dx {dlabel}",
                                  line=dict(color="#ef4444", width=2, dash="dash")))
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), hovermode="x")
        st.plotly_chart(fig, use_container_width=True)

        st.latex(r"\frac{d}{dx}f(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}")

    # ── Integral ─────────────────────────────────────────────
    elif topic == "Integral Area":
        st.markdown("## Definite Integral — Area Under Curve")
        fn_choice = st.selectbox("Function", ["x²", "x³", "sin(x)", "cos(x)"], key="int_fn")
        a_i, b_i = st.slider("Integration range [a, b]", -5.0, 5.0, (0.0, 2.0), 0.1)

        x = np.linspace(-5, 5, 600)
        if fn_choice == "x²": f = x**2; label = "x²"
        elif fn_choice == "x³": f = x**3; label = "x³"
        elif fn_choice == "sin(x)": f = np.sin(x); label = "sin(x)"
        elif fn_choice == "cos(x)": f = np.cos(x); label = "cos(x)"

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=f, mode="lines", name=label, line=dict(color="#6366f1", width=2)))
        mask = (x >= a_i) & (x <= b_i)
        fig.add_trace(go.Scatter(x=x[mask], y=f[mask], mode="lines", fill="tozeroy",
                                  name=f"Area [{a_i}, {b_i}]",
                                  line=dict(color="rgba(99,102,241,0.3)", width=0),
                                  fillcolor="rgba(99,102,241,0.2)"))
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), hovermode="x")
        st.plotly_chart(fig, use_container_width=True)

        # Numerical approximation
        dx = 0.001
        xs = np.arange(a_i, b_i, dx)
        if fn_choice == "x²": approx = np.sum(xs**2) * dx
        elif fn_choice == "x³": approx = np.sum(xs**3) * dx
        elif fn_choice == "sin(x)": approx = np.sum(np.sin(xs)) * dx
        elif fn_choice == "cos(x)": approx = np.sum(np.cos(xs)) * dx

        st.info(f"∫_{a_i}^{b_i} {label} dx ≈ {approx:.6f}")

    # ── Unit Circle ──────────────────────────────────────────
    elif topic == "Unit Circle":
        st.markdown("## Unit Circle Explorer")
        angle = st.slider("Angle θ (degrees)", 0, 360, 45, 1)
        rad = math.radians(angle)
        cx, cy = math.cos(rad), math.sin(rad)

        theta = np.linspace(0, 2*np.pi, 400)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines",
                                  name="Unit circle", line=dict(color="#6366f1", width=2)))
        fig.add_trace(go.Scatter(x=[0, cx], y=[0, cy], mode="lines",
                                  name=f"θ = {angle}°",
                                  line=dict(color="#f59e0b", width=2)))
        fig.add_trace(go.Scatter(x=[cx], y=[cy], mode="markers",
                                  marker=dict(size=10, color="#ef4444"), name="Point"))
        # dashed lines for cos/sin
        fig.add_trace(go.Scatter(x=[0, cx], y=[cy, cy], mode="lines",
                                  line=dict(color="#10b981", width=1, dash="dot"), name=f"sin = {cy:.4f}"))
        fig.add_trace(go.Scatter(x=[cx, cx], y=[0, cy], mode="lines",
                                  line=dict(color="#8b5cf6", width=1, dash="dot"), name=f"cos = {cx:.4f}"))

        fig.update_layout(height=500, xaxis_range=[-1.3, 1.3], yaxis_range=[-1.3, 1.3],
                          xaxis=dict(scaleanchor="y"), margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("sin θ", f"{cy:.4f}")
        with col2: st.metric("cos θ", f"{cx:.4f}")
        with col3: st.metric("tan θ", f"{cy/cx:.4f}" if abs(cx) > 0.001 else "∞")

    # ── 3D Geometry ────────────────────────────────────────────
    elif topic == "3D Geometry":
        st.markdown("## 3D Geometry Explorer")
        st.markdown("Click, drag, and scroll to rotate and zoom. Dimension labels shown in color.")

        shape = st.selectbox("Shape", [
            "Sphere", "Cube", "Pyramid", "Prism",
            "Cylinder", "Cone", "Torus", "Helix", "Sinusoidal Surface"
        ])

        dim_color_r = "#ef4444"   # red — radius
        dim_color_h = "#3b82f6"   # blue — height
        dim_color_s = "#22c55e"   # green — side / length
        dim_color_R = "#f97316"   # orange — major radius

        def label_3d(fig, x, y, z, text, color="white", size=14):
            fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode="text",
                                        text=[text], textfont=dict(color=color, size=size),
                                        hoverinfo="none", showlegend=False))

        def dim_line(fig, x1, y1, z1, x2, y2, z2, color, width=3):
            fig.add_trace(go.Scatter3d(x=[x1, x2], y=[y1, y2], z=[z1, z2],
                                        mode="lines", line=dict(color=color, width=width, dash="dash"),
                                        hoverinfo="none", showlegend=False))

        fig = go.Figure()

        # ── Sphere ──
        if shape == "Sphere":
            r = st.slider("Radius", 0.5, 5.0, 2.0, 0.1)
            phi, theta = np.mgrid[0:2*np.pi:40j, 0:np.pi:40j]
            x = r * np.sin(theta) * np.cos(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(theta)
            fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale="Viridis", opacity=0.85,
                                      showscale=False))
            # center dot + radius line
            dim_line(fig, 0, 0, 0, r, 0, 0, dim_color_r, 3)
            fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers",
                                        marker=dict(size=4, color="white"),
                                        hoverinfo="none", showlegend=False))
            label_3d(fig, r/2, 0, -0.4, "r", dim_color_r, 16)
            st.latex(r"V = \frac{4}{3}\pi r^3  \quad A = 4\pi r^2")
            c1, c2 = st.columns(2)
            with c1: st.metric("Surface Area", f"{4*math.pi*r**2:.2f}")
            with c2: st.metric("Volume", f"{(4/3)*math.pi*r**3:.2f}")

        # ── Cube ──
        elif shape == "Cube":
            s = st.slider("Side length", 0.5, 5.0, 2.0, 0.1)
            h2 = s / 2
            pts = [[x, y, z] for x in [-h2, h2] for y in [-h2, h2] for z in [-h2, h2]]
            edges = [[0,1],[1,3],[3,2],[2,0],[4,5],[5,7],[7,6],[6,4],[0,4],[1,5],[2,6],[3,7]]
            ex, ey, ez = [], [], []
            for a, b in edges:
                ex += [pts[a][0], pts[b][0], None]
                ey += [pts[a][1], pts[b][1], None]
                ez += [pts[a][2], pts[b][2], None]
            fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
                                        line=dict(color="#6366f1", width=4),
                                        hoverinfo="none", showlegend=False))
            # vertices
            fig.add_trace(go.Scatter3d(x=[p[0] for p in pts], y=[p[1] for p in pts],
                                        z=[p[2] for p in pts], mode="markers",
                                        marker=dict(size=5, color="#ef4444"),
                                        hoverinfo="none", showlegend=False))
            # side dimension along bottom edge (0→1)
            dim_line(fig, pts[0][0], pts[0][1]-0.8, pts[0][2],
                     pts[1][0], pts[1][1]-0.8, pts[1][2], dim_color_s, 2)
            label_3d(fig, 0, -h2-0.8, -h2, "s", dim_color_s, 16)
            st.latex(r"V = s^3  \quad A = 6s^2")
            c1, c2 = st.columns(2)
            with c1: st.metric("Surface Area", f"{6*s**2:.2f}")
            with c2: st.metric("Volume", f"{s**3:.2f}")

        # ── Pyramid ──
        elif shape == "Pyramid":
            bs = st.slider("Base side", 0.5, 5.0, 2.0, 0.1)
            ph = st.slider("Height", 0.5, 5.0, 2.0, 0.1)
            hb = bs / 2
            pts = [[-hb,-hb,0],[hb,-hb,0],[hb,hb,0],[-hb,hb,0],[0,0,ph]]
            edges = [[0,1],[1,2],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4]]
            ex, ey, ez = [], [], []
            for a, b in edges:
                ex += [pts[a][0], pts[b][0], None]
                ey += [pts[a][1], pts[b][1], None]
                ez += [pts[a][2], pts[b][2], None]
            fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
                                        line=dict(color="#f59e0b", width=4),
                                        hoverinfo="none", showlegend=False))
            fig.add_trace(go.Scatter3d(x=[p[0] for p in pts], y=[p[1] for p in pts],
                                        z=[p[2] for p in pts], mode="markers",
                                        marker=dict(size=5, color="#ef4444"),
                                        hoverinfo="none", showlegend=False))
            # height line: base center → apex
            dim_line(fig, 0, 0, 0, 0, 0, ph, dim_color_h, 2)
            label_3d(fig, 0.4, 0, ph/2, "h", dim_color_h, 16)
            # base side dimension
            dim_line(fig, pts[0][0], pts[0][1]-0.6, 0, pts[1][0], pts[1][1]-0.6, 0, dim_color_s, 2)
            label_3d(fig, 0, -hb-0.6, 0, "s", dim_color_s, 16)
            slant = math.sqrt(hb**2 + ph**2)
            a_base = bs**2
            a_side = 2 * bs * slant
            st.latex(r"V = \frac{1}{3}s^2 h  \quad A = s^2 + 2s\sqrt{(\frac{s}{2})^2 + h^2}")
            c1, c2 = st.columns(2)
            with c1: st.metric("Surface Area", f"{a_base + a_side:.2f}")
            with c2: st.metric("Volume", f"{(1/3)*bs**2*ph:.2f}")

        # ── Prism (triangular) ──
        elif shape == "Prism":
            bl = st.slider("Base triangle side", 0.5, 5.0, 2.0, 0.1)
            pr_h = st.slider("Prism height", 0.5, 5.0, 3.0, 0.1)
            ht = math.sqrt(3)/2 * bl
            pts = [
                [-bl/2, -ht/3, 0], [bl/2, -ht/3, 0], [0, 2*ht/3, 0],
                [-bl/2, -ht/3, pr_h], [bl/2, -ht/3, pr_h], [0, 2*ht/3, pr_h]
            ]
            edges = [[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]]
            ex, ey, ez = [], [], []
            for a, b in edges:
                ex += [pts[a][0], pts[b][0], None]
                ey += [pts[a][1], pts[b][1], None]
                ez += [pts[a][2], pts[b][2], None]
            fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
                                        line=dict(color="#10b981", width=4),
                                        hoverinfo="none", showlegend=False))
            fig.add_trace(go.Scatter3d(x=[p[0] for p in pts], y=[p[1] for p in pts],
                                        z=[p[2] for p in pts], mode="markers",
                                        marker=dict(size=5, color="#ef4444"),
                                        hoverinfo="none", showlegend=False))
            # side dimension
            dim_line(fig, -bl/2, -ht/3-0.6, 0, bl/2, -ht/3-0.6, 0, dim_color_s, 2)
            label_3d(fig, 0, -ht/3-0.6, 0, "s", dim_color_s, 16)
            # height dimension
            dim_line(fig, bl/2+0.6, -ht/3, 0, bl/2+0.6, -ht/3, pr_h, dim_color_h, 2)
            label_3d(fig, bl/2+0.6, -ht/3, pr_h/2, "h", dim_color_h, 16)
            a_base_tri = (math.sqrt(3)/4) * bl**2
            st.latex(r"V = \frac{\sqrt{3}}{4}s^2 h  \quad A = \frac{\sqrt{3}}{2}s^2 + 3sh")
            c1, c2 = st.columns(2)
            with c1: st.metric("Surface Area", f"{2*a_base_tri + 3*bl*pr_h:.2f}")
            with c2: st.metric("Volume", f"{a_base_tri*pr_h:.2f}")

        # ── Cylinder ──
        elif shape == "Cylinder":
            r = st.slider("Radius", 0.5, 5.0, 2.0, 0.1)
            h = st.slider("Height", 1.0, 8.0, 4.0, 0.1)
            zc = np.linspace(-h/2, h/2, 30)
            tc = np.linspace(0, 2*np.pi, 40)
            tc, zc = np.meshgrid(tc, zc)
            fig.add_trace(go.Surface(x=r*np.cos(tc), y=r*np.sin(tc), z=zc,
                                      colorscale="Turbo", opacity=0.85, showscale=False))
            # radius line at base
            dim_line(fig, 0, 0, -h/2, r, 0, -h/2, dim_color_r, 2)
            label_3d(fig, r/2, -0.4, -h/2-0.4, "r", dim_color_r, 16)
            # height line on side
            dim_line(fig, r+0.5, 0, -h/2, r+0.5, 0, h/2, dim_color_h, 2)
            label_3d(fig, r+0.5, 0, 0, "h", dim_color_h, 16)
            st.latex(r"V = \pi r^2 h  \quad A = 2\pi r(h+r)")
            c1, c2 = st.columns(2)
            with c1: st.metric("Surface Area", f"{2*math.pi*r*(h+r):.2f}")
            with c2: st.metric("Volume", f"{math.pi*r**2*h:.2f}")

        # ── Cone ──
        elif shape == "Cone":
            r = st.slider("Base radius", 0.5, 5.0, 2.0, 0.1)
            h = st.slider("Height", 1.0, 8.0, 4.0, 0.1)
            n = 40
            tc2, zc2 = np.meshgrid(np.linspace(0, 2*np.pi, n), np.linspace(0, h, n))
            rc = r * (1 - zc2 / h)
            fig.add_trace(go.Surface(x=rc*np.cos(tc2), y=rc*np.sin(tc2), z=zc2,
                                      colorscale="Electric", opacity=0.85, showscale=False))
            # radius at base
            dim_line(fig, 0, 0, 0, r, 0, 0, dim_color_r, 2)
            label_3d(fig, r/2, -0.4, -0.4, "r", dim_color_r, 16)
            # height line
            dim_line(fig, 0, 0, 0, 0, 0, h, dim_color_h, 2)
            label_3d(fig, 0.4, 0, h/2, "h", dim_color_h, 16)
            # slant line
            sl = math.sqrt(r**2 + h**2)
            dim_line(fig, r, 0, 0, 0, 0, h, "#a855f7", 2)
            label_3d(fig, r/2, 0.4, h/2, "l", "#a855f7", 16)
            st.latex(r"V = \frac{1}{3}\pi r^2 h  \quad A = \pi r(r+l)")
            c1, c2 = st.columns(2)
            with c1: st.metric("Surface Area", f"{math.pi*r*(r+sl):.2f}")
            with c2: st.metric("Volume", f"{(1/3)*math.pi*r**2*h:.2f}")

        # ── Torus ──
        elif shape == "Torus":
            R = st.slider("Major radius", 1.0, 5.0, 3.0, 0.1)
            r = st.slider("Minor radius", 0.3, 3.0, 1.0, 0.1)
            u, v = np.mgrid[0:2*np.pi:50j, 0:2*np.pi:50j]
            fig.add_trace(go.Surface(
                x=(R + r*np.cos(v))*np.cos(u),
                y=(R + r*np.cos(v))*np.sin(u),
                z=r*np.sin(v),
                colorscale="Portland", opacity=0.9, showscale=False))
            # major radius: center → tube center
            dim_line(fig, 0, 0, 0, R, 0, 0, dim_color_R, 2)
            label_3d(fig, R/2, -0.5, 0.4, "R", dim_color_R, 16)
            # minor radius: tube center → tube surface
            dim_line(fig, R, 0, 0, R+r, 0, 0, dim_color_r, 2)
            label_3d(fig, R+r/2, -0.5, 0.4, "r", dim_color_r, 16)
            # center dot
            fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers",
                                        marker=dict(size=4, color="white"),
                                        hoverinfo="none", showlegend=False))
            st.latex(r"V = 2\pi^2 R r^2  \quad A = 4\pi^2 R r")
            c1, c2 = st.columns(2)
            with c1: st.metric("Surface Area", f"{4*math.pi**2*R*r:.2f}")
            with c2: st.metric("Volume", f"{2*math.pi**2*R*r**2:.2f}")

        # ── Helix ──
        elif shape == "Helix":
            coils = st.slider("Coils", 1, 20, 5, 1)
            r = st.slider("Radius", 0.3, 3.0, 1.5, 0.1)
            t_h = np.linspace(0, coils*2*np.pi, 500)
            z_h = np.linspace(0, 5, 500)
            fig.add_trace(go.Scatter3d(x=r*np.cos(t_h), y=r*np.sin(t_h), z=z_h,
                                        mode="lines", line=dict(color="#6366f1", width=5),
                                        showlegend=False))
            fig.add_trace(go.Scatter3d(x=[r*np.cos(t_h[-1])], y=[r*np.sin(t_h[-1])],
                                        z=[z_h[-1]], mode="markers",
                                        marker=dict(size=7, color="#ef4444"),
                                        showlegend=False))
            # radius line at z=0
            dim_line(fig, 0, 0, 0, r, 0, 0, dim_color_r, 2)
            label_3d(fig, r/2, -0.4, 0, "r", dim_color_r, 16)
            # center axis line
            dim_line(fig, 0, 0, 0, 0, 0, 5, dim_color_h, 2)
            label_3d(fig, 0.3, 0.3, 2.5, "h", dim_color_h, 16)
            # center dot at base
            fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers",
                                        marker=dict(size=4, color="white"),
                                        hoverinfo="none", showlegend=False))
            approx_len = math.sqrt((2*math.pi*r*coils)**2 + 25)
            st.info(f"**Estimated length:** {approx_len:.2f} units (one coil ≈ {approx_len/coils:.2f})")

        # ── Sinusoidal Surface ──
        elif shape == "Sinusoidal Surface":
            amp = st.slider("Amplitude", 0.5, 5.0, 2.0, 0.1)
            freq_s = st.slider("Frequency", 0.5, 5.0, 2.0, 0.1)
            xs = np.linspace(-5, 5, 50)
            ys = np.linspace(-5, 5, 50)
            xs, ys = np.meshgrid(xs, ys)
            z_surf = amp * np.sin(freq_s * np.sqrt(xs**2 + ys**2))
            fig.add_trace(go.Surface(x=xs, y=ys, z=z_surf,
                                      colorscale="Thermal", opacity=0.9, showscale=False))
            # amplitude indicator
            idx0 = np.argmin(np.abs(xs[0,:]))
            idx_peak = np.argmax(z_surf[:, idx0])
            dim_line(fig, 0, 0, 0, 0, 0, amp, dim_color_h, 2)
            label_3d(fig, 0.5, 0, amp/2, "A", dim_color_h, 16)
            st.latex(r"z = A\sin\left(f\sqrt{x^2+y^2}\right)")

        fig.update_layout(
            height=550,
            scene=dict(
                xaxis=dict(showgrid=True, gridcolor="#333", zeroline=False, showbackground=False),
                yaxis=dict(showgrid=True, gridcolor="#333", zeroline=False, showbackground=False),
                zaxis=dict(showgrid=True, gridcolor="#333", zeroline=False, showbackground=False),
                bgcolor="rgba(0,0,0,0)",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🖱️ Drag to rotate · Scroll to zoom · Dashed lines show dimensions")

# ================================================================
#                        ⚡ PHYSICS SECTION
# ================================================================
elif subject == "⚡ Physics":
    topic = st.selectbox("Topic", [
        "Projectile Motion", "Kinematics",
        "Snell's Law (Refraction)", "Ohm's Law",
        "Simple Pendulum"
    ])

    # ── Projectile ────────────────────────────────────────────
    if topic == "Projectile Motion":
        st.markdown("## Projectile Motion Simulator")
        col1, col2 = st.columns(2)
        with col1:
            v0 = st.slider("Initial velocity (m/s)", 1.0, 100.0, 30.0, 1.0)
            angle = st.slider("Launch angle (°)", 1.0, 89.0, 45.0, 1.0)
        with col2:
            h0 = st.slider("Initial height (m)", 0.0, 50.0, 0.0, 1.0)
            g = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, 0.01)

        rad = math.radians(angle)
        vx = v0 * math.cos(rad)
        vy0 = v0 * math.sin(rad)
        
        t_flight = (vy0 + math.sqrt(vy0**2 + 2*g*h0)) / g
        max_h = h0 + vy0**2 / (2*g)
        x_range = vx * t_flight

        t = np.linspace(0, t_flight, 300)
        x_pos = vx * t
        y_pos = h0 + vy0 * t - 0.5 * g * t**2

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_pos, y=y_pos, mode="lines",
                                  name="Trajectory", line=dict(color="#6366f1", width=3)))
        fig.add_trace(go.Scatter(x=[x_pos[-1]], y=[y_pos[-1]], mode="markers",
                                  marker=dict(size=10, color="#ef4444"), name="Landing"))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                          xaxis_title="Distance (m)", yaxis_title="Height (m)",
                          yaxis_range=[0, max_h * 1.1])
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Flight time", f"{t_flight:.2f} s")
        with col2: st.metric("Range", f"{x_range:.2f} m")
        with col3: st.metric("Max height", f"{max_h:.2f} m")
        with col4: st.metric("Final velocity", f"{math.sqrt(vx**2 + (vy0 - g*t_flight)**2):.2f} m/s")

    # ── Kinematics ────────────────────────────────────────────
    elif topic == "Kinematics":
        st.markdown("## Kinematics — Motion Graphs")
        st.latex(r"v = u + at \quad\quad s = ut + \frac{1}{2}at^2 \quad\quad v^2 = u^2 + 2as")

        u = st.slider("Initial velocity u (m/s)", -50.0, 50.0, 10.0, 1.0)
        a_val = st.slider("Acceleration a (m/s²)", -20.0, 20.0, 2.0, 0.5)
        t_max = st.slider("Time range (s)", 1.0, 20.0, 10.0, 0.5)

        t = np.linspace(0, t_max, 400)
        v = u + a_val * t
        s = u * t + 0.5 * a_val * t**2

        fig = make_subplots(rows=2, cols=1, subplot_titles=("Velocity vs Time", "Displacement vs Time"),
                             shared_xaxes=True, vertical_spacing=0.08)
        fig.add_trace(go.Scatter(x=t, y=v, line=dict(color="#6366f1", width=2), name="v(t)"), row=1, col=1)
        fig.add_trace(go.Scatter(x=t, y=s, line=dict(color="#10b981", width=2), name="s(t)"), row=2, col=1)
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"), row=1, col=1)
        fig.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        st.plotly_chart(fig, use_container_width=True)

    # ── Snell's Law ──────────────────────────────────────────
    elif topic == "Snell's Law (Refraction)":
        st.markdown("## Snell's Law of Refraction")
        st.latex(r"n_1 \sin\theta_1 = n_2 \sin\theta_2")

        n1 = st.number_input("Refractive index n₁", 1.0, 3.0, 1.0, 0.01)
        n2 = st.number_input("Refractive index n₂", 1.0, 3.0, 1.5, 0.01)
        theta1 = st.slider("Angle of incidence θ₁ (°)", 0, 89, 45, 1)

        sin_theta2 = n1 * math.sin(math.radians(theta1)) / n2
        if sin_theta2 > 1:
            st.error("🔴 Total internal reflection — sin(θ₂) > 1")
            theta2 = None
        else:
            theta2 = math.degrees(math.asin(sin_theta2))
            st.success(f"**Angle of refraction θ₂:** {theta2:.2f}°")

        # Visual
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[-2, 2], y=[0, 0], mode="lines",
                                  line=dict(color="#555", width=2), name="Interface"))
        # Incident ray
        x1 = -2 * math.sin(math.radians(theta1))
        y1 = 2 * math.cos(math.radians(theta1))
        fig.add_trace(go.Scatter(x=[0, x1], y=[0, y1], mode="lines",
                                  line=dict(color="#f59e0b", width=2), name="Incident ray"))
        fig.add_annotation(x=x1/2, y=y1/2, text=f"θ₁={theta1}°", showarrow=False,
                           font=dict(color="#f59e0b"))

        if theta2:
            x2 = 2 * math.sin(math.radians(theta2))
            y2 = -2 * math.cos(math.radians(theta2))
            fig.add_trace(go.Scatter(x=[0, x2], y=[0, y2], mode="lines",
                                      line=dict(color="#6366f1", width=2), name="Refracted ray"))
            fig.add_annotation(x=x2/2, y=y2/2, text=f"θ₂={theta2:.1f}°", showarrow=False,
                               font=dict(color="#6366f1"))

        fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
                                  marker=dict(size=8, color="white"), name="Point"))
        fig.update_layout(height=450, xaxis_range=[-2.5, 2.5], yaxis_range=[-2.5, 2.5],
                          xaxis=dict(scaleanchor="y"), margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    # ── Ohm's Law ────────────────────────────────────────────
    elif topic == "Ohm's Law":
        st.markdown("## Ohm's Law")
        st.latex(r"V = I \times R")
        mode = st.radio("Calculate:", ["V from I & R", "I from V & R", "R from V & I"], horizontal=True)

        if mode == "V from I & R":
            I = st.slider("Current I (A)", 0.0, 10.0, 2.0, 0.1)
            R = st.slider("Resistance R (Ω)", 0.1, 100.0, 10.0, 0.1)
            V = I * R
            st.success(f"**V = {V:.2f} V**")
        elif mode == "I from V & R":
            V = st.slider("Voltage V (V)", 0.0, 240.0, 12.0, 0.1)
            R = st.slider("Resistance R (Ω)", 0.1, 100.0, 10.0, 0.1)
            I = V / R
            st.success(f"**I = {I:.4f} A**")
        else:
            V = st.slider("Voltage V (V)", 0.0, 240.0, 12.0, 0.1)
            I = st.slider("Current I (A)", 0.0, 10.0, 1.2, 0.1)
            R = V / I if I > 0 else float("inf")
            st.success(f"**R = {R:.2f} Ω**")

        # I-V graph
        st.markdown("### I-V Characteristic")
        r_fixed = st.slider("Fixed resistance for graph (Ω)", 1.0, 100.0, 10.0, 1.0, key="iv_r")
        v_vals = np.linspace(0, 50, 200)
        i_vals = v_vals / r_fixed
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=v_vals, y=i_vals, mode="lines",
                                  line=dict(color="#6366f1", width=2), name=f"R = {r_fixed}Ω"))
        fig.update_layout(height=350, xaxis_title="Voltage (V)", yaxis_title="Current (A)",
                          margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    # ── Pendulum ─────────────────────────────────────────────
    elif topic == "Simple Pendulum":
        st.markdown("## Simple Pendulum")
        st.latex(r"T = 2\pi\sqrt{\frac{L}{g}}")

        L = st.slider("Length L (m)", 0.1, 5.0, 1.0, 0.1)
        g_p = st.slider("Gravity g (m/s²)", 1.0, 20.0, 9.81, 0.01)
        
        T = 2 * math.pi * math.sqrt(L / g_p)
        st.success(f"**Period T = {T:.4f} s**")
        st.info(f"Frequency f = {1/T:.4f} Hz")

        # Animation via time slider
        time = st.slider("Time (s)", 0.0, T * 2, 0.0, 0.01)
        theta0 = math.radians(30)
        theta_t = theta0 * math.cos(2 * math.pi * time / T)

        fig = go.Figure()
        x_bob = L * math.sin(theta_t)
        y_bob = -L * math.cos(theta_t)
        fig.add_trace(go.Scatter(x=[0, x_bob], y=[0, y_bob], mode="lines+markers",
                                  line=dict(color="#6366f1", width=3),
                                  marker=dict(size=[0, 12], color=["#6366f1", "#ef4444"]),
                                  name="Pendulum"))
        fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
                                  marker=dict(size=6, color="#555"), name="Pivot"))
        fig.update_layout(height=450, xaxis_range=[-L-0.3, L+0.3], yaxis_range=[-L-0.3, 0.3],
                          xaxis=dict(scaleanchor="y"), margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

# ================================================================
#                       🧪 CHEMISTRY SECTION
# ================================================================
elif subject == "🧪 Chemistry":
    topic = st.selectbox("Topic", [
        "pH Calculator", "Molar Mass Calculator",
        "Stoichiometry", "Ideal Gas Law",
        "Periodic Trend Explorer"
    ])

    # ── pH ────────────────────────────────────────────────────
    if topic == "pH Calculator":
        st.markdown("## pH Calculator")
        st.latex(r"\text{pH} = -\log_{10}[H^+] \quad\quad \text{pOH} = -\log_{10}[OH^-]")
        st.latex(r"\text{pH} + \text{pOH} = 14")

        mode = st.radio("Input mode:", ["[H⁺] concentration", "[OH⁻] concentration", "pH value"], horizontal=True)

        if mode == "[H⁺] concentration":
            h_conc = st.number_input("[H⁺] (mol/L)", 1e-14, 1.0, 1e-7, format="%.2e")
            ph = -math.log10(h_conc)
            poh = 14 - ph
            oh = 10**-poh
        elif mode == "[OH⁻] concentration":
            oh_conc = st.number_input("[OH⁻] (mol/L)", 1e-14, 1.0, 1e-7, format="%.2e")
            poh = -math.log10(oh_conc)
            ph = 14 - poh
            h_conc = 10**-ph
            oh = oh_conc
        else:
            ph = st.number_input("pH", 0.0, 14.0, 7.0, 0.01)
            h_conc = 10**-ph
            poh = 14 - ph
            oh = 10**-poh

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("pH", f"{ph:.2f}")
        with col2: st.metric("pOH", f"{pOH:.2f}")
        with col3: st.metric("[OH⁻]", f"{oh:.2e} mol/L")

        if ph < 3: label, color = "Strong acid", "#ef4444"
        elif ph < 7: label, color = "Acid", "#f59e0b"
        elif ph == 7: label, color = "Neutral", "#10b981"
        elif ph < 11: label, color = "Base", "#3b82f6"
        else: label, color = "Strong base", "#8b5cf6"

        st.markdown(f'<div style="background:{color}33; border-left:4px solid {color}; padding:0.5rem 1rem; border-radius:6px;">'
                    f'<strong>{label}</strong> — pH {ph:.2f}</div>', unsafe_allow_html=True)

        # pH scale visual
        colors = ["#ef4444","#f97316","#f59e0b","#eab308","#84cc16","#22c55e","#10b981"]
        fig = go.Figure()
        for i in range(0, 14):
            fig.add_trace(go.Scatter(x=[i, i+1], y=[0, 0], mode="lines",
                                      line=dict(width=20, color=px.colors.sequential.Viridis[int(i/14*255)])))
        fig.add_trace(go.Scatter(x=[ph], y=[0], mode="markers",
                                  marker=dict(size=14, color="white", symbol="diamond",
                                              line=dict(color="black", width=2)),
                                  name=f"pH {ph:.2f}"))
        fig.add_vline(x=ph, line=dict(color="white", width=1, dash="dash"))
        fig.update_layout(height=100, xaxis=dict(range=[0, 14], showticklabels=True,
                                                  tickvals=list(range(0, 15))),
                          yaxis=dict(visible=False), margin=dict(l=20, r=20, t=10, b=30))
        st.plotly_chart(fig, use_container_width=True)

    # ── Molar Mass ───────────────────────────────────────────
    elif topic == "Molar Mass Calculator":
        st.markdown("## Molar Mass Calculator")
        elements = {
            "H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012, "B": 10.811,
            "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
            "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.086, "P": 30.974,
            "S": 32.065, "Cl": 35.453, "K": 39.098, "Ar": 39.948, "Ca": 40.078,
            "Fe": 55.845, "Cu": 63.546, "Zn": 65.380, "Br": 79.904, "Ag": 107.868,
            "I": 126.904, "Au": 196.967, "Hg": 200.590, "Pb": 207.200
        }

        formula = st.text_input("Enter chemical formula (e.g. H2O, CO2, H2SO4, C6H12O6)", "H2O").strip()
        
        import re
        parts = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
        total_mass = 0
        breakdown = []
        for el, count in parts:
            if el in elements:
                n = int(count) if count else 1
                mass = elements[el] * n
                total_mass += mass
                breakdown.append(f"{el}{count or ''} = {elements[el]:.3f} × {n} = {mass:.3f}")

        st.success(f"**Molar mass of {formula}: {total_mass:.4f} g/mol**")
        with st.expander("Show breakdown"):
            for line in breakdown:
                st.markdown(f"- {line}")

        st.markdown("### Mass ↔ Moles Converter")
        mass_input = st.number_input("Mass (g)", 0.0, 1000.0, 18.0, 0.1)
        moles = mass_input / total_mass
        st.info(f"{mass_input:.2f} g of {formula} = **{moles:.6f} mol**")

    # ── Stoichiometry ────────────────────────────────────────
    elif topic == "Stoichiometry":
        st.markdown("## Stoichiometry Calculator")
        st.markdown("**Reaction:** aA + bB → cC + dD")
        st.latex(r"\text{Mole ratio: } \frac{n_A}{a} = \frac{n_B}{b} = \frac{n_C}{c} = \frac{n_D}{d}")

        a = st.number_input("Coefficient of A", 1, 10, 1, key="s_a")
        b = st.number_input("Coefficient of B", 0, 10, 1, key="s_b")
        c = st.number_input("Coefficient of C", 0, 10, 1, key="s_c")
        d = st.number_input("Coefficient of D", 0, 10, 1, key="s_d")

        nA = st.number_input("Moles of A given (mol)", 0.0, 100.0, 2.0, 0.1)

        st.subheader("Results")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Moles of B needed", f"{nA * b / a:.4f} mol" if b > 0 else "N/A")
        with col2: st.metric("Moles of C produced", f"{nA * c / a:.4f} mol" if c > 0 else "N/A")
        with col3: st.metric("Moles of D produced", f"{nA * d / a:.4f} mol" if d > 0 else "N/A")

    # ── Ideal Gas Law ───────────────────────────────────────
    elif topic == "Ideal Gas Law":
        st.markdown("## Ideal Gas Law")
        st.latex(r"PV = nRT")

        P = st.slider("Pressure P (atm)", 0.1, 100.0, 1.0, 0.1)
        n = st.slider("Amount n (mol)", 0.1, 10.0, 1.0, 0.1)
        T = st.slider("Temperature T (K)", 100.0, 1500.0, 298.0, 1.0)

        R = 0.082057  # L·atm/(mol·K)
        V = n * R * T / P

        st.success(f"**Volume V = {V:.4f} L**")

        # PV graph
        v_vals = np.linspace(0.1, 50, 300)
        p_vals = n * R * T / v_vals
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=v_vals, y=p_vals, mode="lines",
                                  line=dict(color="#6366f1", width=2), name="P vs V"))
        fig.add_trace(go.Scatter(x=[V], y=[P], mode="markers",
                                  marker=dict(size=12, color="#ef4444", symbol="x"), name="Current"))
        fig.update_layout(height=350, xaxis_title="Volume (L)", yaxis_title="Pressure (atm)",
                          margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    # ── Periodic Trends ─────────────────────────────────────
    elif topic == "Periodic Trend Explorer":
        st.markdown("## Periodic Trends")
        st.markdown("Explore how properties vary across groups (columns) and down periods (rows).")

        trend = st.selectbox("Property", ["Atomic Radius (pm)", "Ionization Energy (eV)", 
                                           "Electronegativity (Pauling)", "Electron Affinity (eV)"])

        # Simplified data for periods 2 & 3
        elements_data = {
            "Li": {"Atomic Radius": 152, "Ionization Energy": 5.39, "Electronegativity": 0.98, "Electron Affinity": 0.618, "Period": 2},
            "Be": {"Atomic Radius": 112, "Ionization Energy": 9.32, "Electronegativity": 1.57, "Electron Affinity": -0.5, "Period": 2},
            "B":  {"Atomic Radius": 87,  "Ionization Energy": 8.30, "Electronegativity": 2.04, "Electron Affinity": 0.277, "Period": 2},
            "C":  {"Atomic Radius": 77,  "Ionization Energy": 11.26, "Electronegativity": 2.55, "Electron Affinity": 1.262, "Period": 2},
            "N":  {"Atomic Radius": 75,  "Ionization Energy": 14.53, "Electronegativity": 3.04, "Electron Affinity": -0.07, "Period": 2},
            "O":  {"Atomic Radius": 73,  "Ionization Energy": 13.62, "Electronegativity": 3.44, "Electron Affinity": 1.461, "Period": 2},
            "F":  {"Atomic Radius": 71,  "Ionization Energy": 17.42, "Electronegativity": 3.98, "Electron Affinity": 3.399, "Period": 2},
            "Ne": {"Atomic Radius": 69,  "Ionization Energy": 21.56, "Electronegativity": 0.0, "Electron Affinity": -1.2, "Period": 2},
            "Na": {"Atomic Radius": 186, "Ionization Energy": 5.14, "Electronegativity": 0.93, "Electron Affinity": 0.548, "Period": 3},
            "Mg": {"Atomic Radius": 160, "Ionization Energy": 7.65, "Electronegativity": 1.31, "Electron Affinity": -0.4, "Period": 3},
            "Al": {"Atomic Radius": 143, "Ionization Energy": 5.99, "Electronegativity": 1.61, "Electron Affinity": 0.433, "Period": 3},
            "Si": {"Atomic Radius": 117, "Ionization Energy": 8.15, "Electronegativity": 1.90, "Electron Affinity": 1.385, "Period": 3},
            "P":  {"Atomic Radius": 110, "Ionization Energy": 10.49, "Electronegativity": 2.19, "Electron Affinity": 0.746, "Period": 3},
            "S":  {"Atomic Radius": 104, "Ionization Energy": 10.36, "Electronegativity": 2.58, "Electron Affinity": 2.077, "Period": 3},
            "Cl": {"Atomic Radius": 99,  "Ionization Energy": 12.97, "Electronegativity": 3.16, "Electron Affinity": 3.613, "Period": 3},
            "Ar": {"Atomic Radius": 97,  "Ionization Energy": 15.76, "Electronegativity": 0.0, "Electron Affinity": -1.0, "Period": 3},
        }

        prop = "Atomic Radius" if "Radius" in trend else ("Ionization Energy" if "Ionization" in trend else ("Electronegativity" if "Electronegativity" in trend else "Electron Affinity"))
        unit = "pm" if "Radius" in trend else ("eV" if "Ionization" in trend else ("Pauling" if "Electronegativity" in trend else "eV"))

        period2 = {k: v for k, v in elements_data.items() if v["Period"] == 2}
        period3 = {k: v for k, v in elements_data.items() if v["Period"] == 3}

        fig = go.Figure()
        for label, data, color in [("Period 2", period2, "#6366f1"), ("Period 3", period3, "#10b981")]:
            names = list(data.keys())
            vals = [data[n][prop] for n in names]
            fig.add_trace(go.Scatter(x=names, y=vals, mode="lines+markers",
                                      name=label, line=dict(color=color, width=2),
                                      marker=dict(size=10, color=color)))
        fig.update_layout(height=400, xaxis_title="Element", yaxis_title=f"{prop} ({unit})",
                          margin=dict(l=20, r=20, t=20, b=20), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"💡 **Trend:** {prop} generally {'decreases' if 'Radius' in trend else 'increases'} across a period (left → right) and {'increases' if 'Radius' in trend else 'decreases'} down a group (top → bottom).")

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
