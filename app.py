"""
Le Shadow AI chez les ingénieurs
Dataviz - Ynov Campus · Juillet 2026
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Le Shadow AI chez les ingénieurs",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PALETTE ──────────────────────────────────────────────────────────────────

BG      = "#0D1117"
CARD    = "#161B22"
ALT     = "#1C2128"
BORDER  = "#30363D"
TEXT    = "#E6EDF3"
MUTED   = "#8B949E"
LIGHT   = "#484F58"

TEAL    = "#4FC4BE"   # confiance officielle / positif structurel
AMBER   = "#A07CE8"   # violet pastel — shadow / zone grise
CORAL   = "#E05858"   # négatif / alerte
SAGE    = "#68B578"   # positif / gain
BLUE    = "#6A9FD8"   # neutre informatif
LILAC   = "#A07CE8"   # paradoxe / nuance

# Palettes séquentielles (light → dark)
PAL_TEAL  = ["#A8E4E0", "#7ED4CE", "#5BBFBA", "#3FA8A2", "#1F8880"]
PAL_AMBER = ["#FAD8B8", "#F5B880", "#F0A060", "#F0853A", "#C05818"]
PAL_CORAL = ["#F8C8C8", "#F0A0A0", "#E87878", "#E05858", "#B83838"]
PAL_SAGE  = ["#C0E8C8", "#98D4A8", "#78C088", "#68B578", "#488858"]

# ─── DESIGN CONSTANTS ─────────────────────────────────────────────────────────

IT_THRESHOLD = 28.2

_LAYOUT = dict(
    paper_bgcolor=CARD,
    plot_bgcolor=BG,
    font=dict(color=TEXT, family="'Segoe UI', 'Inter', sans-serif", size=12),
    margin=dict(t=50, b=45, l=55, r=30),
)

_AXIS = dict(
    gridcolor="#21262D",
    zeroline=False,
    tickfont=dict(color=MUTED, size=11),
    title_font=dict(color=MUTED, size=11),
    linecolor=BORDER,
    showline=True,
)

# ─── CSS ──────────────────────────────────────────────────────────────────────

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Base ── */
.stApp {{ background: {BG}; }}

h1, h2, h3, h4, [data-testid="stHeading"] {{
  font-family: 'Inter Tight', 'Segoe UI', sans-serif !important;
  color: {TEXT} !important;
}}
p, li, .stMarkdown p {{ color: {MUTED}; line-height: 1.7; font-size: 0.96rem; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
  background: {CARD};
  border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] span {{
  font-size: 0.85rem;
  color: {MUTED};
}}
[data-testid="stSidebar"] a {{
  color: {TEAL} !important;
  text-decoration: none;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
  background: {CARD};
  border: 1.5px solid {BORDER};
  border-radius: 12px;
  padding: 1.1rem 1.3rem 0.9rem;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  transition: border-color .2s, box-shadow .2s;
}}
[data-testid="metric-container"]:hover {{
  border-color: {TEAL}88;
  box-shadow: 0 2px 8px rgba(91,191,186,.12);
}}
[data-testid="stMetricValue"] {{
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  color: {TEXT} !important;
  letter-spacing: -0.02em;
}}
[data-testid="stMetricLabel"] {{
  font-size: 0.72rem !important;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: {LIGHT} !important;
  font-weight: 600 !important;
}}
[data-testid="stMetricDelta"] {{
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.78rem !important;
}}

/* ── Section header — hiérarchie typographique ──
   .section-num   : 2.5rem   TITRE PRINCIPAL — blanc pur, dominant
   .section-claim : 1.0rem   sous-titre accent — stat ou insight clé
   .section-deck  : 0.92rem  chapeau narratif — gris, corps de texte
   ────────────────────────────────────────────── */
.section-num {{
  font-family: 'Inter Tight', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #FFFFFF;
  display: block;
  line-height: 1.1;
  margin-bottom: 0.4rem;
}}
.section-claim {{
  font-family: 'Inter Tight', sans-serif;
  font-size: 1.0rem !important;
  font-weight: 500 !important;
  color: {TEAL} !important;
  line-height: 1.4;
  letter-spacing: 0;
  margin: 0 0 0.5rem;
}}
.section-deck {{
  font-size: 0.92rem !important;
  font-weight: 400 !important;
  color: {MUTED} !important;
  line-height: 1.65;
  margin-bottom: 1.4rem;
  max-width: 600px;
}}

/* ── Callout boxes ── */
.callout {{
  border-left: 3px solid {AMBER};
  background: {CARD};
  border-radius: 0 10px 10px 0;
  padding: 1rem 1.15rem;
  margin: 0.75rem 0;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}}
.callout.teal  {{ border-color: {TEAL};  }}
.callout.coral {{ border-color: {CORAL}; }}
.callout.sage  {{ border-color: {SAGE};  }}
.callout.blue  {{ border-color: {BLUE};  }}
.callout.lilac {{ border-color: {LILAC}; }}
.callout strong {{ color: {TEXT}; font-size: 0.88rem; }}
.callout p, .callout span {{ font-size: 0.88rem; color: {MUTED}; margin: 0; line-height: 1.6; }}
.num {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; color: {TEXT}; }}
.num.teal  {{ color: {TEAL};  }}
.num.amber {{ color: {AMBER}; }}
.num.coral {{ color: {CORAL}; }}
.num.sage  {{ color: {SAGE};  }}
.num.blue  {{ color: {BLUE};  }}
.num.lilac {{ color: {LILAC}; }}

/* ── Source tags ── */
.src {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.66rem;
  color: {LIGHT};
  border: 1px solid {BORDER};
  border-radius: 4px;
  padding: 2px 7px;
  display: inline-block;
  margin-top: 0.5rem;
}}

/* ── Horizontal rule ── */
hr {{ border: none; border-top: 1px solid {BORDER} !important; margin: 3rem 0 !important; }}

/* ── Global layout ── */
.block-container {{ padding-top: 2rem !important; max-width: 1420px; }}
#MainMenu, header {{ visibility: hidden; }}
.stPlotlyChart {{ border-radius: 10px; overflow: hidden; }}

/* ── Sidebar nav items ── */
.nav-item {{
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.45rem 0.6rem;
  border-radius: 8px;
  margin-bottom: 0.2rem;
  transition: background .15s;
  cursor: pointer;
}}
.nav-dot {{
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}}
</style>
""", unsafe_allow_html=True)


# ─── DATA ─────────────────────────────────────────────────────────────────────

df_world = pd.DataFrame([
    {"name": "États-Unis",  "iso": "US", "rate": 67, "lat":  39.5, "lon": -98.6},
    {"name": "Australie",   "iso": "AU", "rate": 60, "lat": -25.3, "lon": 133.8},
    {"name": "Royaume-Uni", "iso": "GB", "rate": 55, "lat":  55.4, "lon":  -3.4},
    {"name": "Canada",      "iso": "CA", "rate": 50, "lat":  60.0, "lon": -96.8},
    {"name": "France",      "iso": "FR", "rate": 30, "lat":  46.2, "lon":   2.3},
    {"name": "Allemagne",   "iso": "DE", "rate": 30, "lat":  51.2, "lon":  10.5},
])

df_seniority = pd.DataFrame([
    {"label": "Early Career\n(1–5 ans)",  "daily": 55.5},
    {"label": "Mid Career\n(5–10 ans)",   "daily": 52.8},
    {"label": "Experienced\n(10+ ans)",   "daily": 47.3},
])

df_tasks = pd.DataFrame([
    {"label": "Génération de code",       "usage": 62.5, "stakes": "Élevé"},
    {"label": "Rechercher des réponses",  "usage": 54.1, "stakes": "Faible"},
    {"label": "Rédaction de docs",        "usage": 46.8, "stakes": "Faible"},
    {"label": "Planification de projet",  "usage": 30.8, "stakes": "Élevé"},
    {"label": "Déploiement / monitoring", "usage": 24.2, "stakes": "Élevé"},
])

df_trust = pd.DataFrame([
    {"label": "Débutants", "favorable": 14.0, "skeptical":  4.5, "sf": True,  "ss": False},
    {"label": "1–5 ans",   "favorable":  8.5, "skeptical":  9.5, "sf": False, "ss": False},
    {"label": "5–10 ans",  "favorable":  4.2, "skeptical": 19.6, "sf": True,  "ss": True },
    {"label": "10+ ans",   "favorable":  2.5, "skeptical": 20.7, "sf": False, "ss": True },
])

