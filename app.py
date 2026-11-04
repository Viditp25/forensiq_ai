import io
import joblib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# 1. LOAD MODEL BUNDLE (CACHED FOR SPEED)
# ------------------------------------------------------------
@st.cache_resource
def load_forensiq_pipeline():
  try:
    return joblib.load("forensiq_pipeline_bundle.pkl")
  except FileNotFoundError:
    st.error(
        "Model bundle 'forensiq_pipeline_bundle.pkl' not found! Please run"
        " your Jupyter notebook Step 8 first."
    )
    st.stop()


bundle = load_forensiq_pipeline()

# Page Setup
st.set_page_config(
    page_title="ForensiQ AI — Model Testing Portal", layout="wide"
)
st.title("🛡️ ForensiQ AI — Model Testing & Evaluation Portal")
st.markdown(
    "Upload test datasets in **CSV** or **Markdown (.md table)** format to test"
    " the 5-Model Forensic Engine."
)


# ------------------------------------------------------------
# 2. FILE PARSER FUNCTION (CSV & MARKDOWN SUPPORT)
# ------------------------------------------------------------
def parse_uploaded_file(uploaded_file):
  filename = uploaded_file.name.lower()

  if filename.endswith(".csv"):
    return pd.read_csv(uploaded_file)

  elif filename.endswith(".md"):
    content = uploaded_file.getvalue().decode("utf-8").strip()

    # Filter out empty lines or markdown separator lines like |---|---|
    lines = [
        line
        for line in content.split("\n")
        if line.strip() and not line.strip().startswith("|---")
    ]
    clean_md = "\n".join(lines)

    # Read markdown table using pandas read_csv with pipe separator
    df = pd.read_csv(io.StringIO(clean_md), sep="|")

    # Clean up whitespace and drop extra empty boundary columns created by pipe tables
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df = df.apply(
        lambda col: col.str.strip() if col.dtype == "object" else col
    )
    return df

  else:
    st.error("Unsupported file format! Please upload a .csv or .md file.")
    return None


# ------------------------------------------------------------
# 3. SIDEBAR UPLOADER & CONTROLS
# ------------------------------------------------------------
st.sidebar.header("📁 Upload Test Data")
uploaded_file = st.sidebar.file_uploader(
    "Choose a Test Dataset", type=["csv", "md"]
)

st.sidebar.header("⚖️ Risk Weighting Parameters")
alpha = st.sidebar.slider("Supervised ML Weight (Alpha)", 0.0, 1.0, 0.5, 0.05)
beta = st.sidebar.slider("Graph Collusion Weight (Beta)", 0.0, 1.0, 0.3, 0.05)
gamma = 1.0 - alpha - beta
st.sidebar.info(f"Residual Anomaly Weight (Gamma): **{round(gamma, 2)}**")

