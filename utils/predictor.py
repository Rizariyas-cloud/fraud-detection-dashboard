import pandas as pd
import numpy as np
import joblib
import streamlit as st
import random
import string
from datetime import datetime, timedelta

@st.cache_resource
def load_model():
    try:
        return joblib.load("model/fraud_model.pkl")
    except Exception as e:
        st.error(f"Model not found. Run train_model.py first. Error: {e}")
        return None

@st.cache_data
def load_sample_data():
    try:
        return joblib.load("model/sample_data.pkl")
    except Exception as e:
        st.error(f"Sample data not found. Run train_model.py first. Error: {e}")
        return None

def generate_txn_id():
    return "TXN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_timestamp():
    now = datetime.now()
    delta = timedelta(seconds=random.randint(0, 86400))
    t = now - delta
    return t.strftime("%H:%M:%S"), t.hour

def get_batch(n=500):
    model_data = load_model()
    sample_data = load_sample_data()

    if model_data is None or sample_data is None:
        return None

    model = model_data["model"]
    scaler = model_data["scaler"]
    threshold = model_data["threshold"]

    # Sample transactions
    batch = sample_data.sample(n=min(n, len(sample_data)), replace=True).copy()

    # Prepare features
    feature_cols = [c for c in batch.columns if c.startswith("V")] + ["Amount_scaled"]
    X = batch[feature_cols].copy()
    X = X.rename(columns={"Amount_scaled": "Amount"})

    # Handle missing V columns
    expected_cols = [f"V{i}" for i in range(1, 29)] + ["Amount"]
    for col in expected_cols:
        if col not in X.columns:
            X[col] = 0
    X = X[expected_cols]

    # Predict
    probs = model.predict_proba(X)[:, 1]

    # Build result dataframe
    results = []
    for i, (idx, row) in enumerate(batch.iterrows()):
        prob = probs[i]
        time_str, hour = generate_timestamp()
        pred = 1 if prob >= threshold else 0

        if pred == 1:
            status = "🔴 FRAUD"
        elif prob >= (threshold - 0.15):
            status = "🟡 REVIEW"
        else:
            status = "🟢 CLEAR"

        results.append({
            "Transaction ID": generate_txn_id(),
            "Time": time_str,
            "Hour": hour,
            "Amount": round(row["Amount"], 2),
            "Risk Score": round(prob * 100, 1),
            "Fraud Prob": round(prob, 4),
            "Status": status,
            "Predicted": pred,
            "Actual": int(row["Class"])
        })

    df = pd.DataFrame(results)
    df = df.sort_values("Risk Score", ascending=False).reset_index(drop=True)
    return df, threshold