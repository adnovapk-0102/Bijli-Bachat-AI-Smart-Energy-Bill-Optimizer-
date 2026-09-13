<div align="center">

# ⚡ Bijli-Bachat & Eco-Saver AI
*Smart Energy & Bill Optimizer for Pakistani Households*

<!-- Colored Tech Stack Badges -->
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Hackathon MVP](https://img.shields.io/badge/Status-Hackathon_MVP-success?style=for-the-badge)

<br>
</div>

---

## 📋 1. Project Overview

| 🏷️ Attribute | 📌 Details |
| :--- | :--- |
| **Project Name** | Bijli-Bachat & Eco-Saver AI |
| **Document Type** | Product Requirements Document (PRD) |
| **Version** | 1.0 (Hackathon MVP) |
| **Author** | Taha Bilal |
| **Platform** | Web Application (Responsive Desktop & Mobile) |

---

## 💡 2. Executive Summary

> **🚨 The Problem:** 
> Pakistani households face soaring electricity costs without a clear understanding of which appliances contribute most to their monthly bills. Traditional utility bills provide a total payable amount, but lack granular, actionable insights into daily consumption patterns.

> **✅ Our Solution:** 
> Bijli-Bachat & Eco-Saver AI is a smart energy optimizer dashboard. It empowers users to estimate appliance-level energy consumption, extract billing data automatically via AI OCR, and receive personalized, AI-driven strategies to reduce their energy footprint.

---

## 🎯 3. Target Audience

* 👨‍👩‍👧‍👦 **Primary Users:** Household managers and residents in Pakistan actively seeking ways to monitor and reduce monthly utility expenses.
* 🌱 **Secondary Users:** Environmentally conscious individuals aiming to track and minimize their household's carbon footprint.

---

## ⭐ 4. Core Features (MVP Scope)

### 📄 Smart Bill Data Extraction (AI OCR)
* **Functionality:** Users upload images (PNG, JPG) or PDFs of their electricity bills.
* **Tech:** Integrates **Google Gemini AI** to securely scan and extract `bill_amount_pkr` and `units_kwh` automatically.

### 🔌 Interactive Appliance Energy Audit
* **Functionality:** A dynamic calculator for estimating monthly energy usage.
* **Tech:** Users can add up to 25 appliances (Watts, Hours used, Quantity). The system dynamically calculates estimated monthly kWh and total PKR cost.

### 📊 Energy Snapshot & Trend Alerts
* **Functionality:** A real-time comparative dashboard.
* **Tech:** Calculates percentage changes between current and previous months. Triggers auto-color-coded UI alerts (🟢 Success, 🟡 Warning, 🔴 Critical) for sudden consumption spikes.

### 🤖 Agentic AI Energy Specialists
* **Functionality:** 4 specialized prompt-based AI modules:
  1. **Understanding Agent:** Summarizes the energy profile.
  2. **Energy Analysis Agent:** Identifies heavy consumption drivers.
  3. **Saving Strategy Agent:** Recommends high-impact, low-cost practical savings.
  4. **Monitoring Agent:** Suggests specific usage thresholds for the next month.

### 💬 Floating Energy AI Assistant
* **Functionality:** An omnipresent chat interface. Maintains conversational context, allowing users to ask specific queries (e.g., *"How can I reduce AC consumption?"*) based on their localized data.

### 🌱 Carbon Footprint Estimator
* **Functionality:** Calculates estimated CO₂ emissions (kg CO₂e/month) using an illustrative grid conversion factor to promote eco-friendly habits.

---

## ⚙️ 5. Technical Architecture

* **Frontend:** Built with `Streamlit`. Features custom CSS for strict dual-theme (Light/Dark) consistency, ensuring professional rendering of sidebars and metrics.
* **Backend Data:** Handled via `Python` & `Pandas` for dynamic dataframe creation, filtering, and mathematical aggregations.
* **AI Layer:** Google `genai` SDK utilizing lightweight LLM models (Gemini Flash) for OCR extraction and role-based prompt engineering.

---

## 🗺️ 6. User Journey (Flow)

1. **🏠 Onboarding:** User enters basic demographics (Household size, City).
2. **📸 Data Input:** User uploads bill images for AI extraction (or enters data manually).
3. **⚙️ Appliance Setup:** User configures daily appliances from preset lists.
4. **⚡ Analysis:** User clicks *"Analyze My Energy"* to generate the dashboard.
5. **📈 Review:** User reviews Snapshot Grid, Warnings, and Bar Charts.
6. **🧠 AI Consultation:** User generates AI reports and chats with the Floating Assistant.

---

## 🚀 7. Future Roadmap (Post-Hackathon)

- [ ] **IoT Integration:** Connecting with local smart meters for live data tracking.
- [ ] **Solar ROI Calculator:** Recommending kW solar systems based on user energy audits.
- [ ] **Urdu Localization:** Multi-lingual support for broader accessibility in Pakistan.

<br>

<div align="center">
  <p><i>Developed with ❤️ for a greener, energy-efficient Pakistan.</i></p>
</div>