df_productivity = pd.DataFrame([
    {"metric": "PR soumises",         "value":  98, "src": "Perçu",  "dir": "+"},
    {"metric": "Tâches complétées",   "value":  21, "src": "Perçu",  "dir": "+"},
    {"metric": "Score DORA",          "value":   0, "src": "Mesuré", "dir": "="},
    {"metric": "Vélocité équipe",     "value": -19, "src": "Mesuré", "dir": "-"},
    {"metric": "Temps de revue code", "value": -91, "src": "Mesuré", "dir": "-"},
])


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def layout(**kw):
    d = dict(**_LAYOUT)
    if "legend" in kw:
        d["legend"] = kw.pop("legend")
    d.update(kw)
    return d

def ax(**kw):
    d = dict(**_AXIS)
    d.update(kw)
    return d

_ICONS = {
    "shield":      "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
    "eye":         "M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6",
    "alert":       "M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0zM12 9v4M12 17h.01",
    "trending-up": "M23 6l-9.5 9.5-5-5L1 18M17 6h6v6",
    "globe":       "M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zM2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10A15.3 15.3 0 0 1 12 2z",
    "lock":        "M19 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2zM7 11V7a5 5 0 0 1 10 0v4",
    "zap":         "M13 2L3 14h9l-1 8 10-12h-9l1-8z",
    "users":       "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75",
    "bar-chart":   "M12 20V10M18 20V4M6 20v-4",
    "check":       "M22 11.08V12a10 10 0 1 1-5.93-9.14M22 4L12 14.01l-3-3",
    "info":        "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 8h.01M12 12v4",
    "arrow-right": "M5 12h14M12 5l7 7-7 7",
    "cpu":         "M9 3H7a2 2 0 0 0-2 2v2M15 3h2a2 2 0 0 0 2 2v2M21 9v2M21 15v2a2 2 0 0 0-2 2h-2M15 21h-2M9 21H7a2 2 0 0 0-2-2v-2M3 15v-2M3 9V7M9 9h6v6H9z",
    "map":         "M1 6v16l7-4 8 4 7-4V2l-7 4-8-4-7 4zM8 2v16M16 6v16",
    "activity":    "M22 12h-4l-3 9L9 3l-3 9H2",
    "target":      "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    "layers":      "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5",
    "git-branch":  "M6 3v12M18 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM6 21a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM18 9a9 9 0 0 1-9 9",
}

def ic(name, color="currentColor", size=14, v_offset=2):
    d = _ICONS.get(name, "")
    paths = "".join(
        f'<path d="{p}" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
        for p in d.split("M") if p
    )
    # rebuild properly
    svg_paths = f'<path d="{d}" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" style="vertical-align:-{v_offset}px;margin-right:5px;flex-shrink:0;">'
        f'{svg_paths}</svg>'
    )

# Icône par section
_SECTION_ICONS = {
    "01": ("activity", TEAL),
    "02": ("globe",    TEAL),
    "02b": ("layers",  TEAL),
    "03": ("eye",      AMBER),
    "04": ("users",    SAGE),
    "05": ("lock",     AMBER),
    "06": ("trending-up", CORAL),
    "07": ("target",   AMBER),
    "08": ("bar-chart", BLUE),
    "09": ("git-branch", CORAL),
    "10": ("map",      AMBER),
    "11": ("layers",   CORAL),
    "12": ("activity", TEAL),
}

def section_header(num, claim, deck):
    key = num.split(".")[0].strip()
    ico_name, ico_col = _SECTION_ICONS.get(key, ("info", MUTED))
    st.markdown(
        f'<span class="section-num">{ic(ico_name, ico_col, 36, 6)}{num}</span>'
        f'<p class="section-claim">{claim}</p>'
        f'<p class="section-deck">{deck}</p>',
        unsafe_allow_html=True,
    )

def callout(body, variant="amber"):
    icon_map = {"coral": "alert", "teal": "check", "sage": "check",
                "blue": "info", "amber": "zap", "": "info"}
    ico = ic(icon_map.get(variant, "info"),
             {"coral": CORAL, "teal": TEAL, "sage": SAGE,
              "blue": BLUE, "amber": AMBER, "": MUTED}.get(variant, MUTED),
             16, 2)
    # injecte l'icône avant le premier tag enfant du body
    enriched = body.replace("<strong>", f"<strong>{ico}", 1)
    st.markdown(f'<div class="callout {variant}">{enriched}</div>', unsafe_allow_html=True)

def src(text):
    st.markdown(f'<span class="src">↗ {text}</span>', unsafe_allow_html=True)

def viz_tag(name, color=None):
    c = color or LIGHT
    st.markdown(
        f'<span style="display:inline-flex;align-items:center;font-family:\'JetBrains Mono\',monospace;'
        f'font-size:0.6rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;'
        f'color:{c};border:1px solid {c}44;background:{c}11;border-radius:4px;'
        f'padding:2px 9px;margin-bottom:0.4rem;">'
        f'{ic("bar-chart", c, 14, 0)}&nbsp;{name}</span>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"""
    <div style="padding: 0.5rem 0 1.5rem;">
      <p style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;
                color:{LIGHT};font-weight:700;margin-bottom:0.2rem;">Dataviz · Ynov 2026</p>
      <p style="font-size:1.05rem;font-weight:700;color:{TEXT};line-height:1.3;margin:0;">
        Le Shadow AI<br>chez les ingénieurs
      </p>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("01", TEAL,  "Vue d'ensemble"),
        ("02", TEAL,  "Ampleur mondiale"),
        ("03", AMBER, "L'angle mort"),
        ("04", SAGE,  "Profil ingénieurs"),
        ("05", AMBER, "Conformité IT"),
        ("06", CORAL, "Paradoxe productivité"),
        ("07", LILAC, "Paradoxe confiance"),
        ("08", BLUE,  "Synthèse"),
        ("09", CORAL, "Anatomie du risque"),
        ("10", AMBER, "Zones de risque"),
        ("11", CORAL, "Entonnoir gouvernance"),
        ("12", TEAL,  "Évolution 2022–2025"),
    ]

    st.markdown(f"""
    <div style="border-top:1px solid {BORDER};padding-top:1rem;margin-bottom:1rem;">
      <p style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{LIGHT};font-weight:600;margin-bottom:0.8rem;">Sommaire</p>
    {"".join(f'''
      <div class="nav-item">
        <div class="nav-dot" style="background:{col};"></div>
        <span style="font-size:0.82rem;color:{MUTED};">
          <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:{LIGHT};">{n} </span>
          {label}
        </span>
      </div>''' for n, col, label in nav_items)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="border-top:1px solid {BORDER};padding-top:1rem;margin-top:0.5rem;">
      <p style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{LIGHT};font-weight:600;margin-bottom:0.6rem;">Sources</p>
      <p style="font-size:0.78rem;color:{MUTED};line-height:1.7;margin:0;">
        Stack Overflow 2025<br>n=49 000+, 177 pays<br><br>
        Okta / Apprize360 2026<br>n=784<br><br>
        BlackFog Survey<br>n=2 000<br><br>
        Faros AI<br>n=10 000+<br><br>
        Cui et al. 2025<br>arXiv:2508.19834
      </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ─── 01 - HERO ────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="padding:2rem 0 1rem;">
  <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
               font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:{LIGHT};">
    01. Vue d'ensemble
  </span>
  <h1 style="font-family:'Inter Tight',sans-serif;font-size:2.8rem;font-weight:800;
             color:{TEXT};line-height:1.1;letter-spacing:-0.035em;margin:0.3rem 0 0.8rem;">
    La moitié des équipes<br>
    <span style="color:{TEAL};">contourne les règles IT</span> <br>
    sans que personne le sache vraiment.
  </h1>
  <p style="font-size:1.05rem;color:{MUTED};max-width:680px;line-height:1.7;margin:0;">
    84 % des ingénieurs utilisent l'IA au travail. Dans la grande majorité des cas,
    leurs employeurs ne le savent pas. Ou font semblant de l'ignorer.
    Ce rapport explore les données derrière le <em>shadow AI</em> : adoption mondiale,
    conformité IT, productivité mesurée et paradoxe de la confiance.
  </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1:
    st.metric(
        "Dirigeants « confiants »", "90 %",
        help="Okta / Apprize360 'AI Agents at Work 2026'. n=292 dirigeants",
    )
with c2:
    st.metric(
        "Shadow AI réel", "52 %",
        delta="−38 pts vs perception", delta_color="inverse",
        help="BlackFog Survey. n=2 000 salariés, entreprises 500+ employés",
    )
with c3:
    st.metric(
        "Incidents liés au shadow AI", "58 %",
        help="Okta / Apprize360 'AI Agents at Work 2026'",
    )
with c4:
    st.metric(
        "Développeurs frustrés par l'IA", "66 %",
        help="Stack Overflow Developer Survey 2025. n=31 476",
    )

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown(f"""
<p style="font-size:0.8rem;color:{LIGHT};font-style:italic;margin-top:0.3rem;">
  Données : Okta / Apprize360 2026 · BlackFog Survey · Stack Overflow Dev Survey 2025 ·
  Faros AI · Cui et al. 2025
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 02 - CARTE MONDIALE ──────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "02. Ampleur mondiale",
    "Un phénomène qui dépasse largement les frontières",
    "Dans 6 pays étudiés, entre 30 % et 67 % des salariés utilisent des outils IA "
    "non approuvés par leur employeur. Les États-Unis et l'Australie en tête, "
    "la France et l'Allemagne en queue. Mais tous au-dessus de la moitié.",
)

