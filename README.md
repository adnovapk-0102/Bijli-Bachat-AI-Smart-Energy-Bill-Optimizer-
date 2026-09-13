# PRODUCT REQUIREMENTS DOCUMENT (PRD)

**Project Name:** Bijli-Bachat & Eco-Saver AI
**Document Version:** 1.0 (Hackathon MVP Edition)
**Author:** Taha Bilal
**Date:** September 2026
**Platform:** Web Application (Responsive Desktop & Mobile)
**Tech Stack:** Python, Streamlit, Pandas, Google Gemini API

---

## TABLE OF CONTENTS
1. Executive Summary
2. Target Audience
3. Product Features & Requirements
4. Technical Architecture
5. User Journey
6. Future Roadmap

---

## 1. EXECUTIVE SUMMARY

### 1.1. Problem Statement
Pakistani households face soaring electricity costs without a clear understanding of which appliances contribute most to their monthly bills. Traditional utility bills provide a total payable amount and total consumed units, but lack granular, actionable insights into daily energy consumption patterns. 

### 1.2. Proposed Solution
Bijli-Bachat & Eco-Saver AI is a smart energy and bill optimizer dashboard designed to bridge this gap. It empowers users to estimate appliance-level energy consumption, extract billing data automatically via AI OCR, and receive personalized, AI-driven strategies to reduce their energy footprint and optimize monthly utility costs.

---

## 2. TARGET AUDIENCE

* **Primary Users:** Middle to lower-middle-class household managers and residents in Pakistan actively seeking ways to monitor and reduce monthly utility expenses.
* **Secondary Users:** Environmentally conscious individuals aiming to track and minimize their household's carbon footprint.

---

## 3. PRODUCT FEATURES & REQUIREMENTS (MVP SCOPE)

### 3.1. Smart Bill Data Extraction (AI OCR)
* **Description:** Automated data entry from physical or digital bills.
* **Requirements:** 
  * Users must be able to upload images (PNG, JPG) or PDFs of their latest and previous electricity bills.
  * The system will utilize Gemini AI to scan the document and securely extract `bill_amount_pkr` and `units_kwh`.
  * Extracted data must auto-populate the respective input fields in the user interface.

### 3.2. Interactive Appliance Energy Audit
* **Description:** A dynamic calculator for estimating monthly energy usage based on user habits.
* **Requirements:**
  * Users can dynamically add up to 25 appliances.
  * Inputs must include: Appliance Type (from preset dropdowns), Power Rating (Watts), Daily Usage (Hours), and Quantity.
  * System must calculate and display estimated monthly kWh and total cost in PKR per appliance.

### 3.3. Energy Snapshot & Trend Alerts
* **Description:** A real-time comparative dashboard.
* **Requirements:**
  * Display top-level metrics: Latest Bill, Monthly Units, Appliance Estimate, and Energy Trend.
  * Calculate percentage changes between the current and previous month's data.
  * Trigger automated UI color-coded alerts (Success/Green, Warning/Yellow, Critical/Red) if consumption spikes or drops by ±10%.

### 3.4. Agentic AI Energy Specialists
* **Description:** Prompt-based specialist modules providing contextual advice.
* **Requirements:**
  * **Understanding Agent:** Summarizes the household's overall energy profile.
  * **Energy Analysis Agent:** Identifies heavy consumption drivers and unusual data patterns.
  * **Saving Strategy Agent:** Recommends high-impact, low-cost practical energy-saving steps.
  * **Monitoring & Alerting Agent:** Suggests specific usage thresholds to monitor for the next billing cycle.
  * Feature must include an option to download generated reports as `.txt` files.

### 3.5. Floating Energy AI Assistant
* **Description:** An omnipresent chat interface for dynamic queries.
* **Requirements:**
  * Accessible via a sticky popover button on the UI.
  * Maintains conversational context.
  * Answers specific queries (e.g., "How can I reduce AC consumption?") strictly based on the user's localized input data.

### 3.6. Carbon Footprint Estimator
* **Description:** Environmental impact tracking.
* **Requirements:**
  * Calculate estimated CO₂ emissions (kg CO₂e/month) using an illustrative grid conversion factor for Pakistan.
  * Display a dedicated dashboard card promoting eco-friendly habits.

---

## 4. TECHNICAL ARCHITECTURE

* **Frontend:** Streamlit framework utilizing custom CSS. The UI must ensure strict dual-theme (Light/Dark) consistency, ensuring professional rendering of sidebars, metrics, and interactive popovers regardless of device system settings.
* **Backend Data Handling:** Python with Pandas for dynamic dataframe creation, filtering, sorting, and mathematical aggregations.
* **AI Integration:** Google `genai` Client SDK utilizing lightweight LLM models (e.g., Gemini 3.6 Flash) for OCR extraction and role-based prompt engineering.

---

## 5. USER JOURNEY (FLOW)

1. **Onboarding:** User opens the web app and enters basic household demographics (size, city) in the sidebar.
2. **Data Input:** User uploads bill images for automatic data extraction or manually enters current/previous bill amounts and consumed units.
3. **Appliance Setup:** User configures their daily appliances from preset lists or custom inputs.
4. **Analysis Execution:** User clicks "Analyze My Energy" to generate the dashboard.
5. **Review Phase:** User reviews the Snapshot Grid, Trend Warning Cards, and Appliance Consumption Bar Chart.
6. **AI Consultation:** User generates specific AI Specialist reports (downloading them if needed) and interacts with the Floating Chat Assistant for quick, personalized advice.

---

## 6. FUTURE ROADMAP (POST-HACKATHON)

* **IoT Integration:** Connecting with local smart meters or smart plugs for real-time live data tracking.
* **Solar ROI Calculator:** A dedicated module recommending specific kW solar systems and calculating payback periods based on the user's generated energy audit.
* **Localization:** Multi-lingual support (including an Urdu language toggle) for broader accessibility and adoption across diverse demographics in Pakistan.
