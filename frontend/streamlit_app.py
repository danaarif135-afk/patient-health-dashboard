"""
Patient-Centric Dashboard
Frontend
"""

import random
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

from api import (
    backend_available,
    get_patients,
    get_dashboard
)

from utils import (
    status_badge
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Patient Dashboard",

    page_icon="🩺",

    layout="wide"

)

# ==========================================================
# SESSION STATE (page routing)
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "patient_id" not in st.session_state:
    st.session_state.patient_id = None

if "landing_error" not in st.session_state:
    st.session_state.landing_error = ""

# ==========================================================
# GLOBAL STYLE — GALAXY THEME (visual layer only — no logic/content changes)
# ==========================================================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* ---- Galaxy app background ---- */
        .stApp {
            background-color: #05060f;
            background-image:
                radial-gradient(circle at 15% 10%, rgba(139, 92, 246, 0.20), transparent 38%),
                radial-gradient(circle at 85% 0%, rgba(217, 70, 239, 0.14), transparent 42%),
                radial-gradient(circle at 50% 100%, rgba(34, 211, 238, 0.12), transparent 45%),
                linear-gradient(180deg, #05060f 0%, #0a0e1f 45%, #05060f 100%);
            background-attachment: fixed;
            overflow-x: hidden;
        }

        /* vignette for depth */
        .stApp::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.55) 100%);
            z-index: 0;
        }

        /* ---- Starfield layer (generated below, parallax via JS) ---- */
        #galaxy-layer {
            position: fixed;
            inset: 0;
            z-index: 0;
            overflow: hidden;
            pointer-events: none;
        }
        .galaxy-parallax {
            position: absolute;
            top: -10%;
            left: -10%;
            width: 120%;
            height: 120%;
            border-radius: 0;
            transition: transform 0.15s ease-out;
        }
        @keyframes twinkle {
            0%   { opacity: 0.25; }
            50%  { opacity: 1; }
            100% { opacity: 0.25; }
        }
        .twinkle-a { animation: twinkle 3.2s infinite ease-in-out; }
        .twinkle-b { animation: twinkle 4.6s infinite ease-in-out; }
        .twinkle-c { animation: twinkle 5.8s infinite ease-in-out; }

        /* keep actual app content above the starfield */
        .block-container, section[data-testid="stSidebar"] {
            position: relative;
            z-index: 1;
        }

        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1300px;
        }

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 8, 20, 0.92) 0%, rgba(16, 12, 28, 0.92) 100%);
            border-right: 1px solid rgba(168, 130, 255, 0.12);
            backdrop-filter: blur(4px);
        }
        section[data-testid="stSidebar"] h1 {
            font-family: 'Sora', sans-serif;
            font-size: 1.15rem;
            white-space: nowrap;
            color: #ECE9FF !important;
            -webkit-text-fill-color: #ECE9FF !important;
            background: none !important;
            border-bottom: 1px solid rgba(168, 130, 255, 0.18);
            padding-bottom: 0.6rem;
            margin-bottom: 1.1rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        section[data-testid="stSidebar"] h1::before {
            content: "✦";
            color: #C084FC;
            font-size: 1.1rem;
        }
        section[data-testid="stSidebar"] label {
            color: #B6AEDB !important;
            font-weight: 600;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        section[data-testid="stSidebar"] .stSelectbox > div > div,
        section[data-testid="stSidebar"] .stTextInput > div > div {
            background: rgba(14, 11, 26, 0.85);
            border: 1px solid rgba(192, 132, 252, 0.28);
            border-radius: 10px;
        }
        section[data-testid="stSidebar"] .stButton button {
            background: linear-gradient(135deg, #8B5CF6 0%, #D946EF 55%, #22D3EE 120%);
            background-size: 180% 180%;
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.6rem 1rem;
            width: 100%;
            box-shadow: 0 6px 18px rgba(139, 92, 246, 0.30);
            transition: transform 0.18s ease, box-shadow 0.18s ease, background-position 0.4s ease;
        }
        section[data-testid="stSidebar"] .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 28px rgba(217, 70, 239, 0.40);
            background-position: 100% 100%;
        }

        section[data-testid="stSidebar"] div[data-testid="stAlertContainer"] {
            border-radius: 10px;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 0.6rem 0.8rem;
        }

        /* ---- Title block ---- */
        h1 {
            font-family: 'Sora', sans-serif !important;
            background: linear-gradient(90deg, #C084FC 0%, #D946EF 45%, #22D3EE 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800 !important;
            letter-spacing: 0.2px;
            font-size: 2.3rem !important;
            line-height: 1.5 !important;
            margin-bottom: 0 !important;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        h1 img {
            height: 0.95em !important;
            width: 0.95em !important;
            vertical-align: middle !important;
            margin: 0 !important;
        }

        .stCaption, [data-testid="stCaptionContainer"] p {
            color: #9C93C9 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.02em;
            margin-top: -2px;
        }

        /* ---- Section headers ---- */
        h2 {
            font-family: 'Sora', sans-serif;
            color: #F0EDFF !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
            line-height: 1.9 !important;
            position: relative;
            padding-left: 16px;
            margin-top: 2.8rem !important;
            margin-bottom: 1.4rem !important;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        h2::before {
            content: "";
            position: absolute;
            left: 0;
            top: 6px;
            bottom: 6px;
            width: 5px;
            border-radius: 6px;
            background: linear-gradient(180deg, #8B5CF6, #22D3EE);
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.6);
        }
        /* emoji rendered as <img> by Streamlit — keep it inline and same height as text */
        h2 img {
            height: 1.1em !important;
            width: 1.1em !important;
            vertical-align: middle !important;
            margin: 0 !important;
            position: relative;
            top: -1px;
        }

        /* ---- Metric & chart cards share a spotlight cursor effect ---- */
        div[data-testid="stMetric"],
        div[data-testid="stPlotlyChart"] {
            position: relative;
            --mx: 50%;
            --my: 50%;
        }

        /* ---- Metric cards ---- */
        div[data-testid="stMetric"] {
            background: linear-gradient(160deg, rgba(24, 18, 42, 0.85), rgba(10, 8, 18, 0.88));
            backdrop-filter: blur(6px);
            border: 1px solid rgba(168, 130, 255, 0.16);
            border-radius: 16px;
            padding: 20px 18px 16px 18px;
            box-shadow: 0 10px 28px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.04);
            overflow: hidden;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #8B5CF6, #D946EF, #22D3EE);
            opacity: 0.9;
            box-shadow: 0 0 12px rgba(139, 92, 246, 0.6);
            z-index: 2;
        }
        /* cursor spotlight glow, position driven by JS-set --mx/--my */
        div[data-testid="stMetric"]::after,
        div[data-testid="stPlotlyChart"]::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(260px circle at var(--mx) var(--my), rgba(192, 132, 252, 0.20), transparent 60%);
            opacity: 0;
            transition: opacity 0.25s ease;
            pointer-events: none;
            z-index: 1;
            border-radius: inherit;
        }
        div[data-testid="stMetric"]:hover,
        div[data-testid="stPlotlyChart"]:hover {
            transform: translateY(-3px);
            border-color: rgba(192, 132, 252, 0.55);
            box-shadow: 0 16px 34px rgba(139, 92, 246, 0.25), inset 0 1px 0 rgba(255,255,255,0.06);
        }
        div[data-testid="stMetric"]:hover::after,
        div[data-testid="stPlotlyChart"]:hover::after {
            opacity: 1;
        }
        div[data-testid="stMetricLabel"] {
            color: #A99CDE !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.72rem !important;
            letter-spacing: 0.08em;
            position: relative;
            z-index: 2;
        }
        div[data-testid="stMetricValue"] {
            color: #F6F4FF !important;
            font-weight: 800 !important;
            font-size: 1.7rem !important;
            font-family: 'Sora', sans-serif;
            position: relative;
            z-index: 2;
        }
        div[data-testid="stMetricDelta"] {
            font-weight: 600 !important;
            position: relative;
            z-index: 2;
        }

        /* ---- Info / Warning boxes ---- */
        div[data-testid="stAlertContainer"] {
            border-radius: 14px;
            padding: 1rem 1.2rem !important;
            font-size: 0.98rem;
            line-height: 1.5;
        }

        div[data-testid="stAlertContainer"]:has(svg[data-testid="stIconInfo"]) {
            border: 1px solid rgba(34, 211, 238, 0.4);
            background: linear-gradient(135deg, rgba(34, 211, 238, 0.14), rgba(139, 92, 246, 0.08));
            box-shadow: 0 8px 22px rgba(34, 211, 238, 0.10);
        }

        div[data-testid="stAlertContainer"]:has(svg[data-testid="stIconWarning"]) {
            border: 1px solid rgba(245, 166, 35, 0.4);
            background: linear-gradient(135deg, rgba(245, 166, 35, 0.16), rgba(245, 166, 35, 0.05));
            box-shadow: 0 8px 22px rgba(245, 166, 35, 0.10);
        }

        div[data-testid="stAlertContainer"]:has(svg[data-testid="stIconError"]) {
            border: 1px solid rgba(244, 63, 94, 0.4);
            background: linear-gradient(135deg, rgba(244, 63, 94, 0.16), rgba(244, 63, 94, 0.05));
            box-shadow: 0 8px 22px rgba(244, 63, 94, 0.10);
        }

        /* ---- Plotly chart container ---- */
        div[data-testid="stPlotlyChart"] {
            background: linear-gradient(160deg, rgba(24, 18, 42, 0.85), rgba(8, 7, 16, 0.9));
            backdrop-filter: blur(6px);
            border: 1px solid rgba(168, 130, 255, 0.16);
            border-radius: 18px;
            padding: 14px;
            box-shadow: 0 14px 34px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.04);
        }

        hr {
            border-color: rgba(168, 130, 255, 0.14);
        }

        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #8B5CF6, #D946EF);
            border-radius: 8px;
        }

        /* ---- Landing page (targets st.container(key=...) generated classes) ---- */
        div.st-key-landing_shell {
            min-height: 78vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .landing-wrap {
            text-align: center;
            padding: 0 1rem 1.5rem 1rem;
            width: 100%;
        }
        .landing-title {
            font-family: 'Sora', sans-serif;
            font-weight: 800;
            font-size: 3rem;
            background: linear-gradient(90deg, #C084FC 0%, #D946EF 45%, #22D3EE 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.6rem;
        }
        .landing-sub {
            color: #B6AEDB;
            font-size: 1.05rem;
            max-width: 640px;
            margin: 0 auto 2.2rem auto;
            line-height: 1.6;
        }
        div.st-key-landing_card {
            background: linear-gradient(160deg, rgba(24, 18, 42, 0.85), rgba(10, 8, 18, 0.88));
            border: 1px solid rgba(168, 130, 255, 0.20);
            border-radius: 18px;
            padding: 2rem 2rem 1.4rem 2rem;
            box-shadow: 0 16px 40px rgba(0,0,0,0.5);
        }
        div.st-key-landing_card label {
            color: #A99CDE !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.72rem !important;
            letter-spacing: 0.08em;
        }
        div.st-key-landing_card .stTextInput > div > div {
            background: rgba(14, 11, 26, 0.9);
            border: 1px solid rgba(192, 132, 252, 0.3);
            border-radius: 10px;
        }
        .landing-hint {
            color: #7E76A8;
            font-size: 0.85rem;
            margin-top: 0.8rem;
        }

        /* ---- Hero section (patient dashboard) ---- */
        .hero-card {
            position: relative;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.16), rgba(217, 70, 239, 0.10) 50%, rgba(34, 211, 238, 0.10));
            border: 1px solid rgba(168, 130, 255, 0.22);
            border-radius: 22px;
            padding: 1.8rem 2rem;
            margin-bottom: 0.6rem;
            box-shadow: 0 16px 40px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.05);
            overflow: hidden;
        }
        .hero-card::before {
            content: "";
            position: absolute;
            top: -40%; right: -10%;
            width: 320px; height: 320px;
            background: radial-gradient(circle, rgba(192,132,252,0.25), transparent 65%);
            pointer-events: none;
        }
        .hero-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
            position: relative;
            z-index: 1;
        }
        .hero-id-block {
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }
        .hero-avatar {
            width: 54px; height: 54px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            background: linear-gradient(135deg, #8B5CF6, #D946EF, #22D3EE);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
            flex-shrink: 0;
        }
        .hero-name {
            font-family: 'Sora', sans-serif;
            font-weight: 800;
            font-size: 1.25rem;
            color: #F6F4FF;
            margin: 0;
        }
        .hero-meta {
            color: #B6AEDB;
            font-size: 0.85rem;
            margin-top: 2px;
        }
        .hero-badges {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
        }
        .hero-badge {
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.42rem 0.85rem;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            white-space: nowrap;
        }
        .badge-low { background: rgba(34, 211, 238, 0.16); border: 1px solid rgba(34, 211, 238, 0.45); color: #67E8F9; }
        .badge-medium { background: rgba(245, 166, 35, 0.16); border: 1px solid rgba(245, 166, 35, 0.45); color: #FBBF6A; }
        .badge-high { background: rgba(244, 63, 94, 0.16); border: 1px solid rgba(244, 63, 94, 0.45); color: #FB7185; }
        .badge-neutral { background: rgba(168, 130, 255, 0.16); border: 1px solid rgba(168, 130, 255, 0.40); color: #C7B9FF; }
        .hero-summary {
            margin-top: 1.1rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(168, 130, 255, 0.14);
            color: #DCD7F8;
            font-size: 0.92rem;
            line-height: 1.6;
            position: relative;
            z-index: 1;
        }

        /* ---- KPI cards (custom, color-coded) ---- */
        .kpi-card {
            position: relative;
            background: linear-gradient(160deg, rgba(24, 18, 42, 0.85), rgba(10, 8, 18, 0.88));
            border: 1px solid rgba(168, 130, 255, 0.16);
            border-radius: 16px;
            padding: 18px 18px 16px 18px;
            box-shadow: 0 10px 28px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.04);
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
            height: 100%;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: rgba(192, 132, 252, 0.55);
            box-shadow: 0 16px 34px rgba(139, 92, 246, 0.25);
        }
        .kpi-top-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.7rem;
        }
        .kpi-icon {
            width: 36px; height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.05rem;
        }
        .kpi-label {
            color: #A99CDE;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.08em;
        }
        .kpi-value {
            color: #F6F4FF;
            font-weight: 800;
            font-size: 1.6rem;
            font-family: 'Sora', sans-serif;
            line-height: 1.2;
        }
        .kpi-unit {
            color: #9C93C9;
            font-size: 0.78rem;
            font-weight: 600;
            margin-left: 4px;
        }

        /* ---- Clinical summary panel ---- */
        .summary-panel {
            background: linear-gradient(160deg, rgba(24, 18, 42, 0.85), rgba(8, 7, 16, 0.9));
            border: 1px solid rgba(168, 130, 255, 0.18);
            border-radius: 18px;
            padding: 1.5rem 1.7rem;
            box-shadow: 0 14px 34px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .summary-header {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.9rem;
        }
        .summary-icon {
            width: 38px; height: 38px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            background: linear-gradient(135deg, #8B5CF6, #22D3EE);
            box-shadow: 0 6px 16px rgba(139, 92, 246, 0.35);
        }
        .summary-title {
            font-family: 'Sora', sans-serif;
            font-weight: 700;
            font-size: 1.02rem;
            color: #F0EDFF;
        }
        .summary-text {
            color: #DCD7F8;
            font-size: 0.96rem;
            line-height: 1.65;
        }
        .summary-tags {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-top: 1.1rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(168, 130, 255, 0.14);
        }

        /* ---- Summary sub-sections (key findings / interpretation / recs / follow-up) ---- */
        .summary-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.9rem;
            margin-top: 1.1rem;
        }
        .summary-block {
            background: rgba(168, 130, 255, 0.06);
            border: 1px solid rgba(168, 130, 255, 0.14);
            border-radius: 12px;
            padding: 0.85rem 1rem;
        }
        .summary-block-title {
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #A99CDE;
            margin-bottom: 0.4rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        .summary-block-text {
            color: #DCD7F8;
            font-size: 0.88rem;
            line-height: 1.55;
        }

        /* ---- Landing: backend status + illustration ---- */
        .landing-status-row {
            display: flex;
            justify-content: center;
            margin-bottom: 1.4rem;
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 0.4rem 0.9rem;
            border-radius: 999px;
            letter-spacing: 0.02em;
        }
        .status-pill-on {
            background: rgba(52, 211, 153, 0.14);
            border: 1px solid rgba(52, 211, 153, 0.45);
            color: #6EE7B7;
        }
        .status-pill-off {
            background: rgba(244, 63, 94, 0.14);
            border: 1px solid rgba(244, 63, 94, 0.45);
            color: #FB7185;
        }
        .status-dot {
            width: 8px; height: 8px; border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 8px currentColor;
        }
        .landing-illustration {
            display: flex;
            justify-content: center;
            margin: 0.4rem 0 1.6rem 0;
            opacity: 0.92;
        }
        div.st-key-landing_card .stTextInput input {
            padding-left: 0.25rem;
        }

        /* ---- Patient profile cards ---- */
        .profile-card {
            background: linear-gradient(160deg, rgba(24, 18, 42, 0.85), rgba(10, 8, 18, 0.88));
            border: 1px solid rgba(168, 130, 255, 0.16);
            border-radius: 16px;
            padding: 1.3rem 1.4rem;
            text-align: center;
            box-shadow: 0 10px 28px rgba(0,0,0,0.45);
            transition: transform 0.2s ease, border-color 0.2s ease;
            height: 100%;
        }
        .profile-card:hover {
            transform: translateY(-3px);
            border-color: rgba(192, 132, 252, 0.5);
        }
        .profile-avatar-lg {
            width: 64px; height: 64px;
            margin: 0 auto 0.7rem auto;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            background: linear-gradient(135deg, #8B5CF6, #D946EF, #22D3EE);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
        }
        .profile-label {
            color: #A99CDE;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.08em;
            margin-bottom: 0.3rem;
        }
        .profile-value {
            color: #F6F4FF;
            font-weight: 800;
            font-size: 1.25rem;
            font-family: 'Sora', sans-serif;
        }

        /* ---- Vital status pills (Normal / Borderline / High) ---- */
        .vital-status {
            display: inline-block;
            margin-top: 0.5rem;
            font-size: 0.66rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 0.18rem 0.55rem;
            border-radius: 999px;
        }
        .vstat-normal { background: rgba(52, 211, 153, 0.16); border: 1px solid rgba(52, 211, 153, 0.4); color: #6EE7B7; }
        .vstat-borderline { background: rgba(245, 166, 35, 0.16); border: 1px solid rgba(245, 166, 35, 0.4); color: #FBBF6A; }
        .vstat-high { background: rgba(244, 63, 94, 0.16); border: 1px solid rgba(244, 63, 94, 0.4); color: #FB7185; }
        .vstat-na { background: rgba(168, 130, 255, 0.12); border: 1px solid rgba(168, 130, 255, 0.3); color: #C7B9FF; }

        /* ---- Reference comparison panel ---- */
        .compare-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.4rem;
        }
        .compare-table th {
            text-align: left;
            color: #A99CDE;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 800;
            padding: 0.6rem 0.8rem;
            border-bottom: 1px solid rgba(168, 130, 255, 0.18);
        }
        .compare-table td {
            padding: 0.65rem 0.8rem;
            color: #ECE9FF;
            font-size: 0.9rem;
            border-bottom: 1px solid rgba(168, 130, 255, 0.08);
        }
        .compare-table tr:last-child td { border-bottom: none; }

        /* ---- Health score gauge container ---- */
        .gauge-wrap {
            background: linear-gradient(160deg, rgba(24, 18, 42, 0.85), rgba(8, 7, 16, 0.9));
            border: 1px solid rgba(168, 130, 255, 0.18);
            border-radius: 18px;
            padding: 1rem 1.2rem 0.4rem 1.2rem;
            box-shadow: 0 14px 34px rgba(0,0,0,0.45);
        }

        /* ---- Sidebar patient info card ---- */
        .sb-patient-card {
            background: rgba(168, 130, 255, 0.08);
            border: 1px solid rgba(168, 130, 255, 0.22);
            border-radius: 14px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.9rem;
        }
        .sb-patient-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.82rem;
            color: #DCD7F8;
            padding: 0.18rem 0;
        }
        .sb-patient-row span:first-child { color: #9C93C9; }
        .sb-section-title {
            color: #A99CDE;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.07em;
            margin: 0.9rem 0 0.5rem 0;
        }
        .sb-version {
            color: #6F668F;
            font-size: 0.72rem;
            text-align: center;
            margin-top: 1.6rem;
            padding-top: 0.8rem;
            border-top: 1px solid rgba(168, 130, 255, 0.12);
        }

        /* ---- Footer ---- */
        .app-footer {
            margin-top: 3rem;
            padding-top: 1.6rem;
            border-top: 1px solid rgba(168, 130, 255, 0.14);
            text-align: center;
            color: #7E76A8;
            font-size: 0.82rem;
            line-height: 1.8;
        }
        .app-footer b { color: #B6AEDB; }
        .footer-tech {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        }
        .footer-tech span {
            background: rgba(168, 130, 255, 0.08);
            border: 1px solid rgba(168, 130, 255, 0.18);
            border-radius: 999px;
            padding: 0.25rem 0.7rem;
            font-size: 0.74rem;
            color: #B6AEDB;
        }

        /* ---- About section ---- */
        .about-card {
            background: rgba(168, 130, 255, 0.06);
            border: 1px solid rgba(168, 130, 255, 0.14);
            border-radius: 14px;
            padding: 1rem 1.2rem;
            color: #C7B9FF;
            font-size: 0.85rem;
            line-height: 1.6;
            margin-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# STARFIELD GENERATION (pure CSS box-shadow technique)
# ==========================================================

random.seed(7)

def _star_shadows(count, spread=2000, opacity_range=(0.4, 1.0)):
    parts = []
    for _ in range(count):
        x = random.randint(0, spread)
        y = random.randint(0, spread)
        o = round(random.uniform(*opacity_range), 2)
        parts.append(f"{x}px {y}px rgba(255,255,255,{o})")
    return ", ".join(parts)

_layer1 = _star_shadows(160, opacity_range=(0.3, 0.7))
_layer2 = _star_shadows(90, opacity_range=(0.5, 0.9))
_layer3 = _star_shadows(40, opacity_range=(0.6, 1.0))

st.markdown(
    f"""
    <style>
        .star-l1 {{
            width: 1px; height: 1px; background: transparent;
            box-shadow: {_layer1};
        }}
        .star-l2 {{
            width: 2px; height: 2px; background: transparent;
            box-shadow: {_layer2};
        }}
        .star-l3 {{
            width: 3px; height: 3px; background: transparent;
            border-radius: 50%;
            box-shadow: {_layer3};
        }}
    </style>
    <div id="galaxy-layer">
        <div class="galaxy-parallax star-l1 twinkle-a" id="gx-layer-1" data-depth="6"></div>
        <div class="galaxy-parallax star-l2 twinkle-b" id="gx-layer-2" data-depth="14"></div>
        <div class="galaxy-parallax star-l3 twinkle-c" id="gx-layer-3" data-depth="26"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# CURSOR INTERACTIVITY — parallax stars + card spotlight
# ==========================================================

components.html(
    """
    <script>
    (function () {
        const doc = window.parent.document;

        function handleMove(e) {
            const w = window.parent.innerWidth || doc.documentElement.clientWidth;
            const h = window.parent.innerHeight || doc.documentElement.clientHeight;
            const relX = (e.clientX / w - 0.5) * 2;
            const relY = (e.clientY / h - 0.5) * 2;

            ["gx-layer-1", "gx-layer-2", "gx-layer-3"].forEach((id) => {
                const el = doc.getElementById(id);
                if (!el) return;
                const depth = parseFloat(el.getAttribute("data-depth")) || 10;
                el.style.transform =
                    "translate(" + (relX * -depth) + "px, " + (relY * -depth) + "px)";
            });

            const cards = doc.querySelectorAll(
                '[data-testid="stMetric"], [data-testid="stPlotlyChart"]'
            );
            cards.forEach((card) => {
                const rect = card.getBoundingClientRect();
                if (
                    e.clientX >= rect.left && e.clientX <= rect.right &&
                    e.clientY >= rect.top && e.clientY <= rect.bottom
                ) {
                    const mx = ((e.clientX - rect.left) / rect.width) * 100;
                    const my = ((e.clientY - rect.top) / rect.height) * 100;
                    card.style.setProperty("--mx", mx + "%");
                    card.style.setProperty("--my", my + "%");
                }
            });
        }

        if (!doc.__galaxyMouseBound) {
            doc.addEventListener("mousemove", handleMove);
            doc.__galaxyMouseBound = true;
        }
    })();
    </script>
    """,
    height=0,
)

# Shared color palette for charts, used only for styling (no data/content change)
ACCENT = "#A78BFA"
ACCENT_2 = "#D946EF"
ACCENT_3 = "#22D3EE"

def _hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

def style_chart(fig, line_color=ACCENT):
    """Apply a consistent, polished galaxy-themed visual style to a Plotly figure."""
    fig.update_traces(
        line=dict(color=line_color, width=3.5, shape="spline", smoothing=0.35),
        marker=dict(
            size=8,
            color=line_color,
            line=dict(width=2, color="#05060f"),
        ),
        fill="tozeroy",
        fillcolor=_hex_to_rgba(line_color, 0.16),
        hovertemplate="<b>%{y}</b><br>%{x|%b %Y}<extra></extra>",
    )
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ECE9FF", family="Inter, sans-serif", size=13),
        title_font=dict(size=18, color="#F6F4FF", family="Sora, sans-serif"),
        hoverlabel=dict(
            bgcolor="#160f2b",
            bordercolor=line_color,
            font=dict(color="#F6F4FF", size=13),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#B6AEDB"),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(168, 130, 255, 0.08)",
            zeroline=False,
            showline=True,
            linecolor="rgba(168, 130, 255, 0.18)",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(168, 130, 255, 0.08)",
            zeroline=False,
            showline=False,
        ),
        margin=dict(l=10, r=10, t=55, b=10),
        hovermode="x unified",
    )
    return fig

def add_reference_band(fig, df, low=None, high=None, color=ACCENT_3, label="Reference range"):
    """
    Overlay a shaded reference/normal range band on a trend chart, if bounds
    are available. Purely presentational — does not touch the underlying data.
    """
    if low is None or high is None or df.empty:
        return fig
    try:
        x0 = df["date"].min()
        x1 = df["date"].max()
        fig.add_shape(
            type="rect",
            x0=x0, x1=x1, y0=low, y1=high,
            fillcolor=_hex_to_rgba(color, 0.10),
            line=dict(width=0),
            layer="below",
        )
        fig.add_trace(
            go.Scatter(
                x=[x0, x1],
                y=[high, high],
                mode="lines",
                line=dict(color=_hex_to_rgba(color, 0.55), width=1, dash="dot"),
                name=label,
                hoverinfo="skip",
                showlegend=True,
            )
        )
    except Exception:
        pass
    return fig

def annotate_latest_point(fig, df, color=ACCENT):
    """Highlight and label the most recent reading on a trend chart."""
    if df.empty:
        return fig
    try:
        last_row = df.sort_values("date").iloc[-1]
        fig.add_annotation(
            x=last_row["date"], y=last_row["value"],
            text=f"Latest: {last_row['value']}",
            showarrow=True, arrowhead=2, arrowcolor=color,
            ax=0, ay=-38,
            font=dict(color="#F6F4FF", size=11, family="Inter, sans-serif"),
            bgcolor="#160f2b",
            bordercolor=color,
            borderwidth=1,
            borderpad=4,
        )
    except Exception:
        pass
    return fig

def _risk_badge_class(risk_band):
    risk = str(risk_band).lower()
    if "high" in risk:
        return "badge-high"
    if "med" in risk:
        return "badge-medium"
    if "low" in risk:
        return "badge-low"
    return "badge-neutral"

def _trend_icon(trend):
    t = str(trend).lower()
    if "up" in t or "increas" in t or "ris" in t:
        return "📈"
    if "down" in t or "decreas" in t or "fall" in t:
        return "📉"
    return "➖"

def render_hero(patient, analytics, summary):
    """Professional hero section — patient branding + at-a-glance summary."""
    gender = "Male" if patient["gender"] == 1 else "Female"
    risk_class = _risk_badge_class(analytics["risk_band"])
    trend_icon = _trend_icon(analytics["trend"])

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-top">
                <div class="hero-id-block">
                    <div class="hero-avatar">🩺</div>
                    <div>
                        <p class="hero-name">Patient {patient['patient_id'][:8]}</p>
                        <div class="hero-meta">{gender} &nbsp;•&nbsp; Age {patient['age']} &nbsp;•&nbsp; ID {patient['patient_id'][:8]}</div>
                    </div>
                </div>
                <div class="hero-badges">
                    <span class="hero-badge {risk_class}">⚠ {analytics['risk_band']} risk</span>
                    <span class="hero-badge badge-neutral">{trend_icon} {str(analytics['trend']).capitalize()} trend</span>
                    <span class="hero-badge badge-neutral">⛯ {analytics['anomaly_count']} anomalies</span>
                </div>
            </div>
            <div class="hero-summary">{summary}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_kpi_card(col, icon, label, value, unit="", accent="#8B5CF6", status=None, subtitle=None):
    """Reusable KPI card component with icon, accent color, optional status pill and subtitle."""
    status_html = f'<div class="vital-status {status[0]}">{status[1]}</div>' if status else ""
    subtitle_html = f'<div style="color:#9C93C9; font-size:0.74rem; margin-top:6px;">{subtitle}</div>' if subtitle else ""
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <span class="kpi-label">{label}</span>
                    <div class="kpi-icon" style="background:{_hex_to_rgba(accent, 0.18)}; border:1px solid {_hex_to_rgba(accent, 0.4)};">{icon}</div>
                </div>
                <div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>
                {status_html}
                {subtitle_html}
            </div>
            """,
            unsafe_allow_html=True
        )

def render_summary_panel(summary, analytics):
    """Polished clinical assessment card: findings, interpretation, recommendation, follow-up."""
    risk_class = _risk_badge_class(analytics["risk_band"])
    trend_icon = _trend_icon(analytics["trend"])
    risk = str(analytics["risk_band"]).lower()
    trend = str(analytics["trend"]).lower()

    if "high" in risk:
        interpretation = "Current readings fall into the high-risk band, indicating values outside expected healthy ranges."
        recommendation = "Closer clinical monitoring and a review of the latest vitals with a care provider is advised."
        follow_up = "Schedule a follow-up consultation as soon as practical."
    elif "med" in risk:
        interpretation = "Current readings fall into the medium-risk band, with some values trending away from target ranges."
        recommendation = "Continue regular monitoring and lifestyle measures aligned with this patient's care plan."
        follow_up = "A routine follow-up in the near term is recommended."
    else:
        interpretation = "Current readings fall into the low-risk band, broadly consistent with healthy reference ranges."
        recommendation = "Maintain current monitoring routine and lifestyle measures."
        follow_up = "Standard scheduled follow-up is sufficient."

    if "up" in trend or "increas" in trend or "ris" in trend:
        findings = f"Vitals show an increasing trend with {analytics['anomaly_count']} anomaly point(s) detected."
    elif "down" in trend or "decreas" in trend or "fall" in trend:
        findings = f"Vitals show a decreasing trend with {analytics['anomaly_count']} anomaly point(s) detected."
    else:
        findings = f"Vitals show a stable trend with {analytics['anomaly_count']} anomaly point(s) detected."

    st.markdown(
        f"""
        <div class="summary-panel">
            <div class="summary-header">
                <div class="summary-icon">📝</div>
                <div class="summary-title">Clinical Summary</div>
            </div>
            <div class="summary-text">{summary}</div>
            <div class="summary-grid">
                <div class="summary-block">
                    <div class="summary-block-title">🔎 Key Findings</div>
                    <div class="summary-block-text">{findings}</div>
                </div>
                <div class="summary-block">
                    <div class="summary-block-title">⚠️ Risk Interpretation</div>
                    <div class="summary-block-text">{interpretation}</div>
                </div>
                <div class="summary-block">
                    <div class="summary-block-title">💡 Recommendation</div>
                    <div class="summary-block-text">{recommendation}</div>
                </div>
                <div class="summary-block">
                    <div class="summary-block-title">📅 Follow-up Advice</div>
                    <div class="summary-block-text">{follow_up}</div>
                </div>
            </div>
            <div class="summary-tags">
                <span class="hero-badge {risk_class}">⚠ {analytics['risk_band']} risk</span>
                <span class="hero-badge badge-neutral">{trend_icon} {str(analytics['trend']).capitalize()} trend</span>
                <span class="hero-badge badge-neutral">⛯ {analytics['anomaly_count']} anomalies detected</span>
                <span class="hero-badge badge-neutral">💉 Mean glucose {analytics['mean_glucose']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def vital_status(value, ref):
    """Classify a vital reading as Normal / Borderline / High based on its reference range."""
    if not isinstance(ref, dict) or ref.get("low") is None or ref.get("high") is None:
        return "vstat-na", "N/A"
    try:
        v = float(value)
        low, high = float(ref["low"]), float(ref["high"])
        span = max(high - low, 1e-6)
        if low <= v <= high:
            return "vstat-normal", "Normal"
        if (low - 0.1 * span) <= v <= (high + 0.1 * span):
            return "vstat-borderline", "Borderline"
        return "vstat-high", "High"
    except (TypeError, ValueError):
        return "vstat-na", "N/A"

def compute_health_score(analytics, latest, reference):
    """
    Deterministic 0-100 health score derived purely from existing analytics
    and vitals — presentational aggregation only, no new data sources.
    """
    score = 100.0
    risk = str(analytics["risk_band"]).lower()
    if "high" in risk:
        score -= 40
    elif "med" in risk:
        score -= 20

    trend = str(analytics["trend"]).lower()
    if "up" in trend or "increas" in trend or "ris" in trend:
        score -= 10
    elif "down" in trend or "decreas" in trend or "fall" in trend:
        score += 5

    score -= min(float(analytics.get("anomaly_count", 0)) * 5, 30)

    out_of_range = 0
    counted = 0
    for name, v in latest.items():
        ref = reference.get(name, {}) if isinstance(reference, dict) else {}
        cls, _ = vital_status(v["value"], ref)
        if cls != "vstat-na":
            counted += 1
            if cls == "vstat-high":
                out_of_range += 1
    if counted:
        score -= (out_of_range / counted) * 15

    return max(0, min(100, round(score)))

def render_health_score_gauge(score):
    if score >= 75:
        bar_color = "#34D399"
    elif score >= 50:
        bar_color = "#F5A623"
    else:
        bar_color = "#F43F5E"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": " / 100", "font": {"size": 34, "color": "#F6F4FF", "family": "Sora, sans-serif"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#9C93C9", "tickfont": {"color": "#9C93C9", "size": 10}},
            "bar": {"color": bar_color, "thickness": 0.32},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "rgba(244, 63, 94, 0.14)"},
                {"range": [50, 75], "color": "rgba(245, 166, 35, 0.14)"},
                {"range": [75, 100], "color": "rgba(52, 211, 153, 0.14)"},
            ],
        },
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ECE9FF", family="Inter, sans-serif"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def render_profile_cards(patient, summary):
    """Patient profile shown as attractive cards with avatar, status, and last-updated time."""
    gender = "Male" if patient["gender"] == 1 else "Female"
    status_label = "Stable" if "stable" in str(summary).lower() or "normal" in str(summary).lower() else "Under Observation"
    now_str = datetime.now().strftime("%b %d, %Y · %H:%M")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="profile-card">
                <div class="profile-avatar-lg">🧑‍⚕️</div>
                <div class="profile-label">Patient ID</div>
                <div class="profile-value">{patient['patient_id'][:8]}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""<div class="profile-card">
                <div class="profile-avatar-lg">🎂</div>
                <div class="profile-label">Age</div>
                <div class="profile-value">{patient['age']}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""<div class="profile-card">
                <div class="profile-avatar-lg">{'👨' if patient['gender'] == 1 else '👩'}</div>
                <div class="profile-label">Gender</div>
                <div class="profile-value">{gender}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""<div class="profile-card">
                <div class="profile-avatar-lg">🕐</div>
                <div class="profile-label">Status · Last Updated</div>
                <div class="profile-value" style="font-size:1.0rem;">{status_label}</div>
                <div style="color:#7E76A8; font-size:0.74rem; margin-top:4px;">{now_str}</div>
            </div>""",
            unsafe_allow_html=True
        )

def render_comparison_panel(latest, reference):
    """Patient value vs. population reference mean, with a clinical status column."""
    rows = []
    for name, v in latest.items():
        ref = reference.get(name, {}) if isinstance(reference, dict) else {}
        cls, label = vital_status(v["value"], ref)
        if ref.get("low") is not None and ref.get("high") is not None:
            try:
                pop_mean = ref.get("mean", (float(ref["low"]) + float(ref["high"])) / 2)
                diff = float(v["value"]) - float(pop_mean)
                diff_str = f"{'+' if diff >= 0 else ''}{diff:.1f}"
                pop_mean_str = f"{pop_mean:.1f}"
            except (TypeError, ValueError):
                pop_mean_str, diff_str = "—", "—"
        else:
            pop_mean_str, diff_str = "—", "—"

        rows.append(
            f"""<tr>
                <td>{name.replace('_', ' ').title()}</td>
                <td>{v['value']} {v['units']}</td>
                <td>{pop_mean_str}</td>
                <td>{diff_str}</td>
                <td><span class="vital-status {cls}">{label}</span></td>
            </tr>"""
        )

    st.markdown(
        f"""
        <div class="summary-panel">
            <div class="summary-header">
                <div class="summary-icon">📊</div>
                <div class="summary-title">Reference Comparison</div>
            </div>
            <table class="compare-table">
                <tr>
                    <th>Vital</th>
                    <th>Patient Value</th>
                    <th>Population Mean</th>
                    <th>Difference</th>
                    <th>Clinical Status</th>
                </tr>
                {''.join(rows)}
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_footer():
    st.markdown(
        """
        <div class="app-footer">
            <div><b>Patient-Centric Dashboard</b> — Healthcare Analytics Platform</div>
            <div>Built by <b>MedTech Innovators</b></div>
            <div class="footer-tech">
                <span>FastAPI</span><span>Streamlit</span><span>Plotly</span><span>Supabase</span>
            </div>
            <div style="margin-top:0.6rem;">© 2026 · Version 1.0.0</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# LANDING PAGE
# ==========================================================

if st.session_state.page == "landing":

    backend = backend_available()

    landing_shell = st.container(key="landing_shell")

    with landing_shell:

        status_class = "status-pill-on" if backend else "status-pill-off"
        status_text = "Backend Connected" if backend else "Backend Unavailable"

        st.markdown(
            f"""
            <div class="landing-wrap">
                <div class="landing-status-row">
                    <span class="status-pill {status_class}"><span class="status-dot"></span>{status_text}</span>
                </div>
                <div class="landing-title">🩺 Patient-Centric Dashboard</div>
                <div class="landing-sub">
                    A galaxy-themed healthcare analytics dashboard that brings together a patient's
                    vitals, trends, and clinical summary in one place. Enter a patient ID below to
                    explore their personalized analytics — glucose, BMI, and blood pressure trends,
                    risk classification, and anomaly detection, all in a single view.
                </div>
                <div class="landing-illustration">
                    <svg width="180" height="120" viewBox="0 0 180 120" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="lgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#8B5CF6"/>
                                <stop offset="55%" stop-color="#D946EF"/>
                                <stop offset="100%" stop-color="#22D3EE"/>
                            </linearGradient>
                        </defs>
                        <rect x="20" y="20" width="140" height="80" rx="16" fill="url(#lgGrad)" opacity="0.14"/>
                        <rect x="20" y="20" width="140" height="80" rx="16" fill="none" stroke="url(#lgGrad)" stroke-width="1.5" opacity="0.5"/>
                        <path d="M30 62 H62 L70 42 L82 82 L92 58 L100 62 H150" fill="none" stroke="url(#lgGrad)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="138" cy="34" r="11" fill="none" stroke="url(#lgGrad)" stroke-width="2.4"/>
                        <path d="M138 29 V39 M133 34 H143" stroke="url(#lgGrad)" stroke-width="2.4" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not backend:
            st.error(status_badge(False))
            st.stop()

        left_pad, center_col, right_pad = st.columns([1, 1.3, 1])

        with center_col:

            landing_card = st.container(key="landing_card")

            with landing_card:

                patient_input = st.text_input(
                    "🔍 Enter Patient ID",
                    placeholder="e.g. 01ba763c",
                    key="landing_patient_input"
                )

                st.markdown(
                    '<div class="landing-hint">Type the patient ID and press Enter to open the dashboard.</div>',
                    unsafe_allow_html=True
                )

                if st.session_state.landing_error:
                    st.error(st.session_state.landing_error)

    if patient_input:

        patients = get_patients()

        match = next(
            (p for p in patients if p["patient_id"] == patient_input or p["patient_id"].startswith(patient_input)),
            None
        )

        if match:
            st.session_state.patient_id = match["patient_id"]
            st.session_state.page = "dashboard"
            st.session_state.landing_error = ""
            st.rerun()
        else:
            st.session_state.landing_error = "No patient found with that ID. Please check and try again."
            st.rerun()

    st.stop()

# ==========================================================
# TITLE
# ==========================================================

st.title("🩺 Patient-Centric Dashboard")

st.caption(
    "Healthcare Analytics Dashboard"
)

# ==========================================================
# BACKEND STATUS CHECK
# ==========================================================

backend = backend_available()

if not backend:
    st.sidebar.title("Dashboard")
    if st.sidebar.button("⟵ Back to Home"):
        st.session_state.page = "landing"
        st.session_state.landing_error = ""
        st.rerun()
    st.sidebar.error(status_badge(False))
    st.stop()

# ==========================================================
# LOAD DASHBOARD (patient already selected on the landing page)
# ==========================================================

patient_id = st.session_state.patient_id

dashboard = get_dashboard(patient_id)

# ==========================================================
# Extract Dashboard Data
# ==========================================================

overview = dashboard["overview"]

analytics = dashboard["analytics"]

history = dashboard["history"]

patient = overview["patient"]

latest = overview["latest_vitals"]

reference = overview["reference"]

summary = dashboard["summary"]

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Dashboard")

if st.sidebar.button("⟵ Back to Home"):
    st.session_state.page = "landing"
    st.session_state.landing_error = ""
    st.rerun()

if st.sidebar.button("🔄 Refresh Dashboard"):
    st.rerun()

# ----------------------------------------------------------
# Backend Status
# ----------------------------------------------------------

st.sidebar.success(status_badge(True))

# ----------------------------------------------------------
# Current Patient (read-only summary — dropdown removed)
# ----------------------------------------------------------

_gender_label = "Male" if patient["gender"] == 1 else "Female"

st.sidebar.markdown('<div class="sb-section-title">Current Patient</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    f"""
    <div class="sb-patient-card">
        <div class="sb-patient-row"><span>Patient ID</span><span>{patient['patient_id'][:8]}</span></div>
        <div class="sb-patient-row"><span>Age</span><span>{patient['age']}</span></div>
        <div class="sb-patient-row"><span>Gender</span><span>{_gender_label}</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="sb-section-title">Health Status</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    f"""
    <div class="sb-patient-card">
        <div class="sb-patient-row"><span>Risk</span><span>{analytics['risk_band']}</span></div>
        <div class="sb-patient-row"><span>Trend</span><span>{str(analytics['trend']).capitalize()}</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sb-version">Patient-Centric Dashboard · v1.0.0</div>',
    unsafe_allow_html=True
)

# ==========================================================
# Hero Section — branding + at-a-glance patient summary
# ==========================================================

render_hero(patient, analytics, summary)

# ==========================================================
# Patient Profile
# ==========================================================

st.header("👤 Patient Profile")

render_profile_cards(patient, summary)

# ==========================================================
# Analytics (custom KPI cards — icons, accent colors, hover lift)
# ==========================================================

st.header("📊 Analytics")

_risk_l = str(analytics["risk_band"]).lower()
_trend_l = str(analytics["trend"]).lower()
_trend_note = "Worsening" if ("up" in _trend_l or "increas" in _trend_l or "ris" in _trend_l) else ("Improving" if ("down" in _trend_l or "decreas" in _trend_l or "fall" in _trend_l) else "Stable")
_risk_note = "Requires Monitoring" if ("high" in _risk_l or "med" in _risk_l) else "Stable"
_anomaly_note = "Review Recommended" if analytics["anomaly_count"] else "None Detected"

col1, col2, col3, col4 = st.columns(4)

render_kpi_card(col1, "📈", "Trend", analytics["trend"].capitalize(), accent=ACCENT, subtitle=_trend_note)
render_kpi_card(col2, "⚠️", "Risk", analytics["risk_band"], accent=ACCENT_2, subtitle=_risk_note)
render_kpi_card(col3, "⛯", "Anomalies", analytics["anomaly_count"], accent="#F5A623", subtitle=_anomaly_note)
render_kpi_card(col4, "💉", "Mean Glucose", analytics["mean_glucose"], unit=" mg/dL", accent=ACCENT_3, subtitle="Reference: see chart below")

# ==========================================================
# Health Score
# ==========================================================

st.header("🧮 Overall Health Score")

_health_score = compute_health_score(analytics, latest, reference)
gcol1, gcol2 = st.columns([1, 1.6])

with gcol1:
    st.markdown('<div class="gauge-wrap">', unsafe_allow_html=True)
    render_health_score_gauge(_health_score)
    st.markdown('</div>', unsafe_allow_html=True)

with gcol2:
    _score_word = "Good" if _health_score >= 75 else ("Fair" if _health_score >= 50 else "Needs Attention")
    st.markdown(
        f"""
        <div class="summary-panel" style="height:100%;">
            <div class="summary-header">
                <div class="summary-icon">🧮</div>
                <div class="summary-title">Score Breakdown — {_score_word}</div>
            </div>
            <div class="summary-text">
                This score combines the current risk band, vitals trend, anomaly count, and how many
                latest vitals fall within their reference ranges into a single 0–100 indicator.
            </div>
            <div class="summary-tags">
                <span class="hero-badge {_risk_badge_class(analytics['risk_band'])}">⚠ {analytics['risk_band']} risk</span>
                <span class="hero-badge badge-neutral">{_trend_icon(analytics['trend'])} {str(analytics['trend']).capitalize()} trend</span>
                <span class="hero-badge badge-neutral">⛯ {analytics['anomaly_count']} anomalies</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# Latest Vitals (custom KPI cards)
# ==========================================================

st.header("❤️ Latest Vitals")

_vital_icons = ["💉", "⚖️", "🩸", "❤️", "🌡️", "🫀", "🫁", "🧬"]
_vital_accents = [ACCENT, ACCENT_2, ACCENT_3, "#F5A623", "#34D399", "#F472B6", "#60A5FA", "#FBBF24"]

cols = st.columns(len(latest))

for i, (column, (name, value)) in enumerate(zip(cols, latest.items())):

    _ref = reference.get(name, {}) if isinstance(reference, dict) else {}
    _status = vital_status(value["value"], _ref)

    render_kpi_card(
        column,
        _vital_icons[i % len(_vital_icons)],
        name.replace("_", " ").title(),
        value["value"],
        unit=f" {value['units']}",
        accent=_vital_accents[i % len(_vital_accents)],
        status=_status,
    )

# ==========================================================
# Reference Comparison
# ==========================================================

st.header("📊 Reference Comparison")

render_comparison_panel(latest, reference)

# ----------------------------------------------------------
# Download patient data as CSV
# ----------------------------------------------------------

_vitals_rows = [
    {"vital": name.replace("_", " ").title(), "value": v["value"], "units": v["units"]}
    for name, v in latest.items()
]
_csv_bytes = pd.DataFrame(_vitals_rows).to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Latest Vitals (CSV)",
    data=_csv_bytes,
    file_name=f"patient_{patient['patient_id'][:8]}_vitals.csv",
    mime="text/csv",
)

# ==========================================================
# Clinical Summary (polished panel with status indicators)
# ==========================================================

st.header("📝 Clinical Summary")

render_summary_panel(summary, analytics)

# ==========================================================
# Glucose Trend Chart
# ==========================================================

st.header("📈 Glucose Trend")

glucose_history = history.get("glucose", [])

if len(glucose_history) > 0:

    df = pd.DataFrame(glucose_history)

    df["date"] = pd.to_datetime(df["date"])

    fig = px.line(

        df,

        x="date",

        y="value",

        markers=True,

        title="Blood Glucose Over Time"

    )

    fig.update_layout(

        template="plotly_dark",

        xaxis_title="Date",

        yaxis_title="Glucose (mg/dL)",

        height=450

    )

    _ref = reference.get("glucose", {}) if isinstance(reference, dict) else {}
    fig = add_reference_band(
        fig, df,
        low=_ref.get("low"), high=_ref.get("high"),
        color=ACCENT, label="Normal range"
    )
    fig = annotate_latest_point(fig, df, color=ACCENT)

    fig = style_chart(fig, line_color=ACCENT)

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar": True, "scrollZoom": True, "displaylogo": False}

    )

else:

    st.warning(

        "No glucose history available for this patient."

    )
# ==========================================================
# BMI Trend Chart
# ==========================================================

st.header("📉 BMI Trend")

bmi_history = history.get("bmi", [])

if len(bmi_history) > 0:

    df = pd.DataFrame(bmi_history)

    df["date"] = pd.to_datetime(df["date"])

    fig = px.line(

        df,

        x="date",

        y="value",

        markers=True,

        title="Body Mass Index (BMI) Over Time"

    )

    fig.update_layout(

        template="plotly_dark",

        xaxis_title="Date",

        yaxis_title="BMI (kg/m²)",

        height=450

    )

    _ref = reference.get("bmi", {}) if isinstance(reference, dict) else {}
    fig = add_reference_band(
        fig, df,
        low=_ref.get("low"), high=_ref.get("high"),
        color=ACCENT_2, label="Normal range"
    )
    fig = annotate_latest_point(fig, df, color=ACCENT_2)

    fig = style_chart(fig, line_color=ACCENT_2)

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar": True, "scrollZoom": True, "displaylogo": False}

    )

else:

    st.warning(

        "No BMI history available for this patient."

    )

# ==========================================================
# Blood Pressure Trend Chart
# ==========================================================

st.header("🩸 Blood Pressure Trend")

bp_history = history.get("systolic_bp", [])

if len(bp_history) > 0:

    df = pd.DataFrame(bp_history)

    df["date"] = pd.to_datetime(df["date"])

    fig = px.line(

        df,

        x="date",

        y="value",

        markers=True,

        title="Systolic Blood Pressure Over Time"

    )

    fig.update_layout(

        template="plotly_dark",

        xaxis_title="Date",

        yaxis_title="Blood Pressure (mmHg)",

        height=450

    )

    _ref = reference.get("systolic_bp", {}) if isinstance(reference, dict) else {}
    fig = add_reference_band(
        fig, df,
        low=_ref.get("low"), high=_ref.get("high"),
        color=ACCENT_3, label="Normal range"
    )
    fig = annotate_latest_point(fig, df, color=ACCENT_3)

    fig = style_chart(fig, line_color=ACCENT_3)

    st.plotly_chart(

        fig,

        use_container_width=True,

        config={"displayModeBar": True, "scrollZoom": True, "displaylogo": False}

    )

else:

    st.warning(

        "No blood pressure history available for this patient."

    )

# ==========================================================
# About the Dashboard
# ==========================================================

st.header("ℹ️ About This Dashboard")

st.markdown(
    """
    <div class="about-card">
        This dashboard brings together a patient's vitals, historical trends, and clinical
        analytics into one healthcare-themed view. Risk band, trend, and anomaly count are
        computed by the backend; the overall health score, vital status pills, and reference
        comparisons shown here are presentational summaries derived from those same values.
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# Footer
# ==========================================================

render_footer()