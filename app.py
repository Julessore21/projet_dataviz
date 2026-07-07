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
   .section-num   : 0.68rem  étiquette de section
   .section-claim : 2.0rem   titre principal (affirmation)
   .section-deck  : 1.05rem  sous-titre / chapeau narratif
   body p         : 0.96rem  texte courant
   ────────────────────────────────────────────── */
.section-num {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: {LIGHT};
  display: block;
  margin-bottom: 0.15rem;
}}
.section-claim {{
  font-family: 'Inter Tight', sans-serif;
  font-size: 2.0rem;
  font-weight: 800 !important;
  color: {TEXT} !important;
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin: 0.15rem 0 0.65rem;
}}
.section-deck {{
  font-size: 1.05rem;
  font-weight: 400 !important;
  color: {MUTED} !important;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  max-width: 640px;
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
    {"label": "Rechercher des réponses",  "usage": 54.1, "stakes": "Faible"},
    {"label": "Planification de projet",  "usage": 30.8, "stakes": "Élevé"},
    {"label": "Déploiement / monitoring", "usage": 24.2, "stakes": "Élevé"},
])

df_trust = pd.DataFrame([
    {"label": "Débutants", "favorable": 6.1,  "skeptical":  5.2, "sf": True,  "ss": False},
    {"label": "1–5 ans",   "favorable": 4.2,  "skeptical": 12.0, "sf": False, "ss": False},
    {"label": "5–10 ans",  "favorable": 3.1,  "skeptical": 19.6, "sf": True,  "ss": True },
    {"label": "10+ ans",   "favorable": 2.5,  "skeptical": 20.7, "sf": False, "ss": True },
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

def section_header(num, claim, deck):
    st.markdown(
        f'<span class="section-num">{num}</span>'
        f'<p class="section-claim">{claim}</p>'
        f'<p class="section-deck">{deck}</p>',
        unsafe_allow_html=True,
    )

def callout(body, variant="amber"):
    st.markdown(f'<div class="callout {variant}">{body}</div>', unsafe_allow_html=True)

def src(text):
    st.markdown(f'<span class="src">↗ {text}</span>', unsafe_allow_html=True)


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

    # Barres divergentes ancrées sur le seuil IT (le seuil = "zéro")
    fig_dump.add_trace(go.Bar(
        x=deltas, y=y_pos,
        base=IT_THRESHOLD,
        orientation="h",
        marker=dict(color=bar_cols, opacity=0.85, line=dict(color="rgba(0,0,0,0)")),
        width=0.55,
        customdata=list(zip(labels, usages, stakes, [f"{d:+.1f}" for d in deltas])),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Usage : <b>%{customdata[1]} %</b> (%{customdata[3]} pts vs seuil)<br>"
            "Enjeu : %{customdata[2]}<extra></extra>"
        ),
        showlegend=False,
    ))

    # Valeur d'usage au bout de chaque barre
    for yi, u, d in zip(y_pos, usages, deltas):
        fig_dump.add_annotation(
            x=u, y=yi, xshift=14 if d > 0 else -14,
            text=f"<b>{u} %</b>", showarrow=False,
            xanchor="left" if d > 0 else "right",
            font=dict(color=TEXT, size=12.5, family="JetBrains Mono"),
        )

    # Ligne de seuil = origine des barres
    fig_dump.add_shape(
        type="line", x0=IT_THRESHOLD, x1=IT_THRESHOLD,
        y0=-0.5, y1=n_t - 0.5,
        line=dict(color=TEAL, width=2, dash="dot"),
    )
    fig_dump.add_annotation(
        x=IT_THRESHOLD, y=n_t - 0.35,
        text=f"Seuil IT : {IT_THRESHOLD} %",
        showarrow=False,
        font=dict(color=TEAL, size=11),
        bgcolor=CARD, bordercolor=TEAL, borderwidth=1, borderpad=4,
    )

    for yi, u, s in zip(y_pos, usages, stakes):
        badge_col = AMBER if s == "Faible" else CORAL
        fig_dump.add_annotation(
            x=max(u, IT_THRESHOLD), y=yi, yshift=-17, xshift=14,
            text=f"enjeu {s.lower()}",
            showarrow=False, xanchor="left",
            font=dict(color=badge_col, size=10),
        )

    fig_dump.update_layout(
        **layout(height=360, margin=dict(t=55, b=55, l=210, r=60)),
        xaxis=dict(**ax(range=[0, 68], ticksuffix=" %",
                        title_text="Taux d'utilisation pour cette tâche (%)")),
        yaxis=dict(tickvals=y_pos, ticktext=labels,
                   **ax(tickfont=dict(size=12.5, color=TEXT))),
    )

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
    "+98 % de PR perçues, −19 % de vélocité mesurée",
    "Les développeurs se sentent plus productifs. La télémétrie dit le contraire. "
    "Ce décalage entre ressenti individuel et mesure collective est l'une des tensions "
    "les plus documentées de l'adoption de l'IA en entreprise.",
)

col_pr, col_pr_r = st.columns([3, 1], gap="large")

