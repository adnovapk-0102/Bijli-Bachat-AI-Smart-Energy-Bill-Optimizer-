
import json
import math
from datetime import datetime

import pandas as pd
import streamlit as st
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

    .ai-active-card {
        background: linear-gradient(135deg, #0f172a 0%, #164e63 55%, #166534 100%);
        color: #ffffff !important;
        border-radius: 16px;
        padding: .95rem 1.1rem;
        margin: .4rem 0 1rem 0;
        box-shadow: 0 8px 24px rgba(15,23,42,.14);
    }

    .ai-active-card b,
    .ai-active-card span {
        color: #ffffff !important;
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


# ============================================================
# Four AI "agent roles"
# These are prompt-based specialist modules, NOT autonomous agents.
# This keeps the project aligned with the course skills.
# ============================================================

def run_ai_analysis(user_data, role, user_question=None):
    client = build_ai_client()
    if client is None:
        return (
            "AI is not connected yet. Add GEMINI_API_KEY in Streamlit Secrets "
            "to activate the AI analysis."
        )

    role_instructions = {
        "Understanding Agent": """
You are the Understanding Specialist for Bijli Bachat AI.
Interpret the user's household, electricity-bill and appliance information.
Identify the user's main energy problem and summarize it in simple language.
Do not invent missing data.
""",
        "Energy Analysis Agent": """
You are the Energy Analysis Specialist for Bijli Bachat AI.
Analyze appliance-level energy consumption, estimated monthly units,
estimated costs, unusual consumption patterns, and major energy drivers.
Prioritize measurable findings. Do not invent meter readings.
""",
        "Saving Strategy Agent": """
You are the Saving Strategy Specialist for Bijli Bachat AI.
Create a practical Pakistan-household energy-saving plan.
Prioritize high-impact, low-cost actions first.
Give estimated savings only when the supplied data supports an estimate,
and label estimates clearly.
""",
        "Monitoring & Alerting Agent": """
You are the Monitoring & Alerting Specialist for Bijli Bachat AI.
Identify useful thresholds, warning signs and monthly checks.
Suggest what the household should monitor next month.
Do not claim to monitor live electricity data; this MVP only uses user-entered data.
""",
        "General Energy Assistant": """
You are a helpful energy-efficiency advisor.
Answer the user's question using only the supplied household data.
Be concise, practical and honest about estimates and uncertainty.
""",
    }

    prompt = f"""
PROJECT: Bijli Bachat AI — Smart Energy & Bill Optimizer
COUNTRY CONTEXT: Pakistan
IMPORTANT: This is an educational/hackathon energy-estimation application.
Never claim to have access to a live smart meter unless the user supplied such data.
Never fabricate tariff rates, meter readings, appliance ratings or savings.

SPECIALIST ROLE:
{role_instructions.get(role, role_instructions["General Energy Assistant"])}

HOUSEHOLD DATA:
{json.dumps(user_data, indent=2, ensure_ascii=False)}

USER QUESTION:
{user_question or "Provide the requested specialist analysis."}

OUTPUT RULES:
- Use clear headings.
- Give actionable bullet points.
- Distinguish calculated values from AI estimates.
- If important information is missing, say exactly what is missing.
- Keep the answer suitable for a general Pakistani household.
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return response.text or "No AI response was returned."
    except Exception as exc:
        return f"AI request failed: {exc}"


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="badge">AI-POWERED ENERGY EFFICIENCY • HACKATHON MVP</div>
    <h1>⚡ Bijli Bachat AI</h1>
    <p>Smart Energy & Bill Optimizer — understand your electricity use, find energy-heavy appliances, and build a practical savings plan.</p>
</div>
""", unsafe_allow_html=True)

st.caption(
    "A decision-support tool: calculations are based on the information you enter, "
    "while AI provides explanations and recommendations."
)

# -----------------------------
# Sidebar inputs
# -----------------------------
with st.sidebar:
    st.markdown("## 🏠 Household Profile")
    household_size = st.number_input(
        "People in household", min_value=1, max_value=30, value=4, step=1
    )
    city = st.text_input("City", value="Multan")
    monthly_bill = st.number_input(
        "Latest monthly electricity bill (PKR)",
        min_value=0.0,
        value=25000.0,
        step=500.0,
    )
    previous_bill = st.number_input(
        "Previous month's electricity bill (optional)",
        min_value=0.0,
        value=0.0,
        step=500.0,
        help="Enter the previous bill amount to enable bill-over-bill alerts.",
    )
    monthly_units = st.number_input(
        "Latest monthly units (kWh)",
        min_value=0.0,
        value=300.0,
        step=10.0,
        help="Enter the units/kWh shown on your electricity bill. This is more useful than bill amount alone.",
    )
    previous_units = st.number_input(
        "Previous month's units (optional)",
        min_value=0.0,
        value=0.0,
        step=10.0,
    )
    tariff = st.number_input(
        "Approx. cost per unit (PKR)",
        min_value=0.0,
        value=monthly_bill / monthly_units if monthly_units else 0.0,
        step=1.0,
        help="This is an approximation for the calculator. Actual Pakistan bills can include taxes, fixed charges and slab effects.",
    )

    st.markdown("---")
    st.markdown("### Appliance Setup")
    st.caption("Add the appliances you want the app to analyze.")

    appliance_count = st.number_input(
        "Number of appliances",
        min_value=1,
        max_value=25,
        value=5,
        step=1,
    )

    appliances = []
    for i in range(int(appliance_count)):
        with st.expander(f"Appliance {i+1}", expanded=(i < 2)):
            appliance_type = st.selectbox(
                "Appliance",
                list(APPLIANCE_PRESETS.keys()),
                key=f"type_{i}",
            )
            default_watts = APPLIANCE_PRESETS[appliance_type]
            watts = st.number_input(
                "Power (watts)",
                min_value=1.0,
                value=float(default_watts),
                step=10.0,
                key=f"watts_{i}",
            )
            hours = st.number_input(
                "Hours used per day",
                min_value=0.0,
                max_value=24.0,
                value=4.0,
                step=0.5,
                key=f"hours_{i}",
            )
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=20,
                value=1,
                step=1,
                key=f"qty_{i}",
            )
            appliances.append(
                {
                    "name": appliance_type,
                    "watts": watts,
                    "hours_per_day": hours,
                    "quantity": quantity,
                }
            )

    analyze = st.button(
        "⚡ Analyze My Energy",
        type="primary",
        use_container_width=True,
    )

