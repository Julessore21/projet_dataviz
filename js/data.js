'use strict';

/* ── Sources ─────────────────────────────────────────────────────────── */
const SOURCES = {
  okta: {
    name: 'Okta / Apprize360, "AI Agents at Work 2026" (via The Register)',
    url:  'https://www.theregister.com/ai-ml/2026/05/27/bosses-blinded-by-confidence-about-shadow-ai-use-by-workers/5247275',
    n:    'n=292 dirigeants + 492 knowledge workers, 7 pays'
  },
  blackfog: {
    name: 'BlackFog survey (via CIO.com)',
    url:  'https://www.cio.com/article/4124760/roughly-half-of-employees-are-using-unsanctioned-ai-tools-and-enterprise-leaders-are-major-culprits.html',
    n:    'n=2 000 salariés, entreprises 500+ employés'
  },
  stackoverflow: {
    name: 'Stack Overflow Developer Survey 2025',
    url:  'https://survey.stackoverflow.co/2025/ai/',
    n:    'n=49 000+, 177 pays, licence ODbL'
  },
  faros: {
    name: 'Faros AI, données télémétrie (via P. Dubach)',
    url:  'https://philippdubach.com/posts/93-of-developers-use-ai-coding-tools.-productivity-hasnt-moved./',
    n:    'n=10 000+ développeurs, 1 255 équipes'
  },
  faros2: {
    name: 'Faros AI, synthèse complémentaire (Software Seni)',
    url:  'https://www.softwareseni.com/what-the-research-actually-shows-about-ai-coding-assistant-productivity/',
    n:    'synthèse'
  },
  cui: {
    name: 'Cui et al. 2025 (Microsoft / Accenture), via arXiv',
    url:  'https://arxiv.org/pdf/2508.19834',
    n:    'RCT, n≈5 000 développeurs, 2–8 mois'
  }
};

/* ── Section data ─────────────────────────────────────────────────────── */
const DATA = {

  /* S1 — Hero */
  hero: {
    leaderConfident: 90,
    shadowUsage:     52,
    incidents:       58,
    source: SOURCES.okta
  },

  /* S2 — Ampleur monde (pays triés par taux décroissant) */
  world: {
    countries: [
      { name: 'États-Unis',  iso: 'US', rate: 67, lon: -98.6, lat:  39.5 },
      { name: 'Australie',   iso: 'AU', rate: 60, lon: 133.8, lat: -25.3 },
      { name: 'Royaume-Uni', iso: 'GB', rate: 55, lon:  -3.4, lat:  55.4 },
      { name: 'Canada',      iso: 'CA', rate: 50, lon: -96.8, lat:  60.0 },
      { name: 'France',      iso: 'FR', rate: 30, lon:   2.3, lat:  46.2 },
      { name: 'Allemagne',   iso: 'DE', rate: 30, lon:  10.5, lat:  51.2 }
    ],
    ukNote: 'Écart confiance/réalité le plus large : 96 % des dirigeants BR confiants vs +50 % des salariés utilisant des outils non approuvés.',
    blackfogStats: '49 % sans validation employeur · 69 % des PDG/CODIR tolèrent la pratique · 86 % utilisent l\'IA chaque semaine au travail.',
    source:           SOURCES.okta,
    sourceComplement: SOURCES.blackfog
  },

  /* S3 — Ampleur ingénieurs */
  engineers: {
    headline:  84,
    daily:     51,
    favorable: 60,
    bySeniority: [
      { label: 'Early Career (1–5 ans)', daily: 55.5 },
      { label: 'Mid Career (5–10 ans)',  daily: 52.8 },
      { label: 'Experienced (10+ ans)',  daily: 47.3 }
    ],
    source: SOURCES.stackoverflow
  },

  /* S4 — Écart officiel / réel  */
  gap: {
    itRulesStrict: 28.2,   // % devs avec règles IT strictes anti-IA agentique
    tasks: [
      // usage = % utilisant majoritairement l'IA pour cette tâche
      // Pour enjeu élevé : calculé sur base déclarations de refus (100 − refus)
      { label: 'Rechercher des réponses',  stakes: 'low',  usage: 54.1 },
      { label: 'Planification de projet',  stakes: 'high', usage: 30.8 },
      { label: 'Déploiement / monitoring', stakes: 'high', usage: 24.2 }
    ],
    note: 'Règles IT strictes anti-IA agentique : 28,2 % (13,8 % tout à fait d\'accord + 14,4 % plutôt d\'accord).',
    source: SOURCES.stackoverflow,
    n: 'n=28 930'
  },

  /* S5 — Mythe productivité */
  productivity: {
    diffLines: [
      { type: 'ctx', code: '  // Déclaratif — ressenti développeur'                  },
      { type: 'del', code: '- tasks_completed  += 21%',  comment: '// +21 % de tâches traitées (perçu)'  },
      { type: 'del', code: '- pull_requests    += 98%',  comment: '// ×2 pull requests soumises (perçu)' },
      { type: 'ctx', code: ''                                                          },
      { type: 'ctx', code: '  // Télémétrie — Faros AI, n=10 000+ développeurs'      },
      { type: 'add', code: '+ review_time      += 91%',  comment: '// temps de revue de code doublé'      },
      { type: 'add', code: '+ velocity         -= 19%',  comment: '// 19 % plus lent (mesuré)'            },
      { type: 'add', code: '+ dora_score        = stable', comment: '// livraison globale : inchangée'   },
      { type: 'add', code: '+ // Gains perçus mais non confirmés au niveau collectif', comment: ''        }
    ],
    cuiNote: 'Contrepoint : étude Cui et al. (Microsoft / Accenture, RCT, n≈5 000) montre des gains de productivité et de qualité mesurés positivement avec GitHub Copilot — résultats dépendants du contexte et de la maturité d\'usage.',
    source:           SOURCES.faros,
    sourceComplement: SOURCES.cui
  },

  /* S6 — Paradoxe confiance
     Points SOURCE marqués srcFav / srcSkep.
     Points intermédiaires = extrapolation de la tendance décrite dans l'étude :
     "Plus l'ancienneté augmente, plus la méfiance forte augmente."
  */
  trust: {
    overallFav:  32.7,   // 3.1 + 29.6
    overallSkep: 45.7,   // 26.1 + 19.6
    overallN:    33244,
    frustration: { rate: 66, n: 31476 },
    bySeniority: [
      { label: 'Débutants',   favorable: 6.1, skeptical:  5.2, srcFav: true,  srcSkep: false },
      { label: '1–5 ans',     favorable: 4.2, skeptical: 12.0, srcFav: false, srcSkep: false },
      { label: '5–10 ans',    favorable: 3.1, skeptical: 19.6, srcFav: true,  srcSkep: true  },
      { label: '10+ ans',     favorable: 2.5, skeptical: 20.7, srcFav: false, srcSkep: true  }
    ],
    source: SOURCES.stackoverflow,
    n: 'n=33 244 (confiance) · n=31 476 (frustration)'
  }
};
