# Intelligent Software Requirements Analysis System

Processes a client's free-text project description through a **5-step LangChain LCEL prompt chain** and produces a structured initial project assessment.

---

## How It Works

```
Client Text → Interpret → Categorise → Select Category → Find Gaps → Assessment
```

| Step | What it does |
|------|-------------|
| 1 | **Interpret** — understand the business objective |
| 2 | **List possible categories** that could apply |
| 3 | **Select the best category** from the approved list |
| 4 | **Extract missing requirements** needed before development |
| 5 | **Generate a structured assessment** report |

Each stage passes its output directly into the next using **LCEL composition** (`prompt | llm | parser`).

---

## Project Structure

```
requirements-analyzer/
├── main.py            ← the single script — run this
├── requirements.txt   ← Python dependencies
├── .env.example       ← template for your secrets
├── .gitignore         ← keeps .env out of git
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd requirements-analyzer-with-LCEL
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your values:
```
OPENROUTER_API_KEY=your_actual_key_here
MODEL_NAME=your_actual_model_here
```
Get a free API key at [openrouter.ai](https://openrouter.ai/keys).

---

## Usage

```bash
python main.py "Your client project description here"
```

### Examples

```bash
python main.py "I want to build a platform where farmers in Nigeria can list their produce and buyers can purchase directly, with payment via bank transfer"

python main.py "We need a system that tracks employee attendance using face recognition and generates monthly payroll reports"

python main.py "Build me a dashboard showing real-time sales data from our stores across Lagos"
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key (required) |
| `MODEL_NAME` | Model string e.g. `openai/gpt-4o` (required) |

---

## Available Categories

- Web Application
- Mobile Application
- API / Backend Service
- Data Analytics Platform
- AI / Machine Learning System
- E-Commerce Platform
- Enterprise Management System
- System Integration
- DevOps / Infrastructure Automation
- General Software Project