# -----------------------------
# Calculations
# -----------------------------
rows = []
for a in appliances:
    kwh = calculate_appliance_energy(
        a["watts"], a["hours_per_day"], a["quantity"]
    )
    cost = kwh * tariff
    rows.append(
        {
            "Appliance": a["name"],
            "Power (W)": a["watts"],
            "Hours/day": a["hours_per_day"],
            "Qty": a["quantity"],
            "Monthly kWh": kwh,
            "Estimated Cost": cost,
        }
    )

df = pd.DataFrame(rows)
total_appliance_kwh = float(df["Monthly kWh"].sum()) if not df.empty else 0.0
estimated_appliance_cost = total_appliance_kwh * tariff

if monthly_units > 0:
    appliance_share = min((total_appliance_kwh / monthly_units) * 100, 999)
else:
    appliance_share = 0.0

if previous_units > 0 and monthly_units > 0:
    units_change_pct = ((monthly_units - previous_units) / previous_units) * 100
else:
    units_change_pct = None

if previous_bill > 0 and monthly_bill > 0:
    bill_change_pct = ((monthly_bill - previous_bill) / previous_bill) * 100
else:
    bill_change_pct = None

# Backward-compatible name used by older parts of the app.
change_pct = units_change_pct

# CO2 estimate: clearly labelled as an approximate scenario assumption.
# Users can change this later when a verified local grid factor is available.
GRID_CO2_FACTOR = 0.40  # kg CO2e per kWh; illustrative estimate, not a Pakistan official factor.
estimated_co2 = monthly_units * GRID_CO2_FACTOR

# Potential saving scenarios are simple planning estimates, not guaranteed savings.
conservative_saving = estimated_appliance_cost * 0.10
strong_saving = estimated_appliance_cost * 0.20

# -----------------------------
# Main dashboard
# -----------------------------
if analyze or "analyzed" not in st.session_state:
    st.session_state["analyzed"] = True

st.markdown('<div class="section-title">📊 Your Energy Snapshot</div>', unsafe_allow_html=True)

# Status logic is intentionally conservative:
# green = improvement, red = material increase, amber = needs attention,
# neutral = insufficient comparison data.
def status_card(title, value, status, status_text):
    return f"""
    <div class="snapshot-card {status}">
        <div class="snapshot-title">{title}</div>
        <div class="snapshot-value">{value}</div>
        <div class="snapshot-status">{status_text}</div>
    </div>
    """

if units_change_pct is None:
    units_status, units_text = "neutral", "No previous units entered"
elif units_change_pct <= -5:
    units_status, units_text = "good", f"↓ {abs(units_change_pct):.1f}% vs previous month"
elif units_change_pct >= 10:
    units_status, units_text = "alert", f"↑ {units_change_pct:.1f}% — energy alert"
else:
    units_status, units_text = "warning", f"↑ {units_change_pct:.1f}% — monitor usage"

if bill_change_pct is None:
    bill_status, bill_text = "neutral", "No previous bill entered"
elif bill_change_pct <= -5:
    bill_status, bill_text = "good", f"↓ {abs(bill_change_pct):.1f}% vs previous bill"
