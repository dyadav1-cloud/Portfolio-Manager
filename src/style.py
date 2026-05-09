import streamlit as st


def apply_custom_style():
    st.markdown(
        """
        <style>

        /* ═══════════════════════════════════════════════════════════
           PORTFOLIO MANAGER — CUSTOM THEME
           Dual-mode: light by default, dark via prefers-color-scheme.
           Accent: Indigo  |  Type scale: tight letter-spacing
        ═══════════════════════════════════════════════════════════ */

        /* ── DESIGN TOKENS ──────────────────────────────────────── */
        :root {
            --c-accent:      #4f46e5;
            --c-accent-soft: #ede9fe;
            --c-bg:          #f8fafc;
            --c-card:        #ffffff;
            --c-sidebar:     #f1f5f9;
            --c-border:      #e2e8f0;
            --c-text-hi:     #0f172a;
            --c-text-lo:     #64748b;
            --c-text-hint:   #94a3b8;
            --shadow-card:   0 1px 3px rgba(15,23,42,.07),
                             0 4px 16px rgba(15,23,42,.04);
            --shadow-lift:   0 4px 12px rgba(79,70,229,.14),
                             0 8px 24px rgba(15,23,42,.07);
            --r-md: 12px;
            --r-lg: 16px;
            --r-xl: 20px;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --c-accent:      #818cf8;
                --c-accent-soft: rgba(99,102,241,.14);
                --c-bg:          #070c16;
                --c-card:        rgba(14,21,38,.92);
                --c-sidebar:     #0b1120;
                --c-border:      rgba(99,102,241,.13);
                --c-text-hi:     #f1f5f9;
                --c-text-lo:     #94a3b8;
                --c-text-hint:   #475569;
                --shadow-card:   0 4px 24px rgba(0,0,0,.28),
                                 0 0 0 1px rgba(99,102,241,.06);
                --shadow-lift:   0 8px 32px rgba(99,102,241,.18),
                                 0 0 0 1px rgba(99,102,241,.14);
            }
        }

        /* ── BASE ───────────────────────────────────────────────── */
        .stApp {
            background-color: var(--c-bg);
        }

        @media (prefers-color-scheme: dark) {
            .stApp {
                background: linear-gradient(
                    155deg,
                    #070c16 0%,
                    #0c1424 55%,
                    #060a10 100%
                );
            }
        }

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
        }

        /* ── TYPOGRAPHY ─────────────────────────────────────────── */
        h1 {
            font-size: 2rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em;
            color: var(--c-text-hi) !important;
            line-height: 1.15;
        }

        h2 {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em;
            color: var(--c-text-hi) !important;
        }

        h3 {
            font-size: 1rem !important;
            font-weight: 600 !important;
            letter-spacing: -0.015em;
            color: var(--c-text-hi) !important;
        }

        p, .stMarkdown p {
            color: var(--c-text-lo);
            line-height: 1.65;
        }

        /* ── SIDEBAR ────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: var(--c-sidebar);
            border-right: 1px solid var(--c-border);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.015em;
            color: var(--c-text-hi) !important;
        }

        /* ── METRIC CARDS ───────────────────────────────────────── */
        [data-testid="stMetric"] {
            background-color: var(--c-card);
            border: 1px solid var(--c-border);
            border-radius: var(--r-xl);
            padding: 1.25rem 1.5rem;
            box-shadow: var(--shadow-card);
            transition:
                box-shadow   0.2s ease,
                border-color 0.2s ease,
                transform    0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            box-shadow: var(--shadow-lift);
            border-color: var(--c-accent);
            transform: translateY(-2px);
        }

        [data-testid="stMetricLabel"] > div {
            font-size: 0.7rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--c-text-lo) !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: 1.6rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em;
            color: var(--c-text-hi) !important;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }

        /* ── DATAFRAMES ─────────────────────────────────────────── */
        div[data-testid="stDataFrame"] {
            border-radius: var(--r-lg);
            overflow: hidden;
            border: 1px solid var(--c-border);
            box-shadow: var(--shadow-card);
        }

        /* ── BUTTONS ────────────────────────────────────────────── */
        .stButton > button {
            border-radius: var(--r-md);
            border: 1.5px solid var(--c-border);
            background-color: var(--c-card);
            color: var(--c-text-hi);
            font-weight: 600;
            font-size: 0.875rem;
            padding: 0.55rem 1.25rem;
            box-shadow: var(--shadow-card);
            transition: all 0.18s ease;
            cursor: pointer;
        }

        .stButton > button:hover {
            border-color: var(--c-accent);
            background-color: var(--c-accent-soft);
            color: var(--c-accent);
            box-shadow: var(--shadow-lift);
            transform: translateY(-1px);
        }

        .stButton > button:active {
            transform: translateY(0);
            box-shadow: var(--shadow-card);
        }

        /* ── INPUTS ─────────────────────────────────────────────── */
        .stTextInput  > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput  > div > div > input,
        .stTextArea   > div > div > textarea {
            border-radius: var(--r-md) !important;
            border: 1.5px solid var(--c-border) !important;
            background-color: var(--c-card) !important;
            color: var(--c-text-hi) !important;
            transition:
                border-color 0.15s ease,
                box-shadow   0.15s ease;
        }

        .stTextInput  > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stDateInput  > div > div > input:focus,
        .stTextArea   > div > div > textarea:focus {
            border-color: var(--c-accent) !important;
            box-shadow: 0 0 0 3px var(--c-accent-soft) !important;
            outline: none;
        }

        div[data-baseweb="select"] > div:first-child {
            border-radius: var(--r-md) !important;
            border-color: var(--c-border) !important;
            background-color: var(--c-card) !important;
        }

        /* ── EXPANDERS ──────────────────────────────────────────── */
        [data-testid="stExpander"] {
            border: 1px solid var(--c-border);
            border-radius: var(--r-lg);
            background-color: var(--c-card);
            box-shadow: var(--shadow-card);
            overflow: hidden;
            transition: box-shadow 0.18s ease;
        }

        [data-testid="stExpander"]:hover {
            box-shadow: var(--shadow-lift);
        }

        [data-testid="stExpander"] details > summary {
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--c-text-hi) !important;
            padding: 0.75rem 1rem;
            cursor: pointer;
        }

        [data-testid="stExpander"] details > summary:hover {
            background-color: var(--c-accent-soft);
        }

        /* ── FORMS ──────────────────────────────────────────────── */
        [data-testid="stForm"] {
            border: 1px solid var(--c-border);
            border-radius: var(--r-xl);
            padding: 1.5rem;
            background-color: var(--c-card);
            box-shadow: var(--shadow-card);
        }

        /* ── ALERTS ─────────────────────────────────────────────── */
        [data-testid="stAlert"] {
            border-radius: var(--r-md) !important;
            font-weight: 500;
        }

        /* ── DIVIDERS ───────────────────────────────────────────── */
        hr {
            border: none;
            border-top: 1px solid var(--c-border) !important;
            margin: 1.5rem 0;
        }

        /* ── SCROLLBAR ──────────────────────────────────────────── */
        ::-webkit-scrollbar        { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track  { background: transparent; }
        ::-webkit-scrollbar-thumb  {
            background: var(--c-border);
            border-radius: 100px;
        }
        ::-webkit-scrollbar-thumb:hover { background: var(--c-text-lo); }

        </style>
        """,
        unsafe_allow_html=True,
    )