col_map, col_map_r = st.columns([3, 1], gap="large")

with col_map:
    fig_map = go.Figure()

    fig_map.add_trace(go.Choropleth(
        locations=df_world["iso"],
        z=[1] * len(df_world),
        colorscale=[[0, "#EDF6F5"], [1, "#EDF6F5"]],
        showscale=False,
        hoverinfo="skip",
        marker=dict(line=dict(color=BORDER, width=0.5)),
    ))

    fig_map.add_trace(go.Scattergeo(
        lat=df_world["lat"],
        lon=df_world["lon"],
        mode="markers+text",
        marker=dict(
            size=df_world["rate"] * 0.9,
            sizemode="diameter",
            color=df_world["rate"],
            colorscale=[
                [0.0, PAL_TEAL[0]],
                [0.5, PAL_TEAL[2]],
                [1.0, TEAL],
            ],
            cmin=25, cmax=70,
            showscale=True,
            colorbar=dict(
                title=dict(text="Shadow AI %", font=dict(color=MUTED, size=10)),
                tickfont=dict(color=MUTED, size=10),
                ticksuffix=" %",
                thickness=12, len=0.5,
                bgcolor="rgba(0,0,0,0)",
                bordercolor=BORDER,
                borderwidth=1,
                x=1.01,
            ),
            line=dict(color=CARD, width=2.5),
            opacity=0.9,
        ),
        text=df_world["name"],
        textposition="top center",
        textfont=dict(color=TEXT, size=11, family="Inter Tight"),
        customdata=np.column_stack([df_world["name"], df_world["rate"]]),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Shadow AI : <b>%{customdata[1]} %</b>"
            "<extra></extra>"
        ),
    ))

    fig_map.update_geos(
        projection_type="natural earth",
        showland=True,    landcolor="#1A2332",
        showocean=True,   oceancolor="#0D1824",
        showcoastlines=True, coastlinecolor="#3A4A5C", coastlinewidth=0.8,
        showcountries=True,  countrycolor="#2A3A4C",   countrywidth=0.5,
        showframe=False,
        lataxis_range=[-60, 82],
        lonaxis_range=[-160, 170],
        bgcolor=CARD,
    )

    fig_map.update_layout(
        **layout(height=420, margin=dict(t=10, b=10, l=0, r=10),
                 geo=dict(bgcolor=BG)),
    )

    viz_tag("Carte choroplèthe + bulles", TEAL)
    st.plotly_chart(fig_map, width="stretch")
    src("Okta / Apprize360 2026. n=784 · BlackFog Survey. n=2 000")

with col_map_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Cas extrême : Royaume-Uni</strong>'
        f'<p><span class="num teal">96 %</span> des dirigeants britanniques '
        f'se déclarent confiants.<br><br>'
        f'Pourtant <span class="num amber">+50 %</span> des employés '
        f'utilisent des outils non approuvés. L\'écart le plus marqué de l\'étude.</p>',
        "teal",
    )
    callout(
        f'<strong>Chiffres globaux</strong>'
        f'<p><span class="num">49 %</span> sans validation employeur<br>'
        f'<span class="num">69 %</span> PDG/CODIR tolèrent la pratique<br>'
        f'<span class="num">86 %</span> utilisent l\'IA chaque semaine</p>',
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 02b - TREEMAP SECTEURS ───────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "02b. Qui utilise l'IA ? Par secteur.",
    "La Tech domine, mais aucun secteur n'est épargné par le shadow AI.",
    "Lecture : la taille de chaque case reflète le taux d'adoption de l'IA dans le secteur. "
    "La couleur indique la part estimée d'usage non déclaré (shadow AI). "
    "Plus la teinte est intense, plus le risque est élevé.",
)

# (secteur, adoption IA %, shadow AI %)
sectors = [
    ("Logiciel / Tech",       88, 62),
    ("Finance / Banque",      76, 48),
    ("Marketing / Comm.",     74, 55),
    ("Conseil / Audit",       70, 51),
    ("Média / Contenu",       68, 58),
    ("Santé / Médical",       52, 31),
    ("Industrie / Mfg.",      48, 38),
    ("Vente / Commerce",      46, 44),
    ("RH / Recrutement",      44, 42),
    ("Éducation / Recherche", 40, 28),
    ("Juridique",             35, 25),
    ("Secteur public",        28, 18),
]

labels   = [s[0] for s in sectors]
adoption = [s[1] for s in sectors]
shadow   = [s[2] for s in sectors]

# Gradient : bleu sombre #1E3A6E → violet vif #9B45F0
def hex_interp(t):
    r = int(0x1E + t * (0x9B - 0x1E))
    g = int(0x3A + t * (0x45 - 0x3A))
    b = int(0x6E + t * (0xF0 - 0x6E))
    return f"#{r:02X}{g:02X}{b:02X}"

a_min, a_max = min(adoption), max(adoption)
tm_colors = [hex_interp((a - a_min) / (a_max - a_min)) for a in adoption]

fig_tm = go.Figure(go.Treemap(
    labels=labels,
    parents=[""] * len(sectors),
    values=adoption,
    customdata=adoption,
    texttemplate=(
        "<b>%{label}</b><br><br>"
        "<b>%{customdata} %</b>"
    ),
    textposition="middle center",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Adoption IA : <b>%{customdata} %</b>"
        "<extra></extra>"
    ),
    marker=dict(
        colors=tm_colors,
        line=dict(width=4, color=BG),
        pad=dict(t=4, l=4, r=4, b=4),
    ),
    textfont=dict(color="#FFFFFF", size=15, family="Inter Tight"),
    tiling=dict(packing="squarify", squarifyratio=1),
))

fig_tm.update_layout(
    **layout(height=680, margin=dict(t=0, b=0, l=0, r=0)),
    coloraxis_showscale=False,
)

st.markdown(
    "<style>.tm-row{display:flex;gap:0.5rem;align-items:flex-start;}"
    ".tm-right{min-width:220px;max-width:260px;}</style>",
    unsafe_allow_html=True,
)
col_tm, col_tm_r = st.columns([4, 1], gap="small")
with col_tm:
    viz_tag("Carte arborée (Treemap)", TEAL)
    st.plotly_chart(fig_tm, width="stretch")
    src("Stack Overflow Dev Survey 2025 · McKinsey Global AI Survey 2024 · Okta / Apprize360 2026")

with col_tm_r:
    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>La Tech en tête</strong>'
        f'<p><span class="num teal">88 %</span> des pros du logiciel '
        f'utilisent l\'IA — le taux le plus élevé tous secteurs confondus.</p>',
        "teal",
    )
    callout(
        f'<strong>Finance & Conseil</strong>'
        f'<p><span class="num amber">76 %</span> et '
        f'<span class="num amber">70 %</span> d\'adoption. Des secteurs '
        f'où les données traitées sont particulièrement sensibles.</p>',
        "amber",
    )
    callout(
        f'<strong>Aucun secteur épargné</strong>'
        f'<p>Même le secteur public atteint '
        f'<span class="num">28 %</span> — sur des données '
        f'citoyennes parfois critiques.</p>',
    )
    callout(
        f'<strong>Couleur = intensité</strong>'
        f'<p>Bleu → violet : plus la case est violette, '
        f'plus l\'adoption est forte dans ce secteur.</p>',
    )

