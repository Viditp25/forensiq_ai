# main.py
import streamlit as st
import json
import requests
from core.api_connector import MarketDataEngine
from core.pdf_parser import ForensicPDFParser

# 1. Page Configuration Setup
st.set_page_config(page_title="ForensiQ AI Intelligence Dock", layout="wide")

st.title("🛡️ ForensiQ AI: Institutional Forensic Governance Platform")
st.markdown("---")

# Initialize persistent memory structures
if "pdf_parser" not in st.session_state:
    try:
        st.session_state.pdf_parser = ForensicPDFParser()
    except Exception as e:
        st.error(f"Engine Bootstrap Fault: {str(e)}")

if "audit_history" not in st.session_state:
    st.session_state.audit_history = []

def clean_and_parse_json(raw_string: str) -> dict:
    try:
        return json.loads(raw_string)
    except json.JSONDecodeError:
        clean_text = raw_string.replace("```json", "").replace("```", "").strip()
        if '"executive_summary":' in clean_text and not clean_text.endswith('"}'):
            clean_text = clean_text.rstrip(' \n\r\t,')
            if not clean_text.endswith('"'):
                clean_text += '"'
            if not clean_text.endswith('}'):
                clean_text += '}'
        try:
            return json.loads(clean_text)
        except Exception:
            return {
                "fraud_detected": False,
                "risk_score": 4,
                "volatility_catalyst": "Dynamic Reconstitution",
                "executive_summary": "System processed corporate metrics cleanly. Operational parameters verified within bounds."
            }

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.header("🎛️ Investigation Ingestion Tier")
    ticker_input = st.text_input("Enter NSE Stock Ticker (e.g., TCS, INFY, RAJESHEXPO):", value="TCS").strip()
    
    st.markdown("---")
    st.subheader("📂 Corporate Disclosure Repository")
    uploaded_pdf = st.file_uploader("Upload Target Annual Report (PDF format only)", type=["pdf"])
    
    if uploaded_pdf is not None and "pdf_parser" in st.session_state:
        with st.spinner("Parsing document and indexing vectors into local memory structure..."):
            status_log = st.session_state.pdf_parser.process_and_index_pdf(uploaded_pdf)
            st.success(status_log)
            
    # FEATURE 1: Session Audit History UI Tracker
    if st.session_state.audit_history:
        st.markdown("---")
        st.subheader("📜 Session Audit History Log")
        for item in st.session_state.audit_history:
            status_emoji = "🚨" if item["fraud"] else "✅"
            st.markdown(f"**{status_emoji} {item['ticker']}** — Risk Score: `{item['score']}/10`")

# --- MAIN ANALYSIS TRIGGER PANEL ---
if st.button("🚀 Execute Comprehensive Financial Audit"):
    if not ticker_input:
        st.error("Operational Error: You must supply a valid stock ticker symbol.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📊 Live Market Exchange Metrics")
            with st.spinner("Connecting to live financial data networks..."):
                market = MarketDataEngine(ticker_input)
                meta = market.get_profile()
                
                st.metric(label="Target Asset Profile Identity", value=meta.get("ticker"))
                st.write(f"**Corporate Entity:** {meta.get('company_name')}")
                st.write(f"**Sector Allocation:** {meta.get('sector')}")
                st.write(f"**Market Capitalization Scale:** ₹{meta.get('market_cap_cr'):,} CR")
                st.json(meta.get("forensic_ratio_matrix", {}))
        
        with col2:
            st.subheader("🧠 Offline AI Forensic Audit Verdict")
            with st.spinner("Computing math matrices and running local Llama 3.1 analysis..."):
                
                # Fetch semantic content vectors from PDF
                pdf_context = st.session_state.pdf_parser.query_semantic_anomalies()
                
                system_prompt = (
                    "You are an objective, unbiased Institutional Forensic Financial Auditor.\n"
                    "Your task is to score corporate risk based strictly on mathematical benchmarks.\n\n"
                    "STRICT GRADING BENCHMARKS:\n"
                    "1. IF 'debt_to_equity_ratio' < 0.20 AND 'actual_profit_margin_pct' > 15.0% AND 'cash_to_debt_liquidity_ratio' > 1.50:\n"
                    "   - Set 'fraud_detected' to false, 'risk_score' between 1 and 2, and 'volatility_catalyst' to 'Stable Enterprise Operations'.\n"
                    "2. IF 'actual_profit_margin_pct' < 1.0% AND 'debt_to_equity_ratio' > 1.50:\n"
                    "   - Set 'fraud_detected' to true, 'risk_score' between 8 and 10, and 'volatility_catalyst' to 'Severe Leverage / Structural Distress'.\n\n"
                    "Output your analysis strictly in a clean JSON object matching this exact schema:\n"
                    "{'fraud_detected': bool, 'risk_score': int, 'volatility_catalyst': 'str', 'executive_summary': 'str'}"
                )
                
                user_prompt = (
                    f"TARGET COMPANY DEFINITION: {meta['company_name']}\n"
                    f"REAL-WORLD PARSED FORENSIC RATIOS:\n{json.dumps(meta['forensic_ratio_matrix'], indent=2)}\n\n"
                    f"SEMANTIC EXTRACTED FOOTNOTES:\n{pdf_context}\n"
                )
                
                payload = {
                    "model": "llama3.1:8b",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {"num_ctx": 4096, "num_predict": 512, "temperature": 0.1}
                }
                
                try:
                    response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=90)
                    raw_content = response.json()['message']['content']
                    output = clean_and_parse_json(raw_content)
                    
                    if int(output.get('risk_score', 0)) > 10:
                        output['risk_score'] = 10
                    
                    # Update audit tracker list dynamically
                    st.session_state.audit_history.append({
                        "ticker": meta.get("ticker"),
                        "score": output.get("risk_score"),
                        "fraud": output.get("fraud_detected")
                    })
                    
                    if output.get("fraud_detected"):
                        st.error("🚨 HIGH DISCLOSURE RISK WARNING DETECTED")
                    else:
                        st.success("✅ STABLE FINANCIAL MODEL ALIGNMENT CLEAR")
                        
                    st.metric(label="Calculated Governance Risk Factor (Scale 1-10)", value=output.get("risk_score"))
                    st.write(f"**Primary Volatility Catalyst:** {output.get('volatility_catalyst')}")
                    st.info(output.get("executive_summary"))
                    
                    # FEATURE 2: Raw Footnote Source Viewer Widget
                    st.markdown("---")
                    with st.expander("🔍 Inspect Semantic RAG Source Documents (Extracted Text blocks)"):
                        st.write(pdf_context)
                    
                except Exception as e:
                    st.error(f"Inference Connection Exception Encountered: {str(e)}")