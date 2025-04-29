# 🏡 Realtor Assist AI — Intelligent Rental Lead Assistant for Singapore Agents

**A next-generation conversational AI assistant for real estate agents in Singapore.**  
Realtor Assist AI prescreens and qualifies rental leads, matches them to listings, negotiates intelligently, and even books viewings—so you focus on closing deals, not chasing leads.

---

## ✨ Key Features

- 🧠 **Conversational Lead Screening**  
  Engages leads in natural chat to extract rental enquiry details automatically.

- 🏢 **Smart Listing Matching**  
  Matches user preferences (condo, room type, budget) against your listings using `real_estate_sheet.xlsx`.

- 📋 **Profile Extraction & Validation**  
  Captures lead details like age, profession, citizenship, move-in date, lease period, and validates completeness.

- 🔍 **Profile-Landlord Matching**  
  Compares lead profiles with each landlord’s stated criteria to ensure suitability.

- 🤝 **Intelligent Negotiation**  
  Attempts to close the gap for near-matches by negotiating rental terms or flagging flexible conditions.

- 📅 **Automated Appointment Booking** *(coming soon)*  
  Books viewings for qualified leads—zero back-and-forth needed.

- 🧑‍💼 **Human-in-the-Loop**  
  Escalates to a human agent if the bot is uncertain or clarification is needed.

---

## 🚀 Quick Start

### ✅ Prerequisites

- Python `>= 3.9`
- `langchain`, `langgraph`, and related dependencies
- An LLM API (e.g., OpenAI)
- `real_estate_sheet.xlsx` — your listings and landlord info

---

### ⚙️ Installation

```bash
git clone https://github.com/<your-username>/realtor-assist.git
cd realtor-assist
pip install -r requirements.txt
```

Create a `.env` file with your API keys and config.

Start the agent workflow (CLI, background job, or web endpoint).

---

## 🧩 Architecture Overview

The bot uses a **StateGraph** to orchestrate tasks via modular AI agents, defined in `my_agent/agent.py`.

### 🛠️ Agents & Workflow

| Agent              | Role                                                  |
|--------------------|-------------------------------------------------------|
| `intent_classifier`| Determines if the message is a rental enquiry         |
| `enquiry_extractor`| Parses enquiry info (condo, type, price)              |
| `enquiry_checker`  | Matches enquiry to available listings                 |
| `profile_extractor`| Gathers user's profile data                           |
| `profile_checker`  | Validates profile completeness                        |
| `profile_matcher`  | Compares profile with landlord preferences            |
| `negotiation_agent`| Negotiates when needed                                |
| `human_interrupt`  | Escalates to human if stuck                           |

---

## 📁 File Structure

```text
realtor-assist/
│
├── my_agent/
│   ├── agent.py          # Orchestration graph
│   ├── logging.py        # Logging setup
│   ├── settings.py       # Configs & model setup
│   └── utils/
│       ├── agents/       # All task-specific agent logic
│       └── state.py      # State definitions
│
```

---

## 🔧 Customization

- ✏️ Modify agent behavior in `my_agent/utils/agents/`
- 🔁 Swap out LLMs or APIs via `settings.py`
- 🗂️ Adapt listing data by editing `real_estate_sheet.xlsx`
- 📆 Extend human-in-the-loop or appointment logic

---

## 📊 Logging & Monitoring

- Logs saved in `logs/` directory (per day)
- Controlled via `my_agent/logging.py`

---

## 🔐 Security & Best Practices

- API keys and sensitive config are stored in `.env` (excluded from version control)
- All fields are validated. If user info is missing, the agent gracefully handles with `None`—no hallucinations.

---

## 🌟 Support the Project

If this project saves you time or inspires your own AI real estate tools, **give it a star ⭐** and share it with your team or network!
