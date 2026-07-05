# core/pdf_parser.py
import os
import pdfplumber
import math
from sentence_transformers import SentenceTransformer

class ForensicPDFParser:
    def __init__(self):
        self.embedding_model = None
        self.vector_database = []  # Pure Python in-memory storage array

    def _lazy_load_model(self):
        if self.embedding_model is None:
            print("[*] Initializing local semantic embedding matrix (all-MiniLM-L6-v2)...")
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def process_and_index_pdf(self, uploaded_file) -> str:
        """Parses a PDF file stream and populates an in-memory vector dictionary."""
        self._lazy_load_model()
        print(f"[*] Parsing multi-page document framework semantically...")
        full_text = ""
        
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        full_text += f"\n[Page {idx+1}]\n" + text
            
            if not full_text.strip():
                return "ALERT: The uploaded document layer contains zero readable text structures (Scanned/Image PDF)."

            # Simple, effective text segmenter to bypass langchain-text-splitters errors
            paragraphs = [p.strip() for p in full_text.split("\n\n") if len(p.strip()) > 40]
            print(f"[+] Document fragmented cleanly into {len(paragraphs)} paragraphs.")
            
            # Clear old memory matrix
            self.vector_database = []
            
            # Generate local math coordinate embeddings
            embeddings = self.embedding_model.encode(paragraphs).tolist()
            
            for doc_text, embedding in zip(paragraphs, embeddings):
                self.vector_database.append({
                    "text": doc_text,
                    "vector": embedding
                })
                
            return f"Success: Pure-Python vector registry active. Formatted {len(paragraphs)} nodes cleanly."
            
        except Exception as e:
            return f"Document Processing Fault: {str(e)}"

    def query_semantic_anomalies(self, target_query: str = "related party transactions loans asset tunneling advances un-audited") -> str:
        """Executes a pure-math cosine similarity scan across internal memory structures."""
        if not self.vector_database:
            return "NO DISCLOSURES SUBMITTED: The research database is currently empty. No annual report PDF has been parsed yet."
            
        try:
            self._lazy_load_model()
            query_vector = self.embedding_model.encode([target_query])[0].tolist()
            
            scored_paragraphs = []
            for node in self.vector_database:
                # Direct pure-math implementations of vector dot product cosine calculations
                v1, v2 = query_vector, node["vector"]
                dot_prod = sum(a * b for a, b in zip(v1, v2))
                mag1 = math.sqrt(sum(a * a for a in v1))
                mag2 = math.sqrt(sum(b * b for b in v2))
                similarity = dot_prod / (mag1 * mag2) if (mag1 * mag2) > 0 else 0
                scored_paragraphs.append((similarity, node["text"]))
                
            # Pick top 3 most relevant accounting text alignments
            scored_paragraphs.sort(key=lambda x: x[0], reverse=True)
            top_matches = [text for score, text in scored_paragraphs[:3]]
            
            return "\n\n---\n\n".join(top_matches)[:3500]
        except Exception as e:
            return f"Search anomaly triggered: {str(e)}"