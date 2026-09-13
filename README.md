# Sales Interaction Intelligence

> Traditional NLP system for extracting customer sentiment, intent, interest, product opportunities, and follow-up requirements from banking sales interaction notes.

## 🎯 Problem

Banking sales interactions are often stored as short, unstructured text such as:

> "Customer is interested in personal loan."

> "Customer is not interested in credit card."

> "Customer asked to call tomorrow."

This project converts these interaction notes into structured insights.

## 🔍 What It Extracts

For each interaction, the system identifies:

- **Sentiment** — Positive / Negative / Neutral
- **Customer Interest** — Yes / No / Unclear
- **Interested Product**
- **Not Interested Product**
- **Customer Intent**
- **Customer-Requested Follow-up**
- **Follow-up Action**

### Example

**Input**
```text
Customer is not interested in credit card.

Output

{
  "sentiment": "negative",
  "interest_shown": false,
  "not_interested_product": "Credit Card",
  "customer_intent": "product_rejection",
  "follow_up_required": false
}
🧠 Approach

The current implementation uses traditional, explainable NLP techniques — no LLM or external AI API.

Raw Interaction
      ↓
Text Normalization
      ↓
Product Extraction
      ↓
Negation Detection
      ↓
Interest / Rejection Detection
      ↓
Follow-up Detection
      ↓
Sentiment Analysis
      ↓
Intent Classification
      ↓
Structured Output
Key Design Principles
Product mention ≠ customer interest
Existing product usage ≠ new interest
Salesperson follow-up ≠ customer-requested follow-up
Rejection signals take priority over positive signals
Ambiguous interactions remain Unclear rather than being guessed
📊 Dataset

The initial dataset contains 447 banking interaction records with:

Column	Description
Initiatives/Opportunities	Sales interaction notes
Comments	Analytics / recommendation context

The original dataset is not included in the repository for privacy and data-protection reasons.

🛠️ Tech Stack
Python 3.12+
Regex
NLTK
Pandas
scikit-learn
OpenPyXL
FastAPI
Pydantic
Git / GitHub
📁 Structure
sales-interaction-intelligence/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   └── classical_nlp.py
│   │   ├── test_classical_nlp.py
│   │   ├── audit_classical_nlp.py
│   │   └── batch_analyze.py
│   └── requirements.txt
├── data/              # Private dataset — not committed
├── docs/
├── notebooks/
├── tests/
├── frontend/
├── .gitignore
└── README.md
🚀 Setup
git clone https://github.com/agastyasharma20/sales-interaction-intelligence.git
cd sales-interaction-intelligence

python -m venv .venv
.venv\Scripts\activate

pip install -r backend/requirements.txt
▶️ Run
cd backend
python -m app.test_classical_nlp

Run the complete dataset audit:

python -m app.audit_classical_nlp
📈 Roadmap
Phase 1 — Traditional NLP ✅
Text normalization
Product extraction
Negation detection
Interest/rejection detection
Sentiment analysis
Follow-up detection
Intent classification
Dataset audit
Phase 2 — Machine Learning 🚧
Manual ground-truth labeling
TF-IDF
Logistic Regression / Linear SVM
Precision, Recall & F1
Confusion Matrix
Error Analysis
Phase 3 — Production 🔜
Batch Excel processing
Model persistence
FastAPI REST API
Deployment
Monitoring
⚠️ Important

This repository contains the NLP implementation, not the original banking/customer dataset.

Do not commit:

.env
customer data
banking records
API keys
confidential files
👨‍💻 Author

Agastya Sharma

GitHub

Status: 🚧 Traditional NLP baseline implemented → ML pipeline in progress
