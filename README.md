# 🛡️ ForensiQ AI
### Institutional Forensic Governance Platform

> **Developer:** Vidit Palarpwar  

---

## 📖 Overview

**ForensiQ AI** is an intelligent forensic financial audit platform that performs AI-assisted governance analysis on publicly available corporate information. The application combines financial market data, corporate PDF reports, semantic search, and a local large language model to generate structured financial risk assessments while ensuring complete data privacy.

Unlike cloud-based AI audit platforms, ForensiQ AI executes entirely on a local machine. Sensitive corporate documents, embeddings, and inference remain offline, making it suitable for privacy-conscious financial analysis and academic research.

The platform enables users to:

- Analyze listed companies using stock ticker symbols
- Upload annual reports, 10-K filings, or financial statements
- Build a local semantic knowledge base from uploaded documents
- Retrieve context using vector similarity search
- Generate structured governance and risk reports using a local LLM
- Operate without external AI APIs or cloud storage

---

# ✨ Features

- 📄 Upload and analyze corporate PDF reports
- 📈 Fetch live financial market information using stock tickers
- 🧠 Semantic document retrieval using vector embeddings
- 🤖 Offline AI-powered forensic financial auditing
- 🔒 Fully local execution with no cloud dependency
- 📊 Structured governance and risk scoring
- 📑 Interactive audit reports
- ⚡ Lightweight pure-Python vector database implementation
- 🛠️ Deterministic JSON output with automatic recovery from malformed responses

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
   Financial Data                   Corporate PDF
      Retrieval                       Ingestion
            │                                │
            └───────────────┬────────────────┘
                            ▼
                  Text Extraction
                    (pdfplumber)
                            │
                            ▼
                 Sentence Embeddings
            (sentence-transformers)
                            │
                            ▼
               Local Vector Database
          (Pure Python Cosine Similarity)
                            │
                            ▼
                  Context Retrieval
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
├── main.py
├── requirements.txt
├── README.md
│
├── assets/
│
├── data/
│   ├── uploaded_reports/
│   └── vector_store/
│
├── models/
│
├── utils/
│   ├── parser.py
│   ├── embeddings.py
│   ├── vector_db.py
│   ├── audit_engine.py
│   └── llm.py
│
└── pages/
```

---

# 🚀 Installation

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
sentence-transformers \
requests \
pydantic \
pdfplumber \
torch \
torchvision \
--index-url https://download.pytorch.org/whl/cpu
```

---

## 3. Start the Local LLM

Install Ollama if it is not already installed.

Pull the model:

```bash
ollama pull llama3.1:8b
```

Run the model:

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

# 📊 How to Use

## Step 1 — Enter a Stock Ticker

Provide a valid equity ticker in the sidebar.

Examples:

- TCS
- INFY
- RELIANCE
- PATELENG

---

## Step 2 — Upload Financial Reports *(Optional)*

Upload one or more corporate documents such as:

- Annual Reports
- 10-K Filings
- Quarterly Reports
- Investor Presentations

The uploaded PDFs are parsed and indexed into the local semantic vector database.

---

## Step 3 — Execute the Audit

Click:

```
Execute Comprehensive Financial Audit
```

The system will:

1. Retrieve financial metrics
2. Extract relevant document sections
3. Perform semantic similarity search
4. Generate structured governance insights using the local LLM
5. Display an interactive financial risk assessment

---

# ⚙️ Audit Pipeline

```
User Input
     │
     ▼
Ticker + PDF
     │
     ▼
Financial Data Collection
     │
     ▼
PDF Text Extraction
     │
     ▼
Embedding Generation
     │
     ▼
Vector Similarity Search
     │
     ▼
Context Assembly
     │
     ▼
Llama 3.1 (Offline)
     │
     ▼
JSON Audit Report
     │
     ▼
Interactive Dashboard
```

---

# 🧠 Core Components

## Financial Data Ingestion

Retrieves market information associated with the selected stock ticker to provide contextual financial indicators for analysis.

---

## Document Processing

Corporate reports are parsed using **pdfplumber**, segmented into manageable chunks, and transformed into semantic embeddings.

---

## Semantic Vector Engine

A lightweight custom vector database built entirely in Python performs cosine similarity calculations for context retrieval without external vector database dependencies.

---

## Local AI Inference

Relevant document context is supplied to an offline **Llama 3.1 8B** model running through Ollama to generate deterministic governance assessments.

---

# 🔒 Privacy

ForensiQ AI is designed with privacy as a core principle.

- No cloud AI services
- No external document storage
- No API-based LLM inference
- Local vector database
- Offline document processing
- Offline language model execution

All processing remains on the user's machine.

---

# 💡 Key Design Decisions

### Pure Python Vector Database

A custom cosine similarity implementation replaces traditional vector databases, improving compatibility with Python 3.13 while avoiding native binary dependencies.

---

### Deterministic LLM Prompting

The audit engine applies fixed system instructions and constrained scoring logic to improve consistency and reduce hallucinations.

---

### JSON Recovery Layer

A post-processing module automatically repairs malformed JSON responses generated by quantized local models, ensuring reliable rendering within the Streamlit interface.

---

# 📌 Future Enhancements

- Multi-document knowledge graph
- Comparative company benchmarking
- Financial trend visualization
- Historical audit tracking
- Automated anomaly detection
- Multi-model local inference support
- Export reports as PDF
- RAG optimization with hybrid search

---

# 📷 Screenshots

Add screenshots of the following:

- Dashboard
- PDF Upload
- Audit Report
- Risk Analysis
- Governance Summary

---

# 🤝 Contributing

Contributions are welcome.

To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

# 📄 License

This project is intended for educational and research purposes.

---

> **Disclaimer:**  
> ForensiQ AI is an AI-assisted financial analysis and governance research platform. It is intended for educational, analytical, and research purposes only and should not be considered professional financial, investment, legal, or auditing advice.