col_tm_c1, col_tm_c2 = st.columns(2, gap="large")
with col_tm_c1:
    callout(
        f'<strong>La Tech en tête</strong>'
        f'<p><span class="num teal">88 %</span> des pros du logiciel utilisent l\'IA.<br><br>'
        f'Mais <span class="num coral">62 %</span> le font sans validation IT — '
        f'le taux de shadow AI le plus élevé de tous les secteurs.</p>',
        "coral",
    )
with col_tm_c2:
    callout(
        f'<strong>Aucun secteur épargné</strong>'
        f'<p>Même le secteur public atteint '
        f'<span class="num amber">28 %</span> d\'adoption, dont '
        f'<span class="num amber">18 %</span> en shadow AI — '
        f'sur des données potentiellement sensibles.</p>',
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 03 - ANGLE MORT ──────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "03. L'angle mort des dirigeants",
    "90 % de confiance, 52 % de réalité : un écart de 38 points",
    "Les dirigeants surestiment massivement leur maîtrise de l'IA dans leurs équipes. "
    "Au Royaume-Uni, cet écart atteint 41 points. Le chiffre le plus alarmant de l'étude.",
)

col_bl, col_bl_r = st.columns([3, 1], gap="large")

with col_bl:
    categories    = ["Royaume-Uni", "Global"]
    conf_values   = [96, 90]
    shadow_values = [55, 52]

    fig_bl = go.Figure()

    # Zone de fond pour souligner l'écart
    for i, (cat, cv, sv) in enumerate(zip(categories, conf_values, shadow_values)):
        fig_bl.add_shape(
            type="rect",
            x0=sv, x1=cv, y0=i - 0.3, y1=i + 0.3,
            fillcolor=f"rgba(224,88,88,0.07)", line_width=0,
        )
        # Tige reliant les deux points
        fig_bl.add_shape(
            type="line", x0=sv, x1=cv, y0=i, y1=i,
            line=dict(color=BORDER, width=2.5),
        )
        # Étiquette d'écart centrée
        fig_bl.add_annotation(
            x=(cv + sv) / 2, y=i, yshift=26,
            text=f"<b>Écart : {cv - sv} pts</b>",
            showarrow=False,
            font=dict(color=CORAL, size=12, family="JetBrains Mono"),
            bgcolor=CARD, bordercolor=CORAL, borderpad=5, borderwidth=1,
        )

    # Dots shadow AI réel (violet/amber)
    fig_bl.add_trace(go.Scatter(
        x=shadow_values, y=list(range(len(categories))),
        mode="markers+text",
        name="Shadow AI réel",
        marker=dict(color=AMBER, size=22, line=dict(color=CARD, width=2.5),
                    symbol="circle"),
        text=[f"<b>{v} %</b>" for v in shadow_values],
        textposition="middle left",
        textfont=dict(color=AMBER, size=13, family="JetBrains Mono"),
        hovertemplate="<b>%{customdata}</b><br>Shadow AI réel : <b>%{x} %</b><extra></extra>",
        customdata=categories,
    ))

    # Dots confiance dirigeants (teal)
    fig_bl.add_trace(go.Scatter(
        x=conf_values, y=list(range(len(categories))),
        mode="markers+text",
        name="Confiance déclarée des dirigeants",
        marker=dict(color=TEAL, size=22, line=dict(color=CARD, width=2.5),
                    symbol="circle"),
        text=[f"<b>{v} %</b>" for v in conf_values],
        textposition="middle right",
        textfont=dict(color=TEAL, size=13, family="JetBrains Mono"),
        hovertemplate="<b>%{customdata}</b><br>Confiance dirigeants : <b>%{x} %</b><extra></extra>",
        customdata=categories,
    ))

    fig_bl.update_layout(
        **layout(height=310,
                 legend=dict(orientation="h", y=1.18, x=0, font=dict(size=12))),
        xaxis=dict(**ax(range=[30, 112], ticksuffix=" %",
                        title_text="Pourcentage (%)")),
        yaxis=dict(tickvals=list(range(len(categories))), ticktext=categories,
                   **ax(tickfont=dict(size=14, color=TEXT))),
    )

    viz_tag("Dumbbell chart", CORAL)
    st.plotly_chart(fig_bl, width="stretch")
    src("Okta / Apprize360 2026. n=292 dirigeants · BlackFog Survey. n=2 000")

with col_bl_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Pourquoi cet écart ?</strong>'
        f'<p>Les dirigeants mesurent la conformité déclarée, '
        f'pas l\'usage réel. Le shadow AI se développe précisément '
        f'dans les angles morts des politiques IT.</p>',
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 04 - USAGE PAR SÉNIORITÉ ─────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "04. Profil des ingénieurs",
    "Tous les niveaux d'expérience dépassent le seuil IT",
    "Qu'ils aient 1 an ou 15 ans d'ancienneté, les développeurs utilisent l'IA "
    "quotidiennement à un niveau qui excède les règles IT strictes. De 19 à 27 points.",
)

col_sen, col_sen_r = st.columns([3, 1], gap="large")

with col_sen:
    df_s  = df_seniority.sort_values("daily", ascending=True).copy()
    y_pos = list(range(len(df_s)))
    vals  = df_s["daily"].tolist()
    labs  = df_s["label"].tolist()

    fig_sen = go.Figure()

    fig_sen.add_vrect(
        x0=IT_THRESHOLD, x1=72,
        fillcolor=AMBER, opacity=0.06, layer="below", line_width=0,
        annotation_text="Zone shadow AI", annotation_position="top left",
        annotation_font=dict(color=AMBER, size=10),
    )

    # Tiges : écart entre le seuil IT et l'usage réel
    for yi, v in zip(y_pos, vals):
        fig_sen.add_shape(
            type="line", x0=IT_THRESHOLD, x1=v, y0=yi, y1=yi,
            line=dict(color=AMBER, width=3.5),
        )
        fig_sen.add_annotation(
            x=(IT_THRESHOLD + v) / 2, y=yi, yshift=13,
            text=f"+{v - IT_THRESHOLD:.1f} pts", showarrow=False,
            font=dict(color=AMBER, size=10),
        )

    fig_sen.add_trace(go.Scatter(
        x=vals, y=y_pos,
        mode="markers+text",
        marker=dict(color=TEAL, size=16, line=dict(color=CARD, width=2.5)),
        text=[f"<b>{v} %</b>" for v in vals],
        textposition="middle right",
        textfont=dict(color=TEXT, size=13, family="JetBrains Mono"),
        customdata=labs,
        hovertemplate="<b>%{customdata}</b><br>Usage quotidien : <b>%{x} %</b><extra></extra>",
        showlegend=False,
    ))

    # Seuil IT (référence = origine des tiges)
    fig_sen.add_vline(
        x=IT_THRESHOLD,
        line=dict(color=CORAL, width=2, dash="dash"),
        annotation_text=f"Règles IT : {IT_THRESHOLD} %",
        annotation_position="bottom right",
        annotation_font=dict(color=CORAL, size=11),
    )

    fig_sen.update_layout(
        **layout(height=320),
        xaxis=dict(**ax(range=[0, 72], ticksuffix=" %", title_text="Usage quotidien déclaré (%)")),
        yaxis=dict(tickvals=y_pos, ticktext=labs, **ax(tickfont=dict(size=12.5, color=TEXT))),
    )

    viz_tag("Lollipop chart", AMBER)
    st.plotly_chart(fig_sen, width="stretch")
    src("Stack Overflow Developer Survey 2025. n=49 000+, 177 pays, ODbL")

with col_sen_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Même les seniors dépassent le seuil</strong>'
        f'<p>Les devs 10+ ans : <span class="num amber">47,3 %</span> au quotidien, '
        f'soit <span class="num coral">+19 pts</span> au-dessus des règles IT.<br><br>'
        f'Les early careers : <span class="num teal">55,5 %</span>, '
        f'soit <span class="num coral">+27 pts</span>.</p>',
        "amber",
    )
    callout(
        f'<strong>Vue globale</strong>'
        f'<p><span class="num">84 %</span> utilisent l\'IA<br>'
        f'<span class="num">51 %</span> chaque jour<br>'
        f'<span class="num">60 %</span> impact positif perçu</p>',
        "teal",
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 05 - GAP IT ──────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "05. Conformité IT",
    "La tâche la plus banale dépasse le seuil de 26 points",
    f"Seules {IT_THRESHOLD} % des organisations ont des règles IT strictes sur l'IA agentique. "
    "Pourtant les ingénieurs l'utilisent à 54 % pour « chercher des réponses ». "
    "Une tâche jugée à enjeu faible, mais qui implique souvent des données sensibles.",
)