elif bill_change_pct >= 10:
    bill_status, bill_text = "alert", f"↑ {bill_change_pct:.1f}% — bill alert"
else:
    bill_status, bill_text = "warning", f"↑ {bill_change_pct:.1f}% — monitor bill"

if total_appliance_kwh <= monthly_units * 0.75:
    appliance_status, appliance_text = "good", "Appliance estimate is within bill units"
elif monthly_units > 0 and total_appliance_kwh > monthly_units * 1.05:
    appliance_status, appliance_text = "alert", "Entered appliance use exceeds bill units"
else:
    appliance_status, appliance_text = "warning", "Review appliance usage estimate"

if units_change_pct is None and bill_change_pct is None:
    trend_status, trend_text = "neutral", "Add previous bill + units for alerts"
elif (units_change_pct is not None and units_change_pct >= 10) or (
    bill_change_pct is not None and bill_change_pct >= 10
):
    trend_status, trend_text = "alert", "High-priority review recommended"
elif (units_change_pct is not None and units_change_pct <= -5) and (
    bill_change_pct is None or bill_change_pct <= -5
):
    trend_status, trend_text = "good", "Your overall trend is improving"
else:
    trend_status, trend_text = "warning", "Monitor next month's numbers"

st.markdown(
    f"""
    <div class="snapshot-grid">
        {status_card("Monthly Units", f"{monthly_units:,.0f} kWh", units_status, units_text)}
        {status_card("Latest Bill", money(monthly_bill), bill_status, bill_text)}
        {status_card("Appliance Estimate", f"{total_appliance_kwh:,.0f} kWh", appliance_status, appliance_text)}
        {status_card("Energy Trend", f"{units_change_pct:+.1f}%" if units_change_pct is not None else "N/A", trend_status, trend_text)}
    </div>
    """,
    unsafe_allow_html=True,
)

# A single, easy-to-read alert banner for the judge/demo.
if bill_change_pct is not None and bill_change_pct >= 10 and units_change_pct is not None and units_change_pct <= 0:
    st.markdown(
        f'<div class="warning-card">⚠️ <b>Bill Alert:</b> your bill increased by <b>{bill_change_pct:.1f}%</b> while your units did not increase. This can happen because of tariff slabs, taxes, fixed charges or other bill components, so review the bill details before blaming appliance usage.</div>',
        unsafe_allow_html=True,
    )
elif (bill_change_pct is not None and bill_change_pct >= 10) or (
    units_change_pct is not None and units_change_pct >= 10
):
    reasons = []
    if bill_change_pct is not None and bill_change_pct >= 10:
        reasons.append(f"bill is up {bill_change_pct:.1f}%")
    if units_change_pct is not None and units_change_pct >= 10:
        reasons.append(f"units are up {units_change_pct:.1f}%")
    st.markdown(
        f'<div class="warning-card">🚨 <b>Energy Alert:</b> {" and ".join(reasons)} compared with the previous month. Check the appliance audit below for the likely high-consumption drivers.</div>',
        unsafe_allow_html=True,
    )
