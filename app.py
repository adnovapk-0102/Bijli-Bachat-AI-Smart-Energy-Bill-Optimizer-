import json
from datetime import datetime

import pandas as pd
import streamlit as st
from google import genai


# ============================================================
# BIJLI BACHAT AI
# Smart Energy & Bill Optimizer
# Environment & Sustainability — Tech for Good
# Hackathon MVP
# ============================================================

st.set_page_config(
    page_title="Bijli Bachat AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL THEME-SAFE CSS
# Works with both LIGHT and DARK Streamlit themes
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL STREAMLIT THEME VARIABLES
   ========================================================= */

:root {
    --bb-text: var(--text-color, #0f172a);
    --bb-bg: var(--background-color, #ffffff);
    --bb-secondary-bg: var(--secondary-background-color, #f8fafc);
    --bb-border: rgba(148, 163, 184, 0.30);
}


/* =========================================================
   MAIN APP BACKGROUND
   ========================================================= */

.stApp {
    background:
        linear-gradient(
            135deg,
            rgba(248,250,252,0.96) 0%,
            rgba(240,253,244,0.96) 100%
        );
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #0f172a !important;
}

[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {
    color: #0f172a !important;
    background: #ffffff !important;
}

[data-testid="stSidebar"] input::placeholder,
[data-testid="stSidebar"] textarea::placeholder {
    color: #64748b !important;
}


/* =========================================================
   HERO
   ========================================================= */

.bb-hero {
    padding: 2rem 2.2rem;
    border-radius: 24px;
    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #164e63 55%,
            #166534 100%
        );
    color: #ffffff !important;
    margin-bottom: 1.2rem;
    box-shadow: 0 12px 35px rgba(15, 23, 42, 0.18);
}

.bb-hero h1 {
    margin: 0;
    color: #ffffff !important;
    font-size: 2.5rem;
    font-weight: 800;
}

.bb-hero p {
    margin: .55rem 0 0;
    color: #dbeafe !important;
    font-size: 1.05rem;
    line-height: 1.55;
}

.bb-hero-badge {
    display: inline-block;
    padding: .35rem .75rem;
    border-radius: 999px;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.20);
    color: #dcfce7 !important;
    font-size: .75rem;
    font-weight: 800;
    letter-spacing: .04em;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.bb-section-title {
    color: #0f172a !important;
    font-size: 1.35rem;
    font-weight: 800;
    margin-top: .7rem;
    margin-bottom: .4rem;
}

.bb-section-subtitle {
    color: #475569 !important;
    font-size: .88rem;
    line-height: 1.5;
}


/* =========================================================
   CARDS
   ========================================================= */

.bb-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 18px;
    padding: 1.1rem;
    box-shadow: 0 6px 20px rgba(15, 23, 42, .06);
    margin-bottom: .8rem;
    color: #0f172a !important;
}

.bb-card * {
    color: #0f172a !important;
}

.bb-muted {
    color: #475569 !important;
    font-size: .88rem;
}


/* =========================================================
   BADGES
   ========================================================= */

.bb-badge {
    display: inline-block;
    padding: .28rem .7rem;
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 800;
    background: #dcfce7 !important;
    color: #166534 !important;
}


/* =========================================================
   CARBON CARD
   ========================================================= */

.bb-carbon-card {
    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #164e63 55%,
            #166534 100%
        ) !important;
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 18px;
    padding: 1.25rem 1.4rem;
    color: #ffffff !important;
    box-shadow: 0 10px 28px rgba(15, 23, 42, .16);
    margin: .7rem 0 1rem 0;
}

.bb-carbon-card * {
    color: #ffffff !important;
}

.bb-carbon-label {
    color: #d1fae5 !important;
    font-size: .95rem;
    font-weight: 800;
}

.bb-carbon-value {
    color: #ffffff !important;
    font-size: 1.55rem;
    font-weight: 850;
    margin: .25rem 0 .35rem 0;
}

.bb-carbon-note {
    color: #dbeafe !important;
    font-size: .86rem;
    line-height: 1.45;
}


/* =========================================================
   SNAPSHOT GRID
   ========================================================= */

.bb-snapshot-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: .8rem;
    margin: .6rem 0 1rem 0;
}

.bb-snapshot-card {
    border-radius: 16px;
    padding: 1rem;
    min-height: 108px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(15,23,42,.06);
}

.bb-snapshot-card.good {
    background: #f0fdf4 !important;
    border-left: 5px solid #16a34a !important;
}

.bb-snapshot-card.alert {
    background: #fef2f2 !important;
    border-left: 5px solid #dc2626 !important;
}

.bb-snapshot-card.warning {
    background: #fffbeb !important;
    border-left: 5px solid #f59e0b !important;
}

.bb-snapshot-card.neutral {
    background: #f8fafc !important;
    border-left: 5px solid #64748b !important;
}

.bb-snapshot-title {
    color: #475569 !important;
    font-size: .82rem;
    font-weight: 750;
}

.bb-snapshot-value {
    color: #0f172a !important;
    font-size: 1.35rem;
    font-weight: 850;
    margin: .2rem 0;
}

.bb-snapshot-status {
    font-size: .78rem;
    font-weight: 800;
}

.bb-snapshot-card.good .bb-snapshot-status {
    color: #166534 !important;
}

.bb-snapshot-card.alert .bb-snapshot-status {
    color: #b91c1c !important;
}

.bb-snapshot-card.warning .bb-snapshot-status {
    color: #92400e !important;
}

.bb-snapshot-card.neutral .bb-snapshot-status {
    color: #475569 !important;
}


/* =========================================================
   ALERT CARDS
   ========================================================= */

.bb-warning {
    border-left: 5px solid #f59e0b !important;
    background: #fffbeb !important;
    padding: .9rem 1rem;
    border-radius: 12px;
    color: #78350f !important;
    margin-bottom: .8rem;
}

.bb-warning * {
    color: #78350f !important;
}

.bb-danger {
    border-left: 5px solid #dc2626 !important;
    background: #fef2f2 !important;
    padding: .9rem 1rem;
    border-radius: 12px;
    color: #7f1d1d !important;
    margin-bottom: .8rem;
}

.bb-danger * {
    color: #7f1d1d !important;
}

.bb-success {
    border-left: 5px solid #16a34a !important;
    background: #f0fdf4 !important;
    padding: .9rem 1rem;
    border-radius: 12px;
    color: #14532d !important;
    margin-bottom: .8rem;
}

.bb-success * {
    color: #14532d !important;
}


/* =========================================================
   AI NAVIGATION
   IMPORTANT: TEXT VISIBILITY FIX
   ========================================================= */

.bb-ai-nav-label {
    color: #0f172a !important;
    font-size: .82rem;
    font-weight: 800;
    margin-bottom: .3rem;
}


/*
   Remove the default visible radio circle.
   Keep text visible.
*/

[data-testid="stRadio"] {
    margin-top: .1rem !important;
    margin-bottom: .25rem !important;
}

[data-testid="stRadio"] > label {
    display: none !important;
}

[data-testid="stRadio"] div[role="radiogroup"] {
    gap: .15rem !important;
    align-items: center !important;
    flex-wrap: wrap !important;
}

[data-testid="stRadio"] div[role="radiogroup"] > label {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    box-shadow: none !important;
    border-radius: 0 !important;

    padding: .45rem .8rem .5rem .2rem !important;
    margin: 0 .25rem 0 0 !important;

    color: #334155 !important;
    font-size: .86rem !important;
    font-weight: 800 !important;

    min-height: auto !important;
    cursor: pointer !important;

    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    color: #166534 !important;
    border-bottom-color: #86efac !important;
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
    visibility: visible !important;
}

/* Hide only the actual radio control */
[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

.bb-ai-caption {
    color: #64748b !important;
    font-size: .78rem;
    margin: -.1rem 0 .7rem 0;
}


/* =========================================================
   BUTTONS
   ========================================================= */

div.stButton > button,
div[data-testid="stDownloadButton"] > button {
    background: #0f172a !important;
    color: #ffffff !important;

    border: 1px solid #0f172a !important;
    border-radius: 12px !important;

    font-weight: 800 !important;
    min-height: 2.8rem;

    opacity: 1 !important;
    visibility: visible !important;
}

div.stButton > button *,
div[data-testid="stDownloadButton"] > button * {
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
}

div.stButton > button:hover,
div.stButton > button:focus,
div.stButton > button:active,
div[data-testid="stDownloadButton"] > button:hover,
div[data-testid="stDownloadButton"] > button:focus,
div[data-testid="stDownloadButton"] > button:active {
    background: #166534 !important;
    border-color: #166534 !important;
    color: #ffffff !important;
}


/* =========================================================
   FLOATING AI BUTTON
   ========================================================= */

[data-testid="stPopover"] > button {
    position: fixed !important;
    right: 24px !important;
    bottom: 24px !important;

    z-index: 999999 !important;

    border-radius: 999px !important;

    background: #0f172a !important;
    color: #ffffff !important;

    border: 2px solid #ffffff !important;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, .28) !important;

    padding: .7rem 1rem !important;

    font-weight: 800 !important;

    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stPopover"] > button *,
[data-testid="stPopover"] > button p,
[data-testid="stPopover"] > button span {
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stPopover"] > button:hover {
    background: #166534 !important;
    border-color: #16a34a !important;
}


/* =========================================================
   POPOVER CHAT
   ========================================================= */

[data-testid="stPopoverBody"] {
    background: #ffffff !important;
    color: #0f172a !important;

    min-width: 380px !important;
    max-width: 440px !important;

    padding: 1.2rem !important;
    border-radius: 16px !important;

    box-shadow: 0 10px 30px rgba(15, 23, 42, .2) !important;
}

[data-testid="stPopoverBody"] * {
    color: #0f172a !important;
}

[data-testid="stPopoverBody"] textarea {
    background: #ffffff !important;
    color: #0f172a !important;

    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

[data-testid="stPopoverBody"] textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
}


/* =========================================================
   STREAMLIT INPUT CONTRAST
   ========================================================= */

input,
textarea {
    color: #0f172a !important;
}

input::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}


/* Labels */
label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p {
    color: var(--bb-text) !important;
    opacity: 1 !important;
}


/* Selectbox / multiselect text */
[data-baseweb="select"] * {
    opacity: 1 !important;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {
    border-radius: 12px !important;
}


/* =========================================================
   EXPANDER
   ========================================================= */

[data-testid="stExpander"] {
    border-radius: 12px !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.bb-footer {
    color: #64748b !important;
    font-size: .82rem;
    text-align: center;
    padding: 1rem 0;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {
    .bb-snapshot-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .bb-snapshot-grid {
        grid-template-columns: 1fr;
    }

    .bb-hero h1 {
        font-size: 2rem;
    }

    [data-testid="stPopoverBody"] {
        min-width: 300px !important;
        max-width: 90vw !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# CONSTANTS
# ============================================================

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


GRID_CO2_FACTOR = 0.40


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def money(value):
    return f"PKR {value:,.0f}"


def calculate_appliance_energy(watts, hours_per_day, quantity, days=30):
    return (
        watts
        * hours_per_day
        * quantity
        * days
    ) / 1000


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
# BILL EXTRACTION
# ============================================================

def extract_bill_data(uploaded_file, bill_type):

    client = build_ai_client()

    if client is None:
        return (
            None,
            "AI is not connected. Add GEMINI_API_KEY in Streamlit Secrets."
        )

    try:

        uploaded_file.seek(0)

        bill_part = genai.types.Part.from_bytes(
            data=uploaded_file.getvalue(),
            mime_type=uploaded_file.type
            or "application/octet-stream",
        )

        prompt = f"""
You are extracting data from a Pakistani electricity bill.

This is the {bill_type} electricity bill.

Read ONLY information visibly present in the uploaded document.

Do not guess.
Do not invent.
Do not calculate missing values.

Return ONLY valid JSON with exactly these keys:

{{
    "bill_amount_pkr": number or null,
    "units_kwh": number or null
}}

bill_amount_pkr:
Use the final/current payable amount or total bill amount.

units_kwh:
Use the billed electricity consumption/units.

If something is not clearly visible, return null.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                bill_part,
                prompt,
            ],
        )

        text = (response.text or "").strip()

        if text.startswith("```"):
            text = text.strip("`").strip()

            if text.lower().startswith("json"):
                text = text[4:].strip()

        data = json.loads(text)

        return data, None

    except Exception as exc:

        return (
            None,
            f"Could not read the uploaded bill: {exc}"
        )


# ============================================================
# AI SPECIALIST MODULES
# ============================================================

def run_ai_analysis(
    user_data,
    role,
    user_question=None,
):

    client = build_ai_client()

    if client is None:
        return (
            "⚠️ AI is not connected yet.\n\n"
            "Please add `GEMINI_API_KEY` in your Streamlit Cloud "
            "Secrets to activate the AI features."
        )

    role_instructions = {

        "Understanding Agent": """
You are the Understanding Specialist for Bijli Bachat AI.

Your job is to understand the household situation.

Identify:
- Main energy problem
- Important household usage patterns
- Possible reasons for high consumption
- Key areas that need attention

Explain everything in simple language.
Do not invent missing information.
""",

        "Energy Analysis Agent": """
You are the Energy Analysis Specialist.

Analyze:
- Appliance-level electricity consumption
- Estimated monthly kWh
- Estimated appliance cost
- Highest energy-consuming appliances
- Appliance consumption patterns
- Potential energy waste

Prioritize measurable findings.
Never fabricate meter readings.
""",

        "Saving Strategy Agent": """
You are the Saving Strategy Specialist.

Create a practical energy-saving strategy for a Pakistani household.

Prioritize:
1. High-impact actions
2. Low-cost actions
3. Easy behavioral changes
4. Appliance optimization

Give estimated savings only when data supports an estimate.

Clearly label estimates.
""",

        "Monitoring & Alerting Agent": """
You are the Monitoring & Alerting Specialist.

Identify:
- Energy warning signs
- Bill warning signs
- Consumption thresholds
- Monthly checks
- Important things the household should monitor

This MVP does NOT have live smart-meter access.

Never claim live monitoring.
""",

        "General Energy Assistant": """
You are a helpful household energy-efficiency assistant.

Answer the user's specific question using the supplied household data.

Be:
- Practical
- Clear
- Concise
- Honest about estimates
""",
    }

    instruction = role_instructions.get(
        role,
        role_instructions["General Energy Assistant"],
    )

    prompt = f"""
PROJECT:
Bijli Bachat AI — Smart Energy & Bill Optimizer

COUNTRY:
Pakistan

APPLICATION PURPOSE:
Help households understand electricity consumption,
identify energy-heavy appliances,
reduce electricity waste,
save money and understand environmental impact.

IMPORTANT RULES:

- Never fabricate data.
- Never invent meter readings.
- Never claim access to live electricity data.
- Calculations come from user-provided data.
- AI recommendations are estimates.
- Clearly distinguish calculations from AI estimates.

SPECIALIST ROLE:

{instruction}

HOUSEHOLD DATA:

{json.dumps(
    user_data,
    indent=2,
    ensure_ascii=False,
    default=str,
)}

USER QUESTION:

{user_question or "Provide the requested specialist analysis."}

OUTPUT:

Use clear headings.

Use bullet points.

Keep recommendations practical.

Mention missing information when important.

Make the answer useful for a normal Pakistani household.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return response.text or "No AI response was returned."

    except Exception as exc:

        return f"AI request failed: {exc}"


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="bb-hero">

    <span class="bb-hero-badge">
        AI-POWERED ENERGY EFFICIENCY • HACKATHON MVP
    </span>

    <h1>⚡ Bijli Bachat AI</h1>

    <p>
        Smart Energy & Bill Optimizer — understand your electricity
        usage, identify energy-heavy appliances, reduce waste and
        build a practical saving strategy.
    </p>

</div>
""",
    unsafe_allow_html=True,
)

st.caption(
    "Decision-support tool: calculations are based on your entered data, "
    "while AI provides explanations, insights and recommendations."
)


# ============================================================
# SESSION STATE
# ============================================================

if "analyzed" not in st.session_state:
    st.session_state["analyzed"] = False

if "active_ai_section" not in st.session_state:
    st.session_state["active_ai_section"] = 0

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# ============================================================
# SIDEBAR — HOUSEHOLD PROFILE
# ============================================================

with st.sidebar:

    st.markdown("## 🏠 Household Profile")

    household_size = st.number_input(
        "People in household",
        min_value=1,
        max_value=30,
        value=4,
        step=1,
    )

    city = st.text_input(
        "City",
        value="Multan",
    )

    st.markdown("### ⚡ Electricity Data")

    monthly_bill = st.number_input(
        "Latest monthly electricity bill (PKR)",
        min_value=0.0,
        value=25000.0,
        step=500.0,
    )

    latest_bill_file = st.file_uploader(
        "Upload latest electricity bill (optional)",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
            "pdf",
        ],
        help="Upload a clear electricity bill image or PDF.",
    )

    previous_bill = st.number_input(
        "Previous month's electricity bill (optional)",
        min_value=0.0,
        value=0.0,
        step=500.0,
        help="Used to calculate bill-over-bill alerts.",
    )

    previous_bill_file = st.file_uploader(
        "Upload previous month's bill (optional)",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
            "pdf",
        ],
    )

    monthly_units = st.number_input(
        "Latest monthly units (kWh)",
        min_value=0.0,
        value=300.0,
        step=10.0,
        help="Enter the units shown on your electricity bill.",
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
        value=(
            monthly_bill / monthly_units
            if monthly_units
            else 0.0
        ),
        step=1.0,
        help=(
            "Approximation for calculations. Actual electricity "
            "bills can include taxes, fixed charges and slab effects."
        ),
    )


    # ========================================================
    # BILL EXTRACTION BUTTONS
    # ========================================================

    if latest_bill_file:

        if st.button(
            "📄 Read Latest Bill with AI",
            use_container_width=True,
        ):

            with st.spinner("AI is reading your bill..."):

                data, error = extract_bill_data(
                    latest_bill_file,
                    "latest",
                )

            if error:

                st.error(error)

            else:

                if data.get("bill_amount_pkr") is not None:
                    st.session_state[
                        "monthly_bill_input"
                    ] = float(data["bill_amount_pkr"])

                if data.get("units_kwh") is not None:
                    st.session_state[
                        "monthly_units_input"
                    ] = float(data["units_kwh"])

                st.success("Latest bill data extracted.")

                st.rerun()


    if previous_bill_file:

        if st.button(
            "📄 Read Previous Bill with AI",
            use_container_width=True,
        ):

            with st.spinner("AI is reading the previous bill..."):

                data, error = extract_bill_data(
                    previous_bill_file,
                    "previous",
                )

            if error:

                st.error(error)

            else:

                if data.get("bill_amount_pkr") is not None:
                    st.session_state[
                        "previous_bill_input"
                    ] = float(data["bill_amount_pkr"])

                if data.get("units_kwh") is not None:
                    st.session_state[
                        "previous_units_input"
                    ] = float(data["units_kwh"])

                st.success("Previous bill data extracted.")

                st.rerun()


    # ========================================================
    # APPLIANCES
    # ========================================================

    st.markdown("---")

    st.markdown("### 🔌 Appliance Setup")

    st.caption(
        "Add the appliances you want Bijli Bachat AI to analyze."
    )

    appliance_count = st.number_input(
        "Number of appliances",
        min_value=1,
        max_value=25,
        value=6,
        step=1,
    )

    appliances = []

    for i in range(int(appliance_count)):

        with st.expander(
            f"Appliance {i + 1}",
            expanded=(i < 2),
        ):

            appliance_type = st.selectbox(
                "Appliance",
                list(APPLIANCE_PRESETS.keys()),
                key=f"type_{i}",
            )

            default_watts = APPLIANCE_PRESETS[
                appliance_type
            ]

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


# ============================================================
# CALCULATIONS
# ============================================================

rows = []

for appliance in appliances:

    kwh = calculate_appliance_energy(
        appliance["watts"],
        appliance["hours_per_day"],
        appliance["quantity"],
    )

    cost = kwh * tariff

    rows.append(
        {
            "Appliance": appliance["name"],
            "Power (W)": appliance["watts"],
            "Hours/day": appliance["hours_per_day"],
            "Qty": appliance["quantity"],
            "Monthly kWh": kwh,
            "Estimated Cost": cost,
        }
    )


df = pd.DataFrame(rows)

total_appliance_kwh = (
    float(df["Monthly kWh"].sum())
    if not df.empty
    else 0.0
)

estimated_appliance_cost = (
    total_appliance_kwh * tariff
)


if monthly_units > 0:

    appliance_share = (
        total_appliance_kwh
        / monthly_units
        * 100
    )

else:

    appliance_share = 0.0


# ============================================================
# MONTH-TO-MONTH CHANGES
# ============================================================

if previous_units > 0 and monthly_units > 0:

    units_change_pct = (
        (monthly_units - previous_units)
        / previous_units
    ) * 100

else:

    units_change_pct = None


if previous_bill > 0 and monthly_bill > 0:

    bill_change_pct = (
        (monthly_bill - previous_bill)
        / previous_bill
    ) * 100

else:

    bill_change_pct = None


# ============================================================
# CARBON
# ============================================================

estimated_co2 = (
    monthly_units
    * GRID_CO2_FACTOR
)


# ============================================================
# MAIN DASHBOARD
# ============================================================

st.markdown(
    '<div class="bb-section-title">📊 Your Energy Snapshot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="bb-section-subtitle">
Automatically highlights positive trends, warnings and
high-priority energy situations.
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SNAPSHOT STATUS
# ============================================================

def status_card(
    title,
    value,
    status,
    status_text,
):

    return f"""
    <div class="bb-snapshot-card {status}">

        <div class="bb-snapshot-title">
            {title}
        </div>

        <div class="bb-snapshot-value">
            {value}
        </div>

        <div class="bb-snapshot-status">
            {status_text}
        </div>

    </div>
    """


# Units

if units_change_pct is None:

    units_status = "neutral"
    units_text = "Add previous units for comparison"

elif units_change_pct <= -5:

    units_status = "good"
    units_text = (
        f"↓ {abs(units_change_pct):.1f}% vs previous month"
    )

elif units_change_pct >= 10:

    units_status = "alert"
    units_text = (
        f"↑ {units_change_pct:.1f}% — energy alert"
    )

else:

    units_status = "warning"
    units_text = "Monitor your consumption"


# Bill

if bill_change_pct is None:

    bill_status = "neutral"
    bill_text = "Add previous bill for comparison"

elif bill_change_pct <= -5:

    bill_status = "good"
    bill_text = (
        f"↓ {abs(bill_change_pct):.1f}% vs previous bill"
    )

elif bill_change_pct >= 10:

    bill_status = "alert"
    bill_text = (
        f"↑ {bill_change_pct:.1f}% — bill alert"
    )

else:

    bill_status = "warning"
    bill_text = "Monitor your bill"


# Appliance estimate

if monthly_units <= 0:

    appliance_status = "neutral"
    appliance_text = "Enter monthly units"

elif total_appliance_kwh > monthly_units * 1.05:

    appliance_status = "alert"
    appliance_text = "Estimate exceeds bill units"

elif total_appliance_kwh <= monthly_units * 0.75:

    appliance_status = "good"
    appliance_text = "Within your bill-unit range"

else:

    appliance_status = "warning"
    appliance_text = "Review appliance usage"


# Overall trend

if units_change_pct is None and bill_change_pct is None:

    trend_status = "neutral"
    trend_text = "Add previous data for alerts"
    trend_value = "N/A"

elif (
    (
        units_change_pct is not None
        and units_change_pct >= 10
    )
    or
    (
        bill_change_pct is not None
        and bill_change_pct >= 10
    )
):

    trend_status = "alert"
    trend_text = "High-priority review recommended"

    if units_change_pct is not None:
        trend_value = f"{units_change_pct:+.1f}%"
    else:
        trend_value = f"{bill_change_pct:+.1f}%"

elif (
    units_change_pct is not None
    and units_change_pct <= -5
    and
    (
        bill_change_pct is None
        or bill_change_pct <= -5
    )
):

    trend_status = "good"
    trend_text = "Overall energy trend improving"
    trend_value = (
        f"{units_change_pct:+.1f}%"
    )

else:

    trend_status = "warning"
    trend_text = "Monitor next month's numbers"

    if units_change_pct is not None:
        trend_value = (
            f"{units_change_pct:+.1f}%"
        )
    else:
        trend_value = "Stable"


# ============================================================
# SNAPSHOT HTML
# ============================================================

st.markdown(
    f"""
<div class="bb-snapshot-grid">

    {
        status_card(
            "Monthly Units",
            f"{monthly_units:,.0f} kWh",
            units_status,
            units_text,
        )
    }

    {
        status_card(
            "Latest Bill",
            money(monthly_bill),
            bill_status,
            bill_text,
        )
    }

    {
        status_card(
            "Appliance Estimate",
            f"{total_appliance_kwh:,.0f} kWh",
            appliance_status,
            appliance_text,
        )
    }

    {
        status_card(
            "Energy Trend",
            trend_value,
            trend_status,
            trend_text,
        )
    }

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# AUTOMATIC ALERTS
# ============================================================

if (
    bill_change_pct is not None
    and bill_change_pct >= 10
    and units_change_pct is not None
    and units_change_pct <= 0
):

    st.markdown(
        f"""
<div class="bb-warning">

⚠️ <b>Bill Alert:</b>
Your bill increased by
<b>{bill_change_pct:.1f}%</b>
while your electricity units did not increase.

This can happen because of tariff slabs,
taxes, fixed charges or other bill components.

</div>
""",
        unsafe_allow_html=True,
    )


elif (
    bill_change_pct is not None
    and bill_change_pct >= 10
) or (
    units_change_pct is not None
    and units_change_pct >= 10
):

    reasons = []

    if (
        bill_change_pct is not None
        and bill_change_pct >= 10
    ):

        reasons.append(
            f"bill is up {bill_change_pct:.1f}%"
        )

    if (
        units_change_pct is not None
        and units_change_pct >= 10
    ):

        reasons.append(
            f"units are up {units_change_pct:.1f}%"
        )

    st.markdown(
        f"""
<div class="bb-danger">

🚨 <b>Energy Alert:</b>
{" and ".join(reasons)}
compared with the previous month.

Check the appliance audit below
for possible high-consumption drivers.

</div>
""",
        unsafe_allow_html=True,
    )


elif (
    bill_change_pct is not None
    and bill_change_pct <= -5
    and
    (
        units_change_pct is None
        or units_change_pct <= -5
    )
):

    st.markdown(
        f"""
<div class="bb-success">

✅ <b>Good News:</b>
Your electricity bill reduced by
<b>{abs(bill_change_pct):.1f}%</b>
compared with the previous bill.

Your energy trend is also improving.

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# APPLIANCE ENERGY AUDIT
# ============================================================

st.markdown("---")

left, right = st.columns(
    [1.15, 0.85]
)


with left:

    st.markdown(
        '<div class="bb-section-title">🔌 Appliance Energy Audit</div>',
        unsafe_allow_html=True,
    )

    if not df.empty:

        display_df = df.copy()

        display_df["Monthly kWh"] = (
            display_df["Monthly kWh"]
            .round(1)
        )

        display_df["Estimated Cost"] = (
            display_df["Estimated Cost"]
            .round(0)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Monthly Energy Consumption")

        chart_df = df[
            [
                "Appliance",
                "Monthly kWh",
            ]
        ].copy()

        chart_df = chart_df.sort_values(
            "Monthly kWh",
            ascending=True,
        )

        st.bar_chart(
            chart_df.set_index("Appliance")
        )

    else:

        st.info(
            "Add appliances from the Household Profile."
        )


# ============================================================
# HIGHEST ENERGY CONSUMERS
# ============================================================

with right:

    st.markdown(
        '<div class="bb-section-title">🎯 Highest Energy Consumers</div>',
        unsafe_allow_html=True,
    )

    if not df.empty:

        top = (
            df.sort_values(
                "Monthly kWh",
                ascending=False,
            )
            .head(5)
        )

        for _, row in top.iterrows():

            share = (
                row["Monthly kWh"]
                / total_appliance_kwh
                * 100
                if total_appliance_kwh
                else 0
            )

            st.markdown(
                f"""
<div class="bb-card">

    <b>{row["Appliance"]}</b>

    <div class="bb-muted">

        {row["Monthly kWh"]:.1f} kWh/month

        • {money(row["Estimated Cost"])}

        • {share:.1f}% of entered appliance consumption

    </div>

</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# CARBON FOOTPRINT
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="bb-section-title">🌱 Carbon Footprint Estimate</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="bb-carbon-card">

    <div class="bb-carbon-label">
        Estimated Carbon Footprint
    </div>

    <div class="bb-carbon-value">
        {estimated_co2:,.1f} kg CO₂e/month
    </div>

    <div class="bb-carbon-note">

        Planning estimate using an illustrative
        grid factor of {GRID_CO2_FACTOR:.2f}
        kg CO₂e/kWh.

        This is not an official Pakistan
        grid-emissions factor.

    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# USER DATA FOR AI
# ============================================================

user_data = {

    "city": city,

    "household_size": household_size,

    "monthly_bill_pkr": monthly_bill,

    "previous_month_bill_pkr": previous_bill,

    "monthly_units_kwh": monthly_units,

    "previous_month_units_kwh": previous_units,

    "approx_cost_per_unit_pkr": tariff,

    "estimated_appliance_kwh": total_appliance_kwh,

    "estimated_appliance_cost_pkr":
        estimated_appliance_cost,

    "estimated_monthly_co2_kg":
        estimated_co2,

    "bill_change_percent":
        bill_change_pct,

    "units_change_percent":
        units_change_pct,

    "appliances": rows,
}


# ============================================================
# PERSONALIZED AI ENERGY AUDIT
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="bb-section-title">🤖 Personalized AI Energy Audit</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="bb-section-subtitle">

Four focused AI specialists analyze the same household
data from different perspectives.

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# AI NAVIGATION
# ============================================================

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

    index=st.session_state[
        "active_ai_section"
    ],

    horizontal=True,

    label_visibility="collapsed",

    key="ai_section_radio",
)


st.session_state[
    "active_ai_section"
] = ai_names.index(selected_name)


active_idx = st.session_state[
    "active_ai_section"
]


active_role = ai_roles[
    active_idx
]


active_name = (
    selected_name
    .split(" ", 1)[-1]
)


st.markdown(
    f"""
<div class="bb-ai-caption">

{active_name}
· AI specialist analysis based on your household data

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GENERATE AI REPORT
# ============================================================

if st.button(

    f"✨ Generate {active_name} Report",

    key=f"generate_ai_{active_idx}",

    use_container_width=True,

):

    with st.spinner(
        f"{active_role} is analyzing your data..."
    ):

        result = run_ai_analysis(
            user_data,
            active_role,
        )

    st.session_state[
        f"ai_result_{active_idx}"
    ] = result


# ============================================================
# SHOW SAVED AI RESULT
# ============================================================

saved_result = st.session_state.get(
    f"ai_result_{active_idx}"
)


if saved_result:

    st.markdown(saved_result)

    st.download_button(

        "⬇️ Download This AI Report",

        data=saved_result,

        file_name=(
            "bijli_bachat_"
            + ai_roles[active_idx]
            .lower()
            .replace(" ", "_")
            .replace("&", "and")
            + ".txt"
        ),

        mime="text/plain",

        key=f"download_ai_{active_idx}",

        use_container_width=True,

    )


# ============================================================
# FLOATING ASK ENERGY AI
# ============================================================

with st.popover("🤖 Ask Energy AI"):

    st.markdown(
        "### 💬 Energy Assistant"
    )

    st.caption(
        "Ask anything about your household "
        "energy usage, appliances or saving strategies."
    )


    # Show last messages

    for msg in st.session_state[
        "chat_history"
    ][-6:]:

        with st.chat_message(
            msg["role"]
        ):

            st.write(
                msg["content"]
            )


    question = st.text_area(

        "Your question",

        placeholder=(
            "Example: Why is my electricity bill high?"
        ),

        key="floating_energy_question",

        height=90,

    )


    if st.button(

        "Send to Energy AI",

        key="floating_send",

        use_container_width=True,

    ):

        cleaned_q = (
            question.strip()
            .lower()
        )


        if question.strip():

            st.session_state[
                "chat_history"
            ].append(

                {
                    "role": "user",
                    "content": question.strip(),
                }

            )


            greetings = [

                "hi",
                "hii",
                "hiii",
                "hiiii",
                "hello",
                "hey",
                "salam",
                "assalam-o-alaikum",
                "assalam o alaikum",
                "good morning",
                "good evening",

            ]


            if cleaned_q in greetings:

                answer = (
                    "Hello! 👋 I am your Energy Assistant. "
                    "Ask me anything about your electricity "
                    "usage, appliances or ways to reduce your bill."
                )

            else:

                with st.spinner(
                    "Energy AI is analyzing your data..."
                ):

                    answer = run_ai_analysis(

                        user_data,

                        "General Energy Assistant",

                        question.strip(),

                    )


            st.session_state[
                "chat_history"
            ].append(

                {
                    "role": "assistant",
                    "content": answer,
                }

            )

            st.rerun()

        else:

            st.warning(
                "Please enter a question first."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
<div class="bb-footer">

Bijli Bachat AI • Environment & Sustainability —
Tech for Good • Hackathon MVP

<br>

Calculations are estimates based on
user-provided data. AI recommendations
should be treated as decision-support guidance.

</div>
""",
    unsafe_allow_html=True,
)