with col_pr:
    # Ordre explicite : groupe MESURÉ en bas, groupe PERÇU en haut
    order = ["Temps de revue code", "Vélocité équipe", "Score DORA",
             "Tâches complétées", "PR soumises"]
    df_p = df_productivity.set_index("metric").loc[order].reset_index()

    bar_colors = []
    for _, r in df_p.iterrows():
        if r["dir"] == "+":   bar_colors.append(SAGE)
        elif r["dir"] == "-": bar_colors.append(CORAL)
        else:                 bar_colors.append(MUTED)

    fig_pr = go.Figure()

    # Ligne zéro
    fig_pr.add_vline(x=0, line=dict(color=BORDER, width=1.5))

    # Séparation PERÇU / MESURÉ — bande de fond
    fig_pr.add_hrect(
        y0=2.5, y1=4.6,
        fillcolor=f"rgba(104,181,120,0.05)", line_width=0,
    )
    fig_pr.add_hrect(
        y0=-0.5, y1=2.5,
        fillcolor=f"rgba(224,88,88,0.05)", line_width=0,
    )

    # Tiges depuis 0
    for yi, v, c in zip(range(len(df_p)), df_p["value"], bar_colors):
        fig_pr.add_shape(
            type="line", x0=0, x1=v, y0=yi, y1=yi,
            line=dict(color=c, width=3, dash="solid"),
        )

    # Dots
    fig_pr.add_trace(go.Scatter(
        x=df_p["value"], y=list(range(len(df_p))),
        mode="markers+text",
        marker=dict(color=bar_colors, size=18,
                    line=dict(color=CARD, width=2.5)),
        text=[f"<b>{'+' if v > 0 else ''}{v} %</b>" for v in df_p["value"]],
        textposition=["middle right" if v >= 0 else "middle left" for v in df_p["value"]],
        textfont=dict(color=TEXT, size=12, family="JetBrains Mono"),
        customdata=df_p[["src"]].values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Variation : <b>%{x} %</b><extra></extra>"
        ),
        showlegend=False,
    ))

    # Étiquettes de groupe
    fig_pr.add_annotation(
        x=125, y=3.7, text="PERÇU", showarrow=False, xanchor="right",
        font=dict(color=SAGE, size=10, family="JetBrains Mono"),
    )
    fig_pr.add_annotation(
        x=125, y=3.3, text="déclaratif par les devs", showarrow=False, xanchor="right",
        font=dict(color=MUTED, size=9),
    )
    fig_pr.add_annotation(
        x=125, y=1.7, text="MESURÉ", showarrow=False, xanchor="right",
        font=dict(color=CORAL, size=10, family="JetBrains Mono"),
    )
    fig_pr.add_annotation(
        x=125, y=1.3, text="télémétrie & RCT", showarrow=False, xanchor="right",
        font=dict(color=MUTED, size=9),
    )

    # Séparateur horizontal
    fig_pr.add_hline(y=2.5, line=dict(color=BORDER, width=1, dash="dot"))

    fig_pr.update_layout(
        **layout(height=420),
        xaxis=dict(**ax(range=[-120, 140], ticksuffix=" %", title_text="Variation (%)",
                        zeroline=True, zerolinecolor=BORDER, zerolinewidth=1.5)),
        yaxis=dict(tickvals=list(range(len(df_p))), ticktext=df_p["metric"].tolist(),
                   **ax(tickfont=dict(size=12.5, color=TEXT))),
    )

    st.plotly_chart(fig_pr, width="stretch")
    src(
        "Faros AI. n=10 000+ développeurs, 1 255 équipes · "
        "Cui et al. 2025 (arXiv:2508.19834). RCT, n≈5 000"
    )

with col_pr_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Divergence critique</strong>'
        f'<p>Les devs perçoivent <span class="num sage">+98 %</span> de PR soumises.<br><br>'
        f'La télémétrie mesure <span class="num coral">−19 %</span> de vélocité réelle '
        f'et <span class="num coral">+91 %</span> de temps de revue de code.</p>',
        "coral",
    )
    callout(
        f'<strong>Contrepoint important</strong>'
        f'<p>Cui et al. (Microsoft / Accenture, RCT, n≈5 000) '
        f'montre des gains positifs mesurés avec GitHub Copilot. '
        f'Le résultat dépend du <strong>contexte</strong> et de la <strong>maturité d\'usage</strong>.</p>',
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

    fig_tr.add_annotation(
        x="1–5 ans", y=9,
        text="Point de bascule",
        showarrow=True, arrowhead=2,
        arrowcolor=MUTED, arrowsize=1, arrowwidth=1.5,
        ax=65, ay=-40,
        font=dict(color=TEXT, size=11),
        bgcolor=CARD, bordercolor=BORDER, borderwidth=1, borderpad=4,
    )

    fig_tr.update_layout(
        **layout(height=370, legend=dict(orientation="h", y=1.12, x=0)),
        xaxis=dict(**ax(title_text="Niveau d'ancienneté")),
        yaxis=dict(**ax(ticksuffix=" %", title_text="Part des répondants (%)", range=[0, 26])),
    )

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
            pad=24,
            thickness=24,
            line=dict(color=BORDER, width=0.8),
            label=[
                "100 ingénieurs",
                "Utilisent l'IA",
                "N'utilisent pas",
                "Usage approuvé",
                "Shadow AI",
                "Incidents IT",
                "Sans incident",
            ],
            color=[BLUE, TEAL, MUTED, SAGE, AMBER, CORAL, SAGE],
            customdata=["100 %", "84 %", "16 %", "35 %", "49 %", "28 %", "56 %"],
            hovertemplate="<b>%{label}</b> · %{customdata}<extra></extra>",
        ),
        link=dict(
            source=[0, 0, 1, 1, 3, 3, 4, 4],
            target=[1, 2, 3, 4, 5, 6, 5, 6],
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

    st.plotly_chart(fig_sk, width="stretch")
    src("Stack Overflow Dev Survey 2025 · Okta / Apprize360 2026 · BlackFog Survey")

with col_sk_r:
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    callout(
        f'<strong>Le flux critique</strong>'
        f'<p>Sur <span class="num">84</span> ingénieurs utilisant l\'IA, '
        f'<span class="num amber">49</span> opèrent en shadow AI.<br><br>'
        f'De ces 49, <span class="num coral">28</span> sont associés à un incident IT — '
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
