import json
import math
from datetime import datetime

import pandas as pd
import streamlit as st


st.markdown("""
<style>
/* Keep Download button text visible after click/focus/active states */
div[data-testid="stDownloadButton"] button,
div[data-testid="stDownloadButton"] button p,
div[data-testid="stDownloadButton"] button span {
    color: #111111 !important;
    opacity: 1 !important;
    visibility: visible !important;
}
div[data-testid="stDownloadButton"] button:hover,
div[data-testid="stDownloadButton"] button:focus,
div[data-testid="stDownloadButton"] button:active {
    color: #111111 !important;
}
</style>
""", unsafe_allow_html=True)

from google import genai

# ============================================================
# Bijli Bachat AI — Smart Energy & Bill Optimizer
# Hackathon MVP
# ============================================================

st.set_page_config(
    page_title="Bijli Bachat AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Professional UI styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f0fdf4 100%);
    }

    [data-testid="stSidebar"] {
        background: #0f172a;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    .hero {
        padding: 2rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #0f172a 0%, #164e63 55%, #166534 100%);
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 12px 35px rgba(15, 23, 42, .18);
    }
    .hero h1 { margin: 0; font-size: 2.5rem; color: #ffffff !important; }
    .hero p { margin: .55rem 0 0; color: #dbeafe !important; font-size: 1.05rem; }

    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.1rem;
        box-shadow: 0 6px 20px rgba(15, 23, 42, .06);
        margin-bottom: .8rem;
        color: #0f172a !important;
    }

    .metric-title { color: #475569 !important; font-size: .86rem; }
    .metric-value { color: #0f172a !important; font-size: 1.55rem; font-weight: 750; }

    .badge {
        display: inline-block;
        padding: .28rem .7rem;
        border-radius: 999px;
        font-size: .78rem;
        font-weight: 700;
        background: #dcfce7;
        color: #166534 !important;
    }

    .carbon-card {
        background: linear-gradient(135deg, #0f172a 0%, #164e63 55%, #166534 100%);
        border: 1px solid rgba(255,255,255,.15);
        border-radius: 18px;
        padding: 1.25rem 1.4rem;
        color: #ffffff !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, .16);
        margin: .7rem 0 1rem 0;
    }

    .carbon-label {
        color: #d1fae5 !important;
        font-size: .95rem;
        font-weight: 750;
        letter-spacing: .01em;
    }

    .carbon-value {
        color: #ffffff !important;
        font-size: 1.55rem;
        font-weight: 800;
        margin: .25rem 0 .35rem 0;
    }

    .carbon-note {
        color: #dbeafe !important;
        font-size: .86rem;
        line-height: 1.45;
    }

    .section-title {
        color: #0f172a !important;
        font-size: 1.35rem;
        font-weight: 750;
        margin-top: .6rem;
    }

    .small-muted { color: #475569 !important; font-size: .88rem; }

    .warning-card {
        border-left: 5px solid #f59e0b;
        background: #fffbeb;
        padding: .9rem 1rem;
        border-radius: 12px;
        color: #78350f !important;
    }

    .success-card {
        border-left: 5px solid #16a34a;
        background: #f0fdf4;
        padding: .9rem 1rem;
        border-radius: 12px;
        color: #14532d !important;
    }

    /* Professional AI section navigation */
    .ai-nav-label {
        color: #0f172a !important;
        font-size: .82rem;
        font-weight: 750;
        margin-bottom: .35rem;
    }

    /* Compact, text-style AI navigation — no large boxes */
    [data-testid="stRadio"] {
        margin-top: .1rem;
        margin-bottom: .35rem;
    }

    [data-testid="stRadio"] > label {
        display: none !important;
    }

    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: .25rem !important;
        align-items: center !important;
        flex-wrap: wrap !important;
    }

    [data-testid="stRadio"] div[role="radiogroup"] > label {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: .35rem .75rem .45rem .15rem !important;
        margin: 0 .35rem 0 0 !important;
        color: #334155 !important;
        font-size: .84rem !important;
        font-weight: 700 !important;
        min-height: auto !important;
        cursor: pointer !important;
        transition: color .18s ease, border-color .18s ease !important;
        border-bottom: 2px solid transparent !important;
    }

    [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        color: #0f766e !important;
        border-bottom-color: #99f6e4 !important;
    }

    [data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] {
        color: #0f172a !important;
        border-bottom-color: #16a34a !important;
    }

    [data-testid="stRadio"] div[role="radiogroup"] > label p,
    [data-testid="stRadio"] div[role="radiogroup"] > label span,
    [data-testid="stRadio"] div[role="radiogroup"] > label div {
        color: inherit !important;
        opacity: 1 !important;
    }

    /* Hide the radio control itself while retaining accessible clickable labels */
    [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    .ai-section-caption {
        color: #64748b !important;
        font-size: .78rem;
        margin: -.1rem 0 .7rem 0;
    }

    /* Energy status cards */
    .snapshot-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: .8rem;
        margin: .6rem 0 1rem 0;
    }

    .snapshot-card {
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(15,23,42,.06);
        min-height: 108px;
    }

    .snapshot-card.good {
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
    }

    .snapshot-card.alert {
        background: #fef2f2;
        border-left: 5px solid #dc2626;
    }

    .snapshot-card.neutral {
        background: #f8fafc;
        border-left: 5px solid #64748b;
    }

    .snapshot-card.warning {
        background: #fffbeb;
        border-left: 5px solid #f59e0b;
    }

    .snapshot-title {
        color: #475569 !important;
        font-size: .82rem;
        font-weight: 700;
    }

    .snapshot-value {
        color: #0f172a !important;
        font-size: 1.35rem;
        font-weight: 800;
        margin: .2rem 0;
    }

    .snapshot-status {
        font-size: .78rem;
        font-weight: 750;
    }

    .snapshot-card.good .snapshot-status { color: #166534 !important; }
    .snapshot-card.alert .snapshot-status { color: #b91c1c !important; }
    .snapshot-card.neutral .snapshot-status { color: #475569 !important; }
    .snapshot-card.warning .snapshot-status { color: #92400e !important; }

    @media (max-width: 900px) {
        .snapshot-grid { grid-template-columns: repeat(2, 1fr); }
    }

    @media (max-width: 600px) {
        .snapshot-grid { grid-template-columns: 1fr; }
    }

    /* Strong contrast for all main action buttons */
    div.stButton > button {
        background: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 2.8rem;
    }
    div.stButton > button p,
    div.stButton > button span {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    div.stButton > button:hover {
        background: #166534 !important;
        border-color: #166534 !important;
        box-shadow: 0 6px 18px rgba(22, 101, 52, .18) !important;
    }

    /* Floating AI assistant button */
    [data-testid="stPopover"] > button {
        position: fixed !important;
        right: 24px !important;
        bottom: 24px !important;
        z-index: 999999 !important;
        border-radius: 999px !important;
        background: #0f172a !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 8px 25px rgba(15, 23, 42, .28) !important;
        padding: .7rem 1rem !important;
        font-weight: 750 !important;
    }
    [data-testid="stPopover"] > button p,
    [data-testid="stPopover"] > button span {
        color: #ffffff !important;
    }

    /* Popover chat panel */
    [data-testid="stPopoverBody"] {
        min-width: 360px !important;
        max-width: 430px !important;
    }

    /* General readable text */
    .stMarkdown, .stText, label, [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Constants / appliance presets
# -----------------------------
APPLIANCE_PRESETS = {
    "Inverter AC (1.5 ton)": 1200,
    "Non-Inverter AC (1.5 ton)": 1800,
    "Inverter AC (1 ton)": 900,
    "Refrigerator": 180,
    "Deep Freezer": 250,
    "Ceiling Fan": 75,
    "Pedestal Fan": 60,
    "LED Bulb": 12,
    "Tube Light": 40,
    "LED TV": 100,
    "Desktop Computer": 200,
    "Laptop": 60,
    "Washing Machine": 500,
    "Water Pump": 750,
    "Iron": 1000,
    "Microwave Oven": 1200,
    "Electric Kettle": 1500,
    "Geyser / Water Heater": 2000,
    "Other": 500,
}


# -----------------------------
# Utility functions
# -----------------------------
def money(value):
    return f"PKR {value:,.0f}"


def calculate_appliance_energy(watts, hours_per_day, quantity, days=30):
    return (watts * hours_per_day * quantity * days) / 1000


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""


def build_ai_client():
    key = get_api_key()
    if not key:
        return None
    return genai.Client(api_key=key)


def extract_bill_data(uploaded_file, bill_type):
    """Read a supported electricity-bill image/PDF with Gemini and return structured fields."""
    client = build_ai_client()
    if client is None:
        return None, "AI is not connected. Add GEMINI_API_KEY in Streamlit Secrets."

    try:
        uploaded_file.seek(0)
        bill_part = genai.types.Part.from_bytes(
            data=uploaded_file.getvalue(),
            mime_type=uploaded_file.type or "application/octet-stream",
        )

        prompt = f"""
You are extracting data from a Pakistani electricity bill.
This is the {bill_type} electricity bill.

Read ONLY information that is visibly present in the uploaded document.
Do not guess, infer, calculate, or invent missing values.

Return ONLY valid JSON with exactly these keys:
{{
  "bill_amount_pkr": number or null,
  "units_kwh": number or null
}}

For bill_amount_pkr, use the final/current payable bill amount or total bill amount
that best represents the amount the household pays for this bill.
For units_kwh, use the billed electricity consumption/units (kWh) for this bill.
If a value is not clearly available, return null.
"""
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[bill_part, prompt],
        )

        text = (response.text or "").strip()
        if text.startswith("```"):
            text = text.replace("