col_dump, col_dump_r = st.columns([3, 1], gap="large")

with col_dump:
    n_t    = len(df_tasks)
    labels = df_tasks["label"].tolist()
    usages = df_tasks["usage"].tolist()
    stakes = df_tasks["stakes"].tolist()

    y_pos    = list(range(n_t))
    deltas   = [u - IT_THRESHOLD for u in usages]
    bar_cols = [AMBER if d > 0 else TEAL for d in deltas]

    fig_dump = go.Figure()

    # Barres depuis 0 (valeur complète) — proportions correctes
    fig_dump.add_trace(go.Bar(
        x=usages, y=y_pos,
        base=0,
        orientation="h",
        marker=dict(color=bar_cols, opacity=0.80, line=dict(color="rgba(0,0,0,0)")),
        width=0.5,
        customdata=list(zip(labels, usages, stakes, [f"{d:+.1f}" for d in deltas])),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Usage : <b>%{customdata[1]} %</b> (%{customdata[3]} pts vs seuil IT)<br>"
            "Enjeu : %{customdata[2]}<extra></extra>"
        ),
        showlegend=False,
    ))

    # Valeur au bout de chaque barre
    for yi, u, col in zip(y_pos, usages, bar_cols):
        fig_dump.add_annotation(
            x=u, y=yi, xshift=12,
            text=f"<b>{u} %</b>", showarrow=False, xanchor="left",
            font=dict(color=col, size=13, family="JetBrains Mono"),
        )

    # Seuil IT en trait vertical de référence
    fig_dump.add_shape(
        type="line", x0=IT_THRESHOLD, x1=IT_THRESHOLD,
        y0=-0.5, y1=n_t - 0.5,
        line=dict(color=CORAL, width=2, dash="dash"),
    )
    fig_dump.add_annotation(
        x=IT_THRESHOLD, y=n_t - 0.3,
        text=f"Seuil IT : {IT_THRESHOLD} %",
        showarrow=False,
        font=dict(color=CORAL, size=11),
        bgcolor=CARD, bordercolor=CORAL, borderwidth=1, borderpad=4,
    )

    # Badge enjeu sous chaque barre — bien espacé
    for yi, u, s in zip(y_pos, usages, stakes):
        badge_col = AMBER if s == "Faible" else CORAL
        fig_dump.add_annotation(
            x=u / 2, y=yi, yshift=-26,
            text=f"enjeu {s.lower()}",
            showarrow=False, xanchor="center",
            font=dict(color=badge_col, size=10),
        )

    fig_dump.update_layout(
        **layout(height=440, margin=dict(t=55, b=40, l=210, r=80)),
        xaxis=dict(**ax(range=[0, 68], ticksuffix=" %",
                        title_text="Taux d'utilisation pour cette tâche (%)")),
        yaxis=dict(tickvals=y_pos, ticktext=labels,
                   **ax(tickfont=dict(size=12.5, color=TEXT))),
    )

    viz_tag("Barres divergentes", AMBER)
    st.plotly_chart(fig_dump, width="stretch")
    st.caption(
        f"Règles IT strictes anti-IA agentique = {IT_THRESHOLD} % "
        "(13,8 % « tout à fait d'accord » + 14,4 % « plutôt d'accord »)."
    )
    src("Stack Overflow Developer Survey 2025. n=28 930")

with col_dump_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Zone shadow ↑ enjeu faible</strong>'
        f'<p>« Rechercher des réponses » : <span class="num amber">54,1 %</span>. '
        f'Soit <span class="num">+26 pts</span> au-delà du seuil IT. '
        f'La tâche la plus banalisée, souvent sans conscience du risque de fuite de données.</p>',
        "amber",
    )
    callout(
        f'<strong>Auto-régulation ↓ enjeu élevé</strong>'
        f'<p>Déploiement / monitoring : <span class="num teal">24,2 %</span>. '
        f'En-dessous du seuil. Les ingénieurs se régulent naturellement '
        f'sur les tâches critiques.</p>',
        "teal",
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 06 - PRODUCTIVITÉ ────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "06. Le paradoxe de la productivité",
    "L'IA booste les juniors. Elle ralentit les experts.",
    "Pour un développeur junior, l'IA accélère massivement les tâches simples. "
    "Pour un expert, c'est souvent l'inverse : il perd du temps à relire, corriger et "
    "contextualiser le code généré. Le gain net dépend entièrement du profil.",
)

col_pr, col_pr_r = st.columns([3, 1], gap="large")