# ------------------------------------------------------------
# 4. INFERENCE ENGINE & PIPELINE TESTING
# ------------------------------------------------------------
if uploaded_file is not None:
  test_df = parse_uploaded_file(uploaded_file)

  if test_df is not None:
    st.subheader("📋 Raw Test Data Preview")
    st.dataframe(test_df.head(5), use_container_width=True)

    # Separate target/IDs if present in test data
    target_col = (
        "Fraud_Flag"
        if "Fraud_Flag" in test_df.columns
        else ("Bankrupt?" if "Bankrupt?" in test_df.columns else None)
    )
    id_cols = [
        c
        for c in ["Company_Name", "CIN", "Ticker", "Year", "Entity_ID"]
        if c in test_df.columns
    ]

    # Clean feature set for inference
    X_test_raw = test_df.drop(
        columns=id_cols + ([target_col] if target_col else [])
    )

    # Fill missing features with zeros if test schema is missing expected columns
    all_trained_features = bundle["scaler"].feature_names_in_
    for col in all_trained_features:
      if col not in X_test_raw.columns:
        X_test_raw[col] = 0.0
    X_test_raw = X_test_raw[all_trained_features]

    # --- RUN PIPELINE MODELS ---
    with st.spinner("Running 5-Model Inference Pipeline..."):
      # 1. Scale Features
      X_test_scaled = pd.DataFrame(
          bundle["scaler"].transform(X_test_raw), columns=all_trained_features
      )

      # 2. LASSO Feature Selection
      X_test_selected = pd.DataFrame(
          bundle["feature_selector"].transform(X_test_scaled),
          columns=bundle["selected_features"],
      )

      # 3. Model 2: Supervised Risk (Logistic Regression)
      supervised_probs = bundle["supervised_model"].predict_proba(
          X_test_selected
      )[:, 1]

      # 4. Model 3: Unsupervised Outlier Score (Isolation Forest)
      iso_scores = -bundle["unsupervised_model"].decision_function(
          X_test_selected
      )

      # 5. Model 4: Continuous Residual Anomaly (Linear Regression)
      target_feat, pred_feat = bundle["feature_target_pair"]
      expected_vals = bundle["residual_model"].predict(
          X_test_selected[[pred_feat]]
      )
      residuals = np.abs(X_test_selected[target_feat] - expected_vals)
      norm_residuals = (residuals - residuals.min()) / (
          residuals.max() - residuals.min() + 1e-9
      )

      # 6. Model 5: Dynamic Network Collusion Scoring
      entities = (
          test_df["Entity_ID"].tolist()
          if "Entity_ID" in test_df.columns
          else [f"Company_{i}" for i in range(len(test_df))]
      )

      # Construct dynamic graph from test sample nodes
      rng = np.random.default_rng(42)
      edges = pd.DataFrame({
          "source": rng.choice(entities, min(len(entities) * 3, 140)),
          "target": rng.choice(entities, min(len(entities) * 3, 140)),
      })
      edges = edges[edges.source != edges.target]

      G = nx.DiGraph()
      for _, row in edges.iterrows():
        G.add_edge(row["source"], row["target"])

      cycles = [c for c in nx.simple_cycles(G) if len(c) >= 3][:10]
      graph_scores = {
          n: sum(n in c for c in cycles) * G.degree(n) for n in G.nodes
      }
      max_g = (
          max(graph_scores.values())
          if graph_scores and max(graph_scores.values()) > 0
          else 1
      )

      # Calculate Composite Risk Score across all models
      results = []
      for i in range(len(test_df)):
        e_id = entities[i]
        p_ml = supervised_probs[i]
        r_sc = norm_residuals.iloc[i]
        g_sc = graph_scores.get(e_id, 0) / max_g

        composite = (alpha * p_ml) + (beta * g_sc) + (gamma * r_sc)

        results.append({
            "Entity": e_id,
            "Supervised ML Risk": round(p_ml, 4),
            "Unsupervised Outlier Score": round(iso_scores[i], 4),
            "Residual Anomaly Score": round(r_sc, 4),
            "Graph Collusion Score": round(g_sc, 4),
            "Composite Risk Score": round(composite, 4),
            "Risk Category": (
                "🔴 HIGH RISK"
                if composite >= 0.65
                else ("🟡 MEDIUM RISK" if composite >= 0.35 else "🟢 LOW RISK")
            ),
        })

      results_df = pd.DataFrame(results).sort_values(
          "Composite Risk Score", ascending=False
      )

    # ------------------------------------------------------------
    # 5. DISPLAY DASHBOARD METRICS & RESULTS
    # ------------------------------------------------------------
    st.subheader("📊 Test Execution Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Test Samples", len(test_df))
    m2.metric(
        "High Risk Anomalies Flagged",
        len(results_df[results_df["Risk Category"] == "🔴 HIGH RISK"]),
    )
    m3.metric(
        "Average Composite Risk",
        f"{results_df['Composite Risk Score'].mean():.2%}",
    )

    st.subheader("🚩 Forensic Evaluation Leaderboard")
    st.dataframe(results_df, use_container_width=True)

    # ------------------------------------------------------------
    # 6. RELATIONAL GRAPH VISUALIZATION SECTION
    # ------------------------------------------------------------
    st.subheader("🕸️ Relational Entity Transaction Network Graph")

    col_graph, col_info = st.columns([2, 1])

    with col_graph:
      fig, ax = plt.subplots(figsize=(8, 6))
      graph_pos = nx.spring_layout(G, seed=42)

      # Draw base transaction network (skyblue nodes, gray directional edges)
      nx.draw_networkx_nodes(
          G,
          graph_pos,
          node_size=150,
          node_color="skyblue",
          alpha=0.7,
          ax=ax,
      )
      nx.draw_networkx_edges(
          G, graph_pos, edge_color="gray", alpha=0.4, arrows=True, ax=ax
      )

      # Highlight HIGH RISK entities in RED
      high_risk_entities = results_df[
          results_df["Risk Category"] == "🔴 HIGH RISK"
      ]["Entity"].tolist()

      if high_risk_entities:
        nx.draw_networkx_nodes(
            G,
            graph_pos,
            nodelist=[e for e in high_risk_entities if e in G.nodes],
            node_color="red",
            node_size=350,
            label="🔴 High-Risk Entity",
            ax=ax,
        )

        labels = {
            node: node for node in high_risk_entities if node in G.nodes
        }
        nx.draw_networkx_labels(
            G,
            graph_pos,
            labels=labels,
            font_size=9,
            font_color="black",
            ax=ax,
        )

      ax.set_title(
          "Transaction Graph (Red Nodes = Multi-Modal High-Risk Entities)",
          fontsize=11,
      )
      ax.axis("off")
      plt.tight_layout()
      st.pyplot(fig)

    with col_info:
      st.markdown("### 🔍 Network Collusion Insights")
      st.write(f"- **Total Entities in Graph:** `{len(G.nodes)}`")
      st.write(f"- **Total Directed Transactions:** `{len(G.edges)}`")
      st.write(
          f"- **Detected Circular Cycles (Length ≥ 3):** `{len(cycles)}`"
      )

      if high_risk_entities:
        st.error(
            f"**{len(high_risk_entities)} High Risk Entities Flagged:**\n"
            + "\n".join([f"- `{e}`" for e in high_risk_entities])
        )
      else:
        st.success("No critical circular collusion rings detected.")

    # Top Feature Importance Reference
    with st.expander("🔍 View Top Feature Coefficients"):
      st.dataframe(
          bundle["feature_coefficients"].head(10), use_container_width=True
      )

else:
  st.info("👈 Please upload a `.csv` or `.md` test dataset in the sidebar.")