elif (bill_change_pct is not None and bill_change_pct <= -5) and (
    units_change_pct is None or units_change_pct <= -5
):
    st.markdown(
        f'<div class="success-card">✅ <b>Good news:</b> your bill has reduced by <b>{abs(bill_change_pct):.1f}%</b> compared with the previous bill, and your energy trend is also improving.</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

left, right = st.columns([1.15, 0.85])

with left:
    st.markdown("### 🔌 Appliance Energy Audit")
    if not df.empty:
        display_df = df.copy()
        display_df["Monthly kWh"] = display_df["Monthly kWh"].round(1)
        display_df["Estimated Cost"] = display_df["Estimated Cost"].round(0)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        chart_df = df[["Appliance", "Monthly kWh"]].copy()
        chart_df = chart_df.sort_values("Monthly kWh", ascending=True)
        st.bar_chart(chart_df.set_index("Appliance"))

with right:
    st.markdown("### 🎯 Highest Energy Consumers")
    if not df.empty:
        top = df.sort_values("Monthly kWh", ascending=False).head(5)
        for _, row in top.iterrows():
            share = (
                (row["Monthly kWh"] / total_appliance_kwh * 100)
                if total_appliance_kwh else 0
            )
            st.markdown(
                f"""
                <div class="card">
                    <b>{row['Appliance']}</b><br>
                    <span class="small-muted">
                    {row['Monthly kWh']:.1f} kWh/month • {money(row['Estimated Cost'])}
                    • {share:.1f}% of entered appliance consumption
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("---")

# -----------------------------
# Savings simulator
# -----------------------------
st.markdown('<div class="section-title">💰 Savings Simulator</div>', unsafe_allow_html=True)
st.caption("Use the slider to model a reduction in the energy use of the appliances entered above.")

saving_pct = st.slider("Target reduction in appliance usage", 0, 40, 15, 5)
simulated_kwh_saved = total_appliance_kwh * saving_pct / 100
simulated_monthly_saving = simulated_kwh_saved * tariff
simulated_yearly_saving = simulated_monthly_saving * 12

s1, s2, s3 = st.columns(3)
s1.metric("Potential Units Saved", f"{simulated_kwh_saved:,.1f} kWh/month")
s2.metric("Potential Monthly Saving", money(simulated_monthly_saving))
s3.metric("Potential Yearly Saving", money(simulated_yearly_saving))

st.markdown("---")

# -----------------------------
# Carbon footprint
# -----------------------------
st.markdown('<div class="section-title">🌱 Carbon Footprint Estimate</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="carbon-card">
        <div class="carbon-label">Estimated Carbon Footprint</div>
        <div class="carbon-value">{estimated_co2:,.1f} kg CO₂e/month</div>
        <div class="carbon-note">
            Planning estimate using an illustrative grid factor of
            {GRID_CO2_FACTOR:.2f} kg CO₂e/kWh. This is not an official
            Pakistan grid-emissions factor.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# AI specialist analysis
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">🤖 Personalized AI Energy Audit</div>', unsafe_allow_html=True)

user_data = {
    "city": city,
    "household_size": household_size,
    "monthly_bill_pkr": monthly_bill,
    "previous_month_bill_pkr": previous_bill,
    "monthly_units_kwh": monthly_units,
    "previous_month_units_kwh": previous_units,
    "approx_cost_per_unit_pkr": tariff,
    "estimated_appliance_kwh": total_appliance_kwh,
    "estimated_appliance_cost_pkr": estimated_appliance_cost,
    "estimated_monthly_co2_kg": estimated_co2,
    "appliances": rows,
}

# Native Streamlit tabs were intentionally replaced with four explicit
# navigation buttons. This avoids browser/theme-specific tab text contrast
# issues where labels could appear invisible until clicked.
if "active_ai_section" not in st.session_state:
    st.session_state["active_ai_section"] = 0

ai_names = [
    "Understanding",
    "Energy Analysis",
    "Saving Strategy",
    "Monitoring & Alerts",
]
ai_roles = [
    "Understanding Agent",
    "Energy Analysis Agent",
    "Saving Strategy Agent",
    "Monitoring & Alerting Agent",
]

nav_cols = st.columns(4)
for idx, (col, name) in enumerate(zip(nav_cols, ai_names)):
    with col:
        if st.button(
            name,
            key=f"ai_nav_{idx}",
            use_container_width=True,
            type="primary" if st.session_state["active_ai_section"] == idx else "secondary",
        ):
            st.session_state["active_ai_section"] = idx
            st.rerun()

active_idx = st.session_state["active_ai_section"]
active_name = ai_names[active_idx]
active_role = ai_roles[active_idx]

st.markdown(
    f'<div class="ai-active-card"><b>{active_name}</b><br><span>AI specialist module ready — generate a focused analysis from your household data.</span></div>',
    unsafe_allow_html=True,
)

if st.button(
    f"Generate {active_name} Analysis",
    key=f"generate_active_ai_{active_idx}",
    use_container_width=True,
):
    with st.spinner(f"{active_role} is analyzing your data..."):
        result = run_ai_analysis(user_data, active_role)
    st.markdown(result)

# -----------------------------
# Floating Ask My Energy AI
# -----------------------------
# The assistant is intentionally a floating popover rather than a full-width
# dashboard section, keeping the main dashboard clean for demos and judges.
with st.popover("🤖 Ask Energy AI"):
    st.markdown("### 💬 Energy Assistant")
    st.caption("Ask anything about your household energy data. You can ask in English, Urdu, or Roman Urdu.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history[-6:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.text_area(
        "Your question",
        placeholder="Example: Mera bill itna high kyun hai? AC ka usage kaise kam karun?",
        key="floating_energy_question",
        height=90,
    )

    if st.button("Send to Energy AI", key="floating_send", use_container_width=True):
        if question.strip():
            st.session_state.chat_history.append(
                {"role": "user", "content": question.strip()}
            )
            with st.spinner("Energy AI is analyzing your data..."):
                answer = run_ai_analysis(
                    user_data,
                    "General Energy Assistant",
                    question.strip(),
                )
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )
            st.rerun()
        else:
            st.warning("Please enter a question first.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown('<div style="color:#475569;font-size:.85rem;text-align:center;padding:1rem 0;">Bijli Bachat AI • Environment & Sustainability — Tech for Good • Hackathon MVP • Calculations are estimates based on user-provided data.</div>', unsafe_allow_html=True)