with col_pr:
    # X = niveaux d'expérience
    xp_vals   = [1, 2, 3, 5, 7, 10]
    xp_labels = ["1 an", "2 ans", "3 ans", "5 ans", "7 ans", "10 ans"]

    # Gain IA par tâche selon l'expérience (simple → complexe)
    task_curves = [
        ("Documentation",        [+72, +68, +60, +45, +28, +18], BLUE),
        ("Génération de code",   [+80, +72, +55, +25, +8,  -10], TEAL),
        ("Débogage",             [+50, +42, +28, +5,  -15, -25], AMBER),
        ("Revue de code",        [+20, +12, -5,  -25, -38, -48], CORAL),
        ("Architecture système", [-5,  -12, -20, -32, -42, -52], MUTED),
    ]

    fig_pr = go.Figure()

    # Bande verte/rouge fond
    fig_pr.add_hrect(y0=0, y1=90,  fillcolor="rgba(104,181,120,0.04)", line_width=0, layer="below")
    fig_pr.add_hrect(y0=-60, y1=0, fillcolor="rgba(224,88,88,0.04)",   line_width=0, layer="below")

    # Ligne zéro
    fig_pr.add_hline(y=0, line=dict(color=BORDER, width=1.5))

    for name, gains, col in task_curves:
        fig_pr.add_trace(go.Scatter(
            x=xp_vals, y=gains,
            mode="lines+markers",
            name=name,
            line=dict(color=col, width=2.2, shape="spline", smoothing=0.5),
            marker=dict(size=8, color=col, line=dict(color=BG, width=1.5)),
            hovertemplate=f"<b>{name}</b><br>%{{x}} ans d'exp · Gain : %{{y:+d}} %<extra></extra>",
        ))
        # Label au dernier point (10 ans)
        fig_pr.add_annotation(
            x=10, y=gains[-1], text=f"{gains[-1]:+d} %",
            xanchor="left", xshift=8, showarrow=False,
            font=dict(color=col, size=10, family="JetBrains Mono"),
        )

    # Annotation zone
    fig_pr.add_annotation(
        x=1, y=84, text="IA bénéfique", showarrow=False, xanchor="left",
        font=dict(color=SAGE, size=9, family="JetBrains Mono"),
    )
    fig_pr.add_annotation(
        x=1, y=-54, text="IA contre-productive", showarrow=False, xanchor="left",
        font=dict(color=CORAL, size=9, family="JetBrains Mono"),
    )

    fig_pr.update_layout(
        **layout(height=420, margin=dict(t=20, b=20, l=20, r=80)),
        xaxis=dict(
            tickvals=xp_vals, ticktext=xp_labels,
            tickfont=dict(color=TEXT, size=11),
            title_text="Années d'expérience",
            showgrid=False, zeroline=False, showline=False,
        ),
        yaxis=dict(**ax(ticksuffix=" %", title_text="Gain de productivité (%)",
                        range=[-62, 92], zeroline=False)),
        legend=dict(
            orientation="v", x=1.12, y=0.98, xanchor="left", yanchor="top",
            font=dict(color=TEXT, size=10),
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    viz_tag("Graphique en lignes (Line chart)", SAGE)
    st.plotly_chart(fig_pr, width="stretch")
    src(
        "Kalliamvakou 2022 (GitHub Copilot study) · "
        "Peng et al. 2023 (MIT/Princeton) · "
        "Cui et al. 2025 (arXiv:2508.19834)"
    )

with col_pr_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>L\'effet ciseaux</strong>'
        f'<p>Un junior gagne <span class="num sage">+78 %</span> sur la génération de code.<br><br>'
        f'Un expert perd <span class="num coral">−38 %</span> de temps sur la revue '
        f'du même code — il le récrit plutôt que de le corriger.</p>',
        "coral",
    )
    callout(
        f'<strong>Pourquoi cet écart ?</strong>'
        f'<p>L\'expert a des standards élevés et détecte les erreurs subtiles. '
        f'Il passe plus de temps à <strong>valider</strong> qu\'à <strong>produire</strong>. '
        f'L\'IA optimise la quantité, pas la qualité.</p>',
        "blue",
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 07 - TRUST PARADOX ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "07. Le paradoxe de la confiance",
    "Plus on est expérimenté, plus on est méfiant. Et frustré",
    "Les débutants font confiance à l'IA ; les seniors s'en méfient. "
    "Les deux courbes se croisent dès 1–5 ans d'ancienneté. "
    "Globalement, les très méfiants sont 45,7 % contre 32,7 % de très confiants.",
)

col_tr1, col_tr2 = st.columns([3, 2], gap="large")

with col_tr1:
    fig_tr = go.Figure()

    x_lbl = df_trust["label"].tolist()

    fig_tr.add_trace(go.Scatter(
        x=x_lbl, y=df_trust["favorable"],
        mode="lines+markers",
        name="% très confiant",
        line=dict(color=TEAL, width=3, shape="linear"),
        marker=dict(
            size=[10 if s else 7 for s in df_trust["sf"]],
            color=TEAL,
            line=dict(color=CARD, width=2),
            symbol=["circle" if s else "circle-open" for s in df_trust["sf"]],
        ),
        fill="tozeroy", fillcolor=f"rgba(91,191,186,0.08)",
        hovertemplate="<b>%{x}</b><br>Très confiant : <b>%{y} %</b><extra></extra>",
    ))

    fig_tr.add_trace(go.Scatter(
        x=x_lbl, y=df_trust["skeptical"],
        mode="lines+markers",
        name="% très méfiant",
        line=dict(color=AMBER, width=3, shape="linear"),
        marker=dict(
            size=[10 if s else 7 for s in df_trust["ss"]],
            color=AMBER,
            line=dict(color=CARD, width=2),
            symbol=["circle" if s else "circle-open" for s in df_trust["ss"]],
        ),
        fill="tozeroy", fillcolor=f"rgba(232,168,56,0.08)",
        hovertemplate="<b>%{x}</b><br>Très méfiant : <b>%{y} %</b><extra></extra>",
    ))

    # Marqueur visuel au point de croisement exact (1–5 ans, ~9 %)
    fig_tr.add_trace(go.Scatter(
        x=["1–5 ans"], y=[9.0],
        mode="markers",
        marker=dict(size=16, color="rgba(255,255,255,0.12)",
                    line=dict(color=TEXT, width=1.5), symbol="circle"),
        showlegend=False, hoverinfo="skip",
    ))

    # Annotation au-dessus du croisement, flèche courte et nette
    fig_tr.add_annotation(
        x="1–5 ans", y=9.0,
        text="<b>Point de bascule</b><br><span style='font-size:10px'>confiant → méfiant</span>",
        showarrow=True,
        arrowhead=3, arrowcolor=TEXT, arrowsize=0.9, arrowwidth=1.5,
        ax=-55, ay=-45,
        xanchor="center",
        font=dict(color=TEXT, size=11, family="Inter Tight"),
        bgcolor=ALT, bordercolor=BORDER, borderwidth=1, borderpad=6,
        align="center",
    )

    fig_tr.update_layout(
        **layout(height=370, legend=dict(orientation="h", y=1.12, x=0)),
        xaxis=dict(**ax(title_text="Niveau d'ancienneté")),
        yaxis=dict(**ax(ticksuffix=" %", title_text="Part des répondants (%)", range=[0, 26])),
    )

    viz_tag("Graphique linéaire · aires", TEAL)
    st.plotly_chart(fig_tr, width="stretch")
    st.caption(
        "Cercles pleins = valeurs source (Stack Overflow 2025). "
        "Cercles vides = interpolation de tendance décrite dans l'étude."
    )
    src("Stack Overflow Developer Survey 2025. n=33 244 (confiance) · n=31 476 (frustration)")

with col_tr2:
    # Donut
    fig_donut = go.Figure(go.Pie(
        labels=["Très méfiants", "Très confiants", "Nuancés / mitigés"],
        values=[45.7, 32.7, 21.6],
        hole=0.64,
        marker=dict(
            colors=[AMBER, TEAL, MUTED],
            line=dict(color=CARD, width=3),
        ),
        textinfo="label+percent",
        textfont=dict(color=TEXT, size=11.5),
        direction="clockwise", sort=False, rotation=90,
        hovertemplate="<b>%{label}</b><br>%{value} %<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b style='font-size:16px'>33 244</b><br><span style='font-size:10px;color:{MUTED}'>développeurs</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(color=TEXT, size=14),
    )
    fig_donut.update_layout(
        **layout(height=290, margin=dict(t=60, b=10, l=10, r=10),
                 legend=dict(orientation="h", y=-0.05, font=dict(size=11))),
        title=dict(
            text="Distribution globale de la confiance",
            font=dict(size=13, color=MUTED), x=0.5,
        ),
        showlegend=True,
    )
    viz_tag("Donut chart", AMBER)
    st.plotly_chart(fig_donut, width="stretch")

    # Gauge frustration
    fig_gg = go.Figure(go.Indicator(
        mode="gauge+number",
        value=66,
        title=dict(text="Taux de frustration envers l'IA",
                   font=dict(color=TEXT, size=12)),
        number=dict(suffix=" %", font=dict(color=AMBER, size=38, family="JetBrains Mono")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=MUTED,
                      tickfont=dict(color=TEXT, size=10)),
            bar=dict(color=AMBER, thickness=0.25),
            bgcolor=BG,
            bordercolor=BORDER, borderwidth=1,
            steps=[
                dict(range=[0,  33], color="#1A2E24"),
                dict(range=[33, 66], color="#2A2518"),
                dict(range=[66, 100], color="#2E1A1A"),
            ],
            threshold=dict(line=dict(color=CORAL, width=3), thickness=0.8, value=66),
        ),
    ))
    fig_gg.update_layout(
        **layout(height=255, margin=dict(t=50, b=30, l=30, r=30)),
    )
    viz_tag("Jauge (Gauge)", CORAL)
    st.plotly_chart(fig_gg, width="stretch")
    st.caption("66 % des développeurs frustrés par les outputs IA (n=31 476).")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 08 - RADAR SYNTHÈSE ──────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "08. Synthèse · Profil de gouvernance",
    "Cinq angles morts, une même conclusion : la gouvernance IA est à construire",
    "Chaque dimension révèle un déficit structurel. "
    "L'écart entre situation actuelle et cible de bonne gouvernance "
    "est large sur toutes les dimensions. Mais pas irréductible.",
)

col_rd, col_rd_r = st.columns([2, 1], gap="large")

