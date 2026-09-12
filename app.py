
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
Use the appliance recommendations, bill trend, predicted bill and available data.
Prioritize high-impact, low-cost actions first.
Give estimated savings only when the supplied data supports an estimate,
and label estimates clearly.
""",
        "Monitoring & Alerting Agent": """
You are the Monitoring & Alerting Specialist for Bijli Bachat AI.
Identify useful thresholds, warning signs, bill/unit trends and next-month checks.
Explain whether a rising bill appears related to usage or may involve tariff/charges.
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
    <p>Smart Energy & Bill Optimizer — find energy-heavy appliances, get practical recommendations, and build a personalized savings plan.</p>
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

    st.markdown("### 🧾 Electricity Bill (Optional)")
    st.caption("Upload a bill photo or PDF for reference while preparing your energy plan.")
    bill_file = st.file_uploader(
        "Upload bill photo or PDF",
        type=["png", "jpg", "jpeg", "pdf"],
        key="bill_upload",
    )
    if bill_file is not None:
        st.success(f"Bill attached: {bill_file.name}")

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
# Dashboard helper
# -----------------------------
def status_card(title, value, status, message):
    return f"""
    <div class="snapshot-card {status}">
        <div class="snapshot-title">{title}</div>
        <div class="snapshot-value">{value}</div>
        <div class="snapshot-status">{message}</div>
    </div>
    """


# -----------------------------
# Feature helpers
# -----------------------------
def predict_next_bill(current_bill, previous_bill, current_units, previous_units):
    """Simple transparent estimate; not a guaranteed utility-bill prediction."""
    if current_bill <= 0 or current_units <= 0:
        return None, None

    if previous_bill > 0 and previous_units > 0:
        avg_bill = (current_bill + previous_bill) / 2
        avg_units = (current_units + previous_units) / 2
        # A weighted estimate gives the latest month slightly more importance.
        predicted_bill = (current_bill * 0.65) + (avg_bill * 0.35)
        predicted_units = (current_units * 0.65) + (avg_units * 0.35)
    else:
        predicted_bill = current_bill
        predicted_units = current_units

    return predicted_bill, predicted_units


def appliance_recommendations(df, tariff):
    """Generate practical, deterministic recommendations from appliance data."""
    recommendations = []
    if df.empty:
        return recommendations

    ranked = df.sort_values("Monthly kWh", ascending=False).head(5)

    for _, row in ranked.iterrows():
        name = row["Appliance"]
        kwh = float(row["Monthly kWh"])
        hours = float(row["Hours/day"])
        qty = int(row["Qty"])
        watts = float(row["Power (W)"])

        if hours <= 0 or kwh <= 0:
            continue

        reduction_hours = min(2.0, max(0.5, hours * 0.20))
        saving_kwh = calculate_appliance_energy(
            watts, reduction_hours, qty
        )
        saving_cost = saving_kwh * tariff

        if "AC" in name:
            action = f"Reduce AC usage by about {reduction_hours:.1f} hour/day where practical and use a moderate thermostat setting."
        elif "Water Pump" in name:
            action = "Avoid unnecessary pump cycles and check for leaks or an automatic shut-off."
        elif "Geyser" in name or "Water Heater" in name:
            action = "Reduce unnecessary heating time and avoid keeping the heater on continuously."
        elif "Refrigerator" in name or "Freezer" in name:
            action = "Keep the door closed, maintain good ventilation around the unit, and check the door seal."
        elif "Iron" in name or "Kettle" in name or "Microwave" in name:
            action = "Use in planned batches instead of repeated short cycles."
        elif "Fan" in name:
            action = "Use the fan only where needed and switch it off when the room is unoccupied."
        elif "Light" in name or "Bulb" in name:
            action = "Switch off unused lights and prefer efficient LED lighting."
        else:
            action = "Reduce unnecessary runtime and switch the appliance off instead of leaving it on standby."

        recommendations.append({
            "appliance": name,
            "current_kwh": kwh,
            "estimated_saving_kwh": saving_kwh,
            "estimated_saving_pkr": saving_cost,
            "action": action,
        })

    return recommendations


def make_plan(recommendations, days=7):
    """Create a useful non-AI fallback plan."""
    if not recommendations:
        return []

    tasks = []
    for item in recommendations:
        tasks.append(
            f"Review {item['appliance']} usage and aim for the suggested reduction; "
            f"potential saving is about {item['estimated_saving_pkr']:,.0f} PKR/month."
        )

    if days == 7:
        return [
            "Day 1 — Identify and reduce the highest-consumption appliance.",
            "Day 2 — Switch off unnecessary lights, fans and standby loads.",
            "Day 3 — Review AC/fan usage and avoid unnecessary runtime.",
            "Day 4 — Check refrigerator/freezer ventilation and door seals.",
            "Day 5 — Review water-pump/geyser usage and avoid unnecessary cycles.",
            "Day 6 — Repeat the top appliance action and compare your daily routine.",
            "Day 7 — Record your bill/units trend and set next week's target.",
        ]
    return [
        "Week 1 — Fix the biggest avoidable usage source and establish a baseline.",
        "Week 2 — Optimize AC, fans, lights and standby habits.",
        "Week 3 — Review refrigerator, pump, geyser and other high-load appliances.",
        "Week 4 — Compare units and bill, keep successful habits and set the next target.",
    ]


