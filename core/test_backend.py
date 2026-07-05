# test_backend.py
import json
import requests
from core.api_connector import MarketDataEngine

print("========================================================")
print("     BACKEND ENGINE METRICS VERIFICATION RUN            ")
print("========================================================")

# 1. Verify market data engine returns the new unique calculated profiles
for test_ticker in ["TCS", "INFY", "MARICO", "PATELENG"]:
    print(f"\n[*] Fetching data for: {test_ticker}")
    try:
        engine = MarketDataEngine(test_ticker)
        profile = engine.get_profile()
        print(f"[+] Success! Ticker: {profile['ticker']}")
        print(f"    Company Name: {profile['company_name']}")
        print(f"    Ratios Extracted: {json.dumps(profile['forensic_ratio_matrix'], indent=2)}")
    except Exception as e:
        print(f"[X] Failed for {test_ticker}: {str(e)}")

print("\n========================================================")
print("Testing Local Ollama LLM Connection...")
try:
    payload = {
        "model": "llama3.1:8b",
        "messages": [{"role": "user", "content": "Ping"}],
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=5)
    if response.status_code == 200:
        print("[+] Ollama AI Server is alive and responding perfectly!")
    else:
        print(f"[!] Ollama returned status code: {response.status_code}")
except Exception as e:
    print(f"[X] Ollama connection failed. Is 'ollama run llama3.1:8b' running in another window? Error: {str(e)}")