with col_rd:
    dims = [
        "Shadow AI (% non approuvé)",
        "Non-conformité IT (% hors seuil)",
        "Gap productivité (perçu vs mesuré)",
        "Polarisation de la confiance",
        "Blindspot dirigeants",
    ]
    current = [52.0, 71.8, 57.0, 78.4, 38.0]
    target  = [15,   20,   20,   30,   10  ]

    # Tri par écart croissant : le plus critique se retrouve en haut du graphique
    order     = sorted(range(len(dims)), key=lambda i: current[i] - target[i])
    dims_s    = [dims[i]    for i in order]
    current_s = [current[i] for i in order]
    target_s  = [target[i]  for i in order]
    y_pos     = list(range(len(dims_s)))

    # ── Radar / Toile d'araignée ──────────────────────────────────────────
    dims_closed    = dims    + [dims[0]]
    current_closed = current + [current[0]]
    target_closed  = target  + [target[0]]

    fig_rd = go.Figure()

    # Zone remplie — situation actuelle
    fig_rd.add_trace(go.Scatterpolar(
        r=current_closed,
        theta=dims_closed,
        fill="toself",
        fillcolor=f"rgba(160,124,232,0.18)",
        line=dict(color=AMBER, width=2.5),
        name="Situation actuelle",
        hovertemplate="<b>%{theta}</b><br>Score actuel : <b>%{r:.0f} / 100</b><extra></extra>",
    ))

    # Zone remplie — cible de bonne gouvernance
    fig_rd.add_trace(go.Scatterpolar(
        r=target_closed,
        theta=dims_closed,
        fill="toself",
        fillcolor=f"rgba(79,196,190,0.12)",
        line=dict(color=TEAL, width=2, dash="dot"),
        name="Cible de bonne gouvernance",
        hovertemplate="<b>%{theta}</b><br>Cible : <b>%{r:.0f} / 100</b><extra></extra>",
    ))

    fig_rd.update_layout(
        **layout(height=480, margin=dict(t=60, b=60, l=60, r=60),
                 legend=dict(orientation="h", y=-0.12, x=0.2, font=dict(size=12))),
        polar=dict(
            bgcolor=CARD,
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100],
                tickfont=dict(color=LIGHT, size=9),
                gridcolor=BORDER,
                linecolor=BORDER,
                angle=90,
            ),
            angularaxis=dict(
                tickfont=dict(color=TEXT, size=11.5),
                linecolor=BORDER,
                gridcolor=BORDER,
            ),
        ),
    )

    viz_tag("Radar · toile d'araignée", BLUE)
    st.plotly_chart(fig_rd, width="stretch")
    st.caption(
        "Score de préoccupation normalisé (0 = pas de risque, 100 = situation critique). "
        "Gap productivité estimé à partir de l'écart +98 % perçu vs −19 % mesuré."
    )

with col_rd_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Lecture du graphique</strong>'
        f'<p>• Shadow AI : <span class="num amber">52 / 100</span><br>'
        f'• Non-conformité IT : <span class="num amber">72 / 100</span><br>'
        f'• Gap productivité : <span class="num amber">57 / 100</span><br>'
        f'• Polarisation confiance : <span class="num coral">78 / 100</span><br>'
        f'• Blindspot dirigeants : <span class="num amber">38 / 100</span></p>',
    )
    callout(
        f'<strong>3 leviers prioritaires</strong>'
        f'<p><b>① Légitimer</b> les usages courants (search, doc) pour réduire le shadow sans l\'interdire.<br><br>'
        f'<b>② Former</b> sur les tâches à fort enjeu (sécurité, déploiement, données sensibles).<br><br>'
        f'<b>③ Mesurer</b> la productivité par télémétrie, pas par ressenti individuel.</p>',
        "sage",
    )

# ══════════════════════════════════════════════════════════════════════════════
# ─── 09 - SANKEY FLUX ─────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "09. Anatomie du risque",
    "De l'usage à l'incident : 49 ingénieurs sur 100 empruntent la mauvaise voie",
    "Sur 100 ingénieurs qui utilisent l'IA, 49 le font sans validation de leur employeur. "
    "Parmi eux, 28 sont directement liés à un incident IT détecté. "
    "Ce flux rend visible la chaîne shadow AI → exposition → incident, "
    "rarement représentée en un seul graphique.",
)

col_sk, col_sk_r = st.columns([3, 1], gap="large")

with col_sk:
    fig_sk = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=22,
            line=dict(color=BORDER, width=0.8),
            # ordre : sources d'abord, sinks ensuite — "N'utilisent pas" en dernier
            # pour que snap le place en bas sans croiser "Utilisent l'IA"
            label=[
                "100 ingénieurs",   # 0
                "Utilisent l'IA",   # 1
                "Usage approuvé",   # 2
                "Shadow AI",        # 3
                "Sans incident",    # 4
                "Incidents IT",     # 5
                "N'utilisent pas",  # 6  ← sink en dernier = placé en bas
            ],
            color=[BLUE, TEAL, SAGE, AMBER, SAGE, CORAL, MUTED],
            customdata=["100 %", "84 %", "35 %", "49 %", "56 %", "28 %", "16 %"],
            hovertemplate="<b>%{label}</b> · %{customdata}<extra></extra>",
        ),
        link=dict(
            # flux réordonnés selon les nouveaux indices
            source=[0, 0, 1, 1, 2, 2, 3, 3],
            target=[1, 6, 2, 3, 5, 4, 5, 4],
            value= [84, 16, 35, 49, 5, 30, 28, 21],
            color=[
                "rgba(79,196,190,0.20)",
                "rgba(139,148,158,0.15)",
                "rgba(104,181,120,0.25)",
                "rgba(160,124,232,0.25)",
                "rgba(224,88,88,0.20)",
                "rgba(104,181,120,0.20)",
                "rgba(224,88,88,0.38)",
                "rgba(104,181,120,0.15)",
            ],
            hovertemplate=(
                "<b>%{source.label}</b> → <b>%{target.label}</b>"
                "<br>%{value} ingénieurs sur 100"
                "<extra></extra>"
            ),
        ),
    ))

    fig_sk.update_layout(
        **layout(height=460, margin=dict(t=20, b=20, l=10, r=10)),
    )

    viz_tag("Diagramme de Sankey", CORAL)
    st.plotly_chart(fig_sk, width="stretch")
    src("Stack Overflow Dev Survey 2025 · Okta / Apprize360 2026 · BlackFog Survey")

with col_sk_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Le flux critique</strong>'
        f'<p>Sur <span class="num">84</span> ingénieurs utilisant l\'IA, '
        f'<span class="num amber">49</span> opèrent en shadow AI.<br><br>'
        f'De ces 49, <span class="num coral">28</span> sont associés à un incident IT '
        f'soit plus d\'un sur deux.</p>',
        "coral",
    )
    callout(
        f'<strong>Les 5 incidents « approuvés »</strong>'
        f'<p>Même les usages officiellement validés génèrent des incidents. '
        f'La validation seule ne suffit pas : '
        f'formation et périmètres d\'usage restent indispensables.</p>',
        "blue",
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 10 - HEATMAP ZONES DE RISQUE ─────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "10. Cartographie des zones de risque",
    "Recherche sur données internes : la combinaison la plus exposée",
    "Croiser le type de tâche avec la sensibilité des données révèle où le shadow AI "
    "est le plus dangereux. La tâche la plus banale n'est pas la moins risquée.",
)

col_hm, col_hm_r = st.columns([3, 1], gap="large")

with col_hm:
    tasks_hm = ["Recherche / Q&A", "Génération de code", "Documentation",
                "Planification", "Déploiement"]
    sensitivity = ["Données critiques", "Données confidentielles",
                   "Données internes", "Données publiques"]

    z_hm = [
        [18, 22, 15, 12,  5],
        [35, 42, 28, 25, 10],
        [52, 58, 44, 40, 16],
        [68, 64, 50, 36, 22],
    ]

    fig_hm = go.Figure(go.Heatmap(
        z=z_hm,
        x=tasks_hm,
        y=sensitivity,
        colorscale=[
            [0.00, "#0D1117"],
            [0.20, "#1C1A2E"],
            [0.45, "#2E1A2E"],
            [0.65, "#6B2A3A"],
            [0.85, CORAL],
            [1.00, "#FF8888"],
        ],
        zmin=0, zmax=72,
        text=[[f"{v} %" for v in row] for row in z_hm],
        texttemplate="%{text}",
        textfont=dict(size=13, family="JetBrains Mono", color=TEXT),
        hovertemplate=(
            "<b>%{y}</b><br>%{x}<br>"
            "Shadow AI estimé : <b>%{z} %</b><extra></extra>"
        ),
        showscale=True,
        colorbar=dict(
            title=dict(text="Shadow AI %", font=dict(color=MUTED, size=10)),
            tickfont=dict(color=MUTED, size=10),
            ticksuffix=" %",
            thickness=12, len=0.65,
            bgcolor="rgba(0,0,0,0)",
            bordercolor=BORDER, borderwidth=1,
        ),
    ))

    fig_hm.update_layout(
        **layout(height=340, margin=dict(t=20, b=20, l=175, r=20)),
        xaxis=dict(**ax(tickfont=dict(size=11, color=TEXT), showgrid=False,
                        showline=False)),
        yaxis=dict(**ax(tickfont=dict(size=11, color=TEXT), showgrid=False,
                        showline=False)),
    )

    viz_tag("Carte de chaleur (Heatmap)", CORAL)
    st.plotly_chart(fig_hm, width="stretch")
    src("Estimation croisée · Stack Overflow Dev Survey 2025 · BlackFog Survey")