def bill_analysis_status(current, previous, label):
    if previous <= 0:
        return "neutral", f"No previous {label.lower()} entered"
    pct = ((current - previous) / previous) * 100
    if pct <= -5:
        return "good", f"↓ {abs(pct):.1f}% vs previous month"
    if pct >= 10:
        return "alert", f"↑ {pct:.1f}% — investigate"
    return "warning", f"{pct:+.1f}% vs previous month"




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

# Feature 4 — Bill prediction
predicted_bill, predicted_units = predict_next_bill(
    monthly_bill, previous_bill, monthly_units, previous_units
)

# Feature 2 — Smart appliance recommendations
recommendations = appliance_recommendations(df, tariff)
total_recommended_saving = sum(x["estimated_saving_pkr"] for x in recommendations)

# Feature 3 — Personalized saving plans
plan_7_day = make_plan(recommendations, 7)
plan_30_day = make_plan(recommendations, 30)


# -----------------------------
# Main dashboard
# -----------------------------
if analyze or "analyzed" not in st.session_state:
    st.session_state["analyzed"] = True

st.markdown('<div class="section-title">📊 Your Energy Snapshot</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
s1.metric("Latest Bill", money(monthly_bill))
s2.metric("Monthly Units", f"{monthly_units:,.0f} kWh")
s3.metric("Appliance Estimate", f"{total_appliance_kwh:,.0f} kWh")
s4.metric("Predicted Next Bill", money(predicted_bill) if predicted_bill is not None else "N/A")

if units_change_pct is not None:
    if units_change_pct > 10:
        st.markdown(
            f'<div class="warning-card">⚠️ Your entered unit consumption is about <b>{units_change_pct:.1f}% higher</b> than last month. Review the highest-consuming appliances first.</div>',
            unsafe_allow_html=True,
        )
    elif units_change_pct < -5:
        st.markdown(
            f'<div class="success-card">✅ Great: your entered unit consumption is about <b>{abs(units_change_pct):.1f}% lower</b> than last month.</div>',
            unsafe_allow_html=True,
        )

# -----------------------------
# Appliance diagnosis
# -----------------------------
left, right = st.columns([1.15, 0.85])

with left:
    st.markdown("### 🔌 Appliance Energy Audit")
    if not df.empty:
        display_df = df.copy()
        display_df["Monthly kWh"] = display_df["Monthly kWh"].round(1)
        display_df["Estimated Cost"] = display_df["Estimated Cost"].round(0)
        st.dataframe(display_df, use_container_width=True, hide_index=True)


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
# Feature 2 — Smart Appliance Recommendations
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">🏠 Smart Appliance Recommendations</div>', unsafe_allow_html=True)
st.caption("Recommendations are prioritized from the appliances with the highest estimated monthly consumption.")

if recommendations:
    for idx, item in enumerate(recommendations[:3], start=1):
        st.markdown(
            f"""
            <div class="card">
                <b>{idx}. {item['appliance']}</b><br>
                <span class="small-muted">{item['current_kwh']:.1f} kWh/month • estimated saving potential: {item['estimated_saving_kwh']:.1f} kWh/month ({money(item['estimated_saving_pkr'])})</span>
                <br><span style="color:#334155;">{item['action']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("Add appliance usage data to generate recommendations.")

# -----------------------------
# Feature 3 — Personalized 7/30-Day Saving Plan
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">📅 Personalized Saving Plan</div>', unsafe_allow_html=True)

plan_choice = st.radio(
    "Plan duration",
    ["7-Day Quick Plan", "30-Day Sustainable Plan"],
    horizontal=True,
    label_visibility="collapsed",
    key="plan_duration",
)

selected_plan = plan_7_day if plan_choice == "7-Day Quick Plan" else plan_30_day

if selected_plan:
    for task in selected_plan:
        st.markdown(f"• {task}")
    st.markdown(
        f'<div class="success-card">🎯 Estimated opportunity from your highest-use appliances: <b>{money(total_recommended_saving)}/month</b>. This is an estimate, not a guaranteed saving.</div>',
        unsafe_allow_html=True,
    )

    plan_text = "Bijli Bachat AI — Personalized Saving Plan\n" + "=" * 52 + "\n"
    plan_text += f"Plan: {plan_choice}\n"
    plan_text += f"Household: {int(household_size)} people | City: {city}\n"
    plan_text += f"Latest bill: {money(monthly_bill)} | Units: {monthly_units:,.0f} kWh\n\n"
    plan_text += "ACTION PLAN\n"
    for idx, task in enumerate(selected_plan, start=1):
        plan_text += f"{idx}. {task}\n"
    plan_text += f"\nEstimated saving opportunity: {money(total_recommended_saving)}/month\n"
    plan_text += "Note: Savings are estimates, not guaranteed.\n"

    st.download_button(
        "⬇️ Download Saving Plan",
        data=plan_text,
        file_name="bijli_bachat_personalized_saving_plan.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.info("Add appliance usage data to generate a personalized plan.")

# -----------------------------
# Feature 4 — Bill Prediction
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">🔮 Next Bill Prediction</div>', unsafe_allow_html=True)
st.caption("A transparent estimate based on the bill and units you entered. It is not an official utility forecast.")

if predicted_bill is not None:
    p1, p2, p3 = st.columns(3)
    p1.metric("Predicted Next Bill", money(predicted_bill))
    p2.metric("Predicted Units", f"{predicted_units:,.0f} kWh")
    if monthly_bill > 0:
        expected_change = ((predicted_bill - monthly_bill) / monthly_bill) * 100
        p3.metric("Expected Bill Change", f"{expected_change:+.1f}%")
    else:
        p3.metric("Expected Bill Change", "N/A")
else:
    st.info("Enter your current bill and units to see a prediction.")

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
# -----------------------------
# Feature 6 — Professional Judge Dashboard
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">🏆 Judge Dashboard</div>', unsafe_allow_html=True)

potential_saving_pct = (
    min(100, (total_recommended_saving / monthly_bill) * 100)
    if monthly_bill > 0 else 0
)

score = 60
if bill_pct is not None and bill_pct <= -5:
    score += 12
elif bill_pct is not None and bill_pct >= 10:
    score -= 10

if units_pct is not None and units_pct <= -5:
    score += 12
elif units_pct is not None and units_pct >= 10:
    score -= 10

if total_appliance_kwh <= monthly_units * 0.75:
    score += 8
elif monthly_units > 0 and total_appliance_kwh > monthly_units * 1.05:
    score -= 8

score = max(0, min(100, score))

score_label = "Excellent" if score >= 80 else ("Good" if score >= 65 else "Needs Improvement")

j1, j2, j3, j4 = st.columns(4)
j1.metric("Energy Efficiency Score", f"{score}/100", score_label)
j2.metric("Potential Monthly Saving", money(total_recommended_saving))
j3.metric("CO₂ Footprint", f"{estimated_co2:,.0f} kg/month")
j4.metric("Predicted Bill", money(predicted_bill) if predicted_bill is not None else "N/A")

if not df.empty:
    top_appliance = df.sort_values("Monthly kWh", ascending=False).iloc[0]
    st.markdown(
        f"""
        <div class="card">
            <b>Top Energy Driver:</b> {top_appliance['Appliance']}
            • {top_appliance['Monthly kWh']:.1f} kWh/month
            • approximately {money(top_appliance['Estimated Cost'])}
            <br><span class="small-muted">
            The dashboard prioritizes this appliance because it has the highest estimated monthly consumption among the appliances entered.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="small-muted">Judge view: household data → appliance diagnosis → personalized action plan → next-bill estimate. All calculations are transparent estimates based on user-entered data.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# AI specialist analysis
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">🤖 Personalized AI Energy Audit</div>', unsafe_allow_html=True)

user_data = {
    "city": city,
    "bill_file_attached": bool(bill_file),
    "bill_file_name": bill_file.name if bill_file else None,
    "household_size": household_size,
    "monthly_bill_pkr": monthly_bill,
    "previous_month_bill_pkr": previous_bill,
    "monthly_units_kwh": monthly_units,
    "previous_month_units_kwh": previous_units,
    "approx_cost_per_unit_pkr": tariff,
    "estimated_appliance_kwh": total_appliance_kwh,
    "estimated_appliance_cost_pkr": estimated_appliance_cost,
    "estimated_monthly_co2_kg": estimated_co2,
    "predicted_next_bill_pkr": predicted_bill,
    "predicted_next_units_kwh": predicted_units,
    "recommended_monthly_saving_pkr": total_recommended_saving,
    "appliances": rows,
}

# Compact text navigation. We use a radio control styled as simple text tabs
# instead of large buttons, avoiding the invisible-label issue from the old tabs.
if "active_ai_section" not in st.session_state:
    st.session_state["active_ai_section"] = 0

ai_names = [
    "🧠 Understanding",
    "⚡ Energy Analysis",
    "💡 Saving Strategy",
    "🔔 Monitoring & Alerts",
]
ai_roles = [
    "Understanding Agent",
    "Energy Analysis Agent",
    "Saving Strategy Agent",
    "Monitoring & Alerting Agent",
]

selected_name = st.radio(
    "AI audit modules",
    ai_names,
    index=st.session_state["active_ai_section"],
    horizontal=True,
    label_visibility="collapsed",
    key="ai_section_radio",
)
st.session_state["active_ai_section"] = ai_names.index(selected_name)
active_idx = st.session_state["active_ai_section"]
active_name = ai_names[active_idx].split(" ", 1)[-1]
active_role = ai_roles[active_idx]

st.markdown(
    f'<div class="ai-section-caption">{active_name} · AI specialist analysis based on your household data</div>',
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
