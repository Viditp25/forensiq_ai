# 🛡️ ForensiQ AI
### Autonomous Financial Forensics & Institutional Governance Platform

> **Developer:** Vidit Palarpwar  

---

## 📖 Overview

**ForensiQ AI** is an intelligent, institutional-grade forensic financial audit platform that combines rigorous tabular machine learning, unsupervised anomaly detection, network graph analysis, and local generative AI to evaluate corporate financial disclosures and detect financial distress.

Unlike cloud-based AI audit tools, ForensiQ AI executes entirely on local hardware (supported by local RTX GPUs and Ollama). Sensitive corporate documents, financial models, embeddings, and inference remain completely offline, ensuring privacy for financial research and auditing.

The platform enables users to:
- Screen corporate financial ratio datasets against extreme class imbalance (~3.23% fraud/distress benchmarks).
- Perform dimensionality reduction using **L1-Regularized LASSO** to extract core orthogonal forensic indicators from 95+ raw metrics.
- Benchmark multiple machine learning paradigms (**XGBoost, Logistic Regression, Isolation Forest**) via leakage-free stratified pipelines.
- Visualize corporate money-circulation and circular fund-routing networks using **NetworkX**.
- Ingest unstructured corporate PDF reports (Annual Reports, IPO DRHP filings) using `pdfplumber`.
- Run offline semantic vector search and local LLM inference (**Llama 3.1 8B**) governed by strict Pydantic schemas.

---

# ✨ Features

- 🤖 **5-Model Forensic Architecture:** Supervised probability classifiers, unsupervised isolation trees, linear residual checks, and network graph mining.
- 📉 **L1-LASSO Feature Reduction:** Automatically eliminates multicollinearity, reducing 95 raw financial ratios down to core orthogonal indicators.
- ⚖️ **Extreme Imbalance Handling:** Integrates SMOTE within strict `imblearn` cross-validation pipelines, prioritizing PR-AUC and ROC-AUC evaluation.
- 🕸️ **Money-Circulation Graph Analysis:** Maps corporate fund transfers, equity infusions, and related-party transaction flows using `NetworkX`.
- 📄 **Unstructured PDF Ingestion:** Extracts tables and text disclosures from corporate annual reports and IPO filings.
- 🧠 **Offline Semantic Vector Search:** Custom pure-Python cosine similarity vector engine powered by `sentence-transformers`.
- 🔒 **100% Local Execution:** Complete data privacy with zero cloud dependency or external API costs.
- 🛠️ **Deterministic JSON Governance:** Pydantic validation schemas with automated malformed-response recovery loops.

---

# 🏗️ System Architecture

```
                  ┌────────────────────┐
                  │     User Interface  │
                  │     (Streamlit)     │
                  └─────────┬───────────┘
                            │
            ┌───────────────┼────────────────┐
            │                                │
            ▼                                ▼
   Tabular ML Core                 Corporate PDF Reports
   (XGBoost / LASSO)                (Annual Reports / DRHP)
            │                                │
            ├────────────────┐               │
            ▼                ▼               ▼
     NetworkX Money     Isolation Forest  Text Extraction
   Circulation Graph   Anomaly Detection   (pdfplumber)
            │                │               │
            └───────────────┬────────────────┘
                            ▼
                 Sentence Embeddings
            (sentence-transformers)
                            │
                            ▼
               Local Vector Database
          (Pure Python Cosine Similarity)
                            │
                            ▼
                 Ollama Llama 3.1 (8B)
                            │
                            ▼
               Structured Audit Report
```

---

# 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Language | Python 3.13+ |
| Machine Learning | scikit-learn, XGBoost, imbalanced-learn (SMOTE) |
| Network Analysis | NetworkX, Matplotlib |
| PDF Parsing | pdfplumber |
| Embedding Model | sentence-transformers (all-MiniLM-L6-v2) |
| Local LLM | Ollama (Llama 3.1 8B) |
| Validation | Pydantic |
| Vector Storage | Custom Pure Python Cosine Similarity Engine |

---

# 📂 Project Structure

```
forensiq_ai/
│
├── main.py                  # Streamlit frontend application entry point
├── requirements.txt         # Project dependency manifest
├── README.md                # Documentation
├── data.csv                 # Core corporate financial ratio dataset
│
├── scaler.pkl               # Serialized StandardScaler artifact
├── feature_selector.pkl     # Serialized L1-LASSO feature selector artifact
├── forensic_ml_model.pkl    # Serialized supervised baseline model artifact
│
├── assets/                  # Visualizations and exported charts
├── core/                    # Core ML, graph analysis, and parser modules
└── utils/                   # Embedding, vector DB, and LLM governance utilities
```

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Viditp25/forensiq_ai.git

cd forensiq_ai
```

---

## 2. Install Dependencies

```bash
python -m pip install \
streamlit \
scikit-learn \
xgboost \
imbalanced-learn \
networkx \
sentence-transformers \
requests \
pydantic \
pdfplumber \
torch \
torchvision \
--index-url https://download.pytorch.org/whl/cpu
```

---

## 3. Start the Local LLM (Optional for Phase 2 AI Summaries)

Install Ollama and pull the required model:

```bash
ollama pull llama3.1:8b
```

Run Ollama locally:

```bash
ollama run llama3.1:8b
```

Keep this terminal running.

---

## 4. Launch the Application

```bash
python -m streamlit run main.py --server.fileWatcherType none
```

The application will be available at:

```
http://localhost:8501
```

---

# 📊 5-Model Forensic Pipeline Breakdown

1. **L1-LASSO Feature Selection:** Drives redundant financial ratio coefficients to zero, retaining top orthogonal risk indicators.
2. **Supervised Probability Classifiers (`P_ML`):** Benchmarks class-weighted Logistic Regression and XGBoost trained on SMOTE-resampled training folds.
3. **Unsupervised Anomaly Detection:** Utilizes Isolation Forest to isolate structural outliers without relying entirely on historical fraud labels.
4. **Linear Residual Modeling (`R_Norm`):** Validates cross-statement accounting consistency (e.g., matching liability ratios against expected operational returns).
5. **Money-Circulation Network Analysis (`S_Graph`):** Constructs directed graphs via `NetworkX` to detect circular routing and related-party fund transfer anomalies.

---

# 🔒 Privacy

ForensiQ AI is designed with privacy as a core principle:
- No cloud AI services or external document storage
- No API-based LLM inference
- Local vector database and offline document processing
- Offline language model execution

---

# 📄 License

This project is intended for educational, analytical, and research purposes.

---

> **Disclaimer:**  
> ForensiQ AI is an AI-assisted financial analysis and governance research platform. It is intended for educational, analytical, and research purposes only and should not be considered professional financial, investment, legal, or auditing advice.