with col_hm_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Zone rouge : 68 %</strong>'
        f'<p>Recherche / Q&A sur <b>données publiques</b> : '
        f'<span class="num coral">68 %</span> de shadow AI. '
        f'La tâche la plus banalisée reste la plus exposée en volume.</p>',
        "coral",
    )
    callout(
        f'<strong>Auto-régulation confirmée</strong>'
        f'<p>Déploiement sur données critiques : '
        f'<span class="num teal">5 %</span>. '
        f'Les ingénieurs perçoivent le risque sur les tâches critiques '
        f'pas sur les tâches quotidiennes.</p>',
        "teal",
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 11 - FUNNEL GOUVERNANCE ──────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "11. L'entonnoir de la gouvernance IA",
    "Sur 100 entreprises, 6 seulement ont un plan de réponse aux incidents",
    "Chaque étape de maturité filtre davantage d'organisations. "
    "La politique IA existe souvent sur le papier l'application et la détection, "
    "beaucoup moins. La chute entre politique écrite et contrôles actifs est la plus brutale.",
)

col_fn, col_fn_r = st.columns([3, 1], gap="large")

with col_fn:
    funnel_labels = [
        "Entreprises utilisant l'IA",
        "Avec une politique IA formelle",
        "Formant leurs employés à l'IA",
        "Avec des contrôles de conformité",
        "Avec monitoring shadow AI actif",
        "Avec plan de réponse aux incidents",
    ]
    funnel_values = [100, 68, 45, 29, 14, 6]
    funnel_colors = [TEAL, BLUE, BLUE, AMBER, CORAL, CORAL]

    fig_fn = go.Figure(go.Funnel(
        y=funnel_labels,
        x=funnel_values,
        textinfo="value+percent initial",
        textfont=dict(family="JetBrains Mono", size=13, color=TEXT),
        marker=dict(
            color=funnel_colors,
            line=dict(color=CARD, width=2),
        ),
        connector=dict(line=dict(color=BORDER, width=1.5, dash="dot")),
        hovertemplate="<b>%{y}</b><br>%{x} entreprises sur 100<extra></extra>",
    ))

    fig_fn.update_layout(
        **layout(height=460, margin=dict(t=20, b=20, l=20, r=20)),
    )

    viz_tag("Diagramme en entonnoir (Funnel)", AMBER)
    st.plotly_chart(fig_fn, width="stretch")
    src("Okta / Apprize360 2026 · BlackFog Survey · estimation secteur")

with col_fn_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>La chute la plus brutale</strong>'
        f'<p><span class="num teal">68 %</span> ont une politique écrite.<br>'
        f'Seulement <span class="num amber">29 %</span> ont des contrôles actifs.<br><br>'
        f'Politique sans enforcement = fausse sécurité.</p>',
        "amber",
    )
    callout(
        f'<strong>6 sur 100</strong>'
        f'<p>Seules <span class="num coral">6 entreprises sur 100</span> '
        f'ont un vrai plan de réponse aux incidents IA. '
        f'Les 94 autres découvrent le problème après coup.</p>',
        "coral",
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ─── 12 - ÉVOLUTION TEMPORELLE ────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

section_header(
    "12. L'écart se creuse depuis 2022",
    "ChatGPT déclenche le décrochage l'usage shadow triple en 3 ans",
    "L'usage approuvé progresse. Mais le shadow AI part d'un niveau plus élevé "
    "et maintient son avance. Le fossé en points absolus a triplé depuis le lancement "
    "de ChatGPT en novembre 2022.",
)

col_tl, col_tl_r = st.columns([3, 1], gap="large")

with col_tl:
    years_tl   = [2022, 2023, 2024, 2025]
    approved_tl = [8, 18, 32, 38]
    shadow_tl   = [12, 28, 44, 52]

    fig_tl = go.Figure()

    # Zone shadow (derrière)
    fig_tl.add_trace(go.Scatter(
        x=years_tl, y=shadow_tl,
        fill="tozeroy",
        fillcolor="rgba(160,124,232,0.18)",
        line=dict(color=AMBER, width=3),
        mode="lines+markers",
        name="Shadow AI",
        marker=dict(size=11, color=AMBER, line=dict(color=CARD, width=2.5)),
        hovertemplate="<b>%{x}</b><br>Shadow AI : <b>%{y} %</b><extra></extra>",
    ))

    # Zone approuvée (devant)
    fig_tl.add_trace(go.Scatter(
        x=years_tl, y=approved_tl,
        fill="tozeroy",
        fillcolor="rgba(79,196,190,0.22)",
        line=dict(color=TEAL, width=3),
        mode="lines+markers",
        name="Usage approuvé",
        marker=dict(size=11, color=TEAL, line=dict(color=CARD, width=2.5)),
        hovertemplate="<b>%{x}</b><br>Usage approuvé : <b>%{y} %</b><extra></extra>",
    ))

    # Annotation ChatGPT launch
    fig_tl.add_vline(
        x=2022.92,
        line=dict(color=MUTED, width=1.5, dash="dot"),
        annotation_text="ChatGPT · nov. 2022",
        annotation_position="top right",
        annotation_font=dict(color=MUTED, size=10),
    )

    # Écart final 2025
    fig_tl.add_annotation(
        x=2025, y=(52 + 38) / 2, xshift=12,
        text=f"<b>Écart<br>14 pts</b>",
        showarrow=True, arrowhead=2, ax=-50, ay=0,
        arrowcolor=CORAL, arrowwidth=1.5,
        font=dict(color=CORAL, size=11, family="JetBrains Mono"),
        bgcolor=CARD, bordercolor=CORAL, borderpad=5, borderwidth=1,
        xanchor="left",
    )

    # Labels finaux
    fig_tl.add_annotation(
        x=2025, y=52, yshift=14, xshift=6,
        text="<b>52 %</b>", showarrow=False, xanchor="left",
        font=dict(color=AMBER, size=13, family="JetBrains Mono"),
    )
    fig_tl.add_annotation(
        x=2025, y=38, yshift=-16, xshift=6,
        text="<b>38 %</b>", showarrow=False, xanchor="left",
        font=dict(color=TEAL, size=13, family="JetBrains Mono"),
    )

    fig_tl.update_layout(
        **layout(height=420,
                 legend=dict(orientation="h", y=1.12, x=0, font=dict(size=12))),
        xaxis=dict(**ax(
            tickvals=years_tl, ticktext=[str(y) for y in years_tl],
            title_text="Année", tickfont=dict(size=13, color=TEXT),
        )),
        yaxis=dict(**ax(ticksuffix=" %", title_text="Taux d'usage IA (%)",
                        range=[0, 62])),
    )

    viz_tag("Graphique d'aires empilées", TEAL)
    st.plotly_chart(fig_tl, width="stretch")
    src("Estimation longitudinale · Stack Overflow Dev Survey 2022–2025 · Okta 2026")

with col_tl_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>L\'écart triple en 3 ans</strong>'
        f'<p>2022 : gap <span class="num">4 pts</span><br>'
        f'2023 : gap <span class="num amber">10 pts</span><br>'
        f'2025 : gap <span class="num coral">14 pts</span><br><br>'
        f'Le shadow AI accélère plus vite que la gouvernance.</p>',
        "amber",
    )
    callout(
        f'<strong>Usage approuvé ×4,75</strong>'
        f'<p>L\'adoption approuvée a progressé de 8 % à 38 % '
        f'une vraie croissance. Mais insuffisante pour combler '
        f'le décrochage shadow.</p>',
        "teal",
    )

st.markdown("---")

# ─── FOOTER ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(f"""
<div style="padding:1rem 0 2rem;color:{LIGHT};font-size:0.78rem;line-height:2;">
  <strong style="color:{MUTED};">Sources complètes</strong><br>
  Okta / Apprize360. <em>AI Agents at Work 2026</em> (via The Register). n=784<br>
  BlackFog Survey (via CIO.com). n=2 000<br>
  Stack Overflow Developer Survey 2025. n=49 000+, 177 pays, licence ODbL<br>
  Faros AI, données télémétrie (via P. Dubach). n=10 000+ développeurs<br>
  Cui et al. 2025 (Microsoft / Accenture). arXiv:2508.19834. RCT, n≈5 000<br><br>
  Dataviz réalisée dans le cadre du cours <strong style="color:{MUTED};">Dataviz</strong>. Ynov Campus · Juillet 2026
</div>
""", unsafe_allow_html=True)
