import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pytz
import sys
import os

sys.path.append(os.path.dirname(__file__))
from utils.styles import get_css, get_colors
from utils.predictor import get_batch, load_model

# Page config
st.set_page_config(
    page_title="FraudGuard — Transaction Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS
st.markdown(get_css(), unsafe_allow_html=True)
C = get_colors()

# Session state
if "batch" not in st.session_state:
    st.session_state.batch = None
if "threshold" not in st.session_state:
    st.session_state.threshold = None
if "run_count" not in st.session_state:
    st.session_state.run_count = 0

# Load model info
model_data = load_model()
default_threshold = model_data["threshold"] if model_data else 0.3
auc_score = model_data["auc_score"] if model_data else "N/A"
train_date = model_data["train_date"] if model_data else "N/A"

# ── SIDEBAR ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛡️ FraudGuard Controls")
    st.markdown("---")

    st.markdown("**Detection Controls**")
    threshold = st.slider(
        "Alert Sensitivity",
        min_value=0.10,
        max_value=0.90,
        value=default_threshold,
        step=0.01,
        help="Lower = more sensitive, more alerts. Higher = fewer alerts."
    )
    st.caption("Lower = more sensitive | Higher = fewer alerts")

    st.markdown("---")
    st.markdown("**Simulation Controls**")

    batch_size = st.selectbox(
        "Batch Size",
        options=[100, 250, 500, 1000],
        index=2
    )

    run_batch = st.button("⚡ Run New Batch")

    st.markdown("---")
    st.markdown("**Model Info**")
    st.caption(f"Model: XGBoost")
    st.caption(f"AUC-ROC: {auc_score}")
    st.caption(f"Trained: {train_date}")
    st.caption(f"Batch #: {st.session_state.run_count}")

# ── LOAD / REFRESH BATCH ────────────────────────────────────────
if run_batch or st.session_state.batch is None:
    result = get_batch(batch_size)
    if result:
        st.session_state.batch, st.session_state.threshold = result
        st.session_state.run_count += 1

df = st.session_state.batch

# ── HEADER ──────────────────────────────────────────────────────
dubai_tz = pytz.timezone("Asia/Dubai")
dubai_time = datetime.now(dubai_tz).strftime("%H:%M:%S")

st.markdown(f"""
<div class="header-wrap">
    <div>
        <div class="brand-name">🛡️ FraudGuard</div>
        <div class="brand-sub">Transaction Intelligence Platform</div>
    </div>
    <div class="live-wrap">
        <span class="pulse"></span>
        SYSTEM LIVE &nbsp;|&nbsp; Dubai, UAE &nbsp;|&nbsp; {dubai_time}
    </div>
</div>
""", unsafe_allow_html=True)

if df is None:
    st.error("No data loaded. Please check that creditcard.csv is in the data/ folder and you have run train_model.py")
    st.stop()

# Apply threshold filter
df_filtered = df.copy()
df_filtered["Predicted"] = (df_filtered["Fraud Prob"] >= threshold).astype(int)
df_filtered["Status"] = df_filtered.apply(
    lambda r: "🔴 FRAUD" if r["Fraud Prob"] >= threshold
    else ("🟡 REVIEW" if r["Fraud Prob"] >= threshold - 0.15
    else "🟢 CLEAR"), axis=1
)

# Metrics
total = len(df_filtered)
fraud_count = df_filtered["Predicted"].sum()
legit_count = total - fraud_count
fraud_rate = round((fraud_count / total) * 100, 2)
total_amount = df_filtered["Amount"].sum()
fraud_amount = df_filtered[df_filtered["Predicted"] == 1]["Amount"].sum()

# ── ALERT BANNER ────────────────────────────────────────────────
if fraud_rate > 5:
    st.markdown(f"""
    <div class="alert-banner">
        ⚠️ HIGH FRAUD ACTIVITY DETECTED — Fraud rate {fraud_rate}% exceeds normal threshold
    </div>
    """, unsafe_allow_html=True)

# ── KPI CARDS ───────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Total Transactions</div>
        <div class="metric-value blue">{total:,}</div>
        <div class="metric-sub">Transactions analyzed</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card red">
        <div class="metric-label">Fraud Detected</div>
        <div class="metric-value red">{fraud_count:,}</div>
        <div class="metric-sub">{fraud_rate}% fraud rate</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Legitimate</div>
        <div class="metric-value green">{legit_count:,}</div>
        <div class="metric-sub">Transactions cleared</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Volume Processed</div>
        <div class="metric-value">${total_amount:,.2f}</div>
        <div class="metric-sub">Total batch value</div>
    </div>""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card red">
        <div class="metric-label">Amount at Risk</div>
        <div class="metric-value red">${fraud_amount:,.2f}</div>
        <div class="metric-sub">In flagged transactions</div>
    </div>""", unsafe_allow_html=True)

# ── CHART ROW 1 ─────────────────────────────────────────────────
st.markdown('<div class="section-title">Live Analytics</div>', unsafe_allow_html=True)
col1, col2 = st.columns([6, 4])

with col1:
    colors_stream = [C["red"] if p >= threshold else C["green"]
                     for p in df_filtered["Fraud Prob"]]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        y=df_filtered["Fraud Prob"].values,
        mode="lines+markers",
        line=dict(color=C["blue"], width=1.5),
        marker=dict(color=colors_stream, size=4),
        name="Fraud Probability",
        hovertemplate="Transaction %{x}<br>Probability: %{y:.3f}<extra></extra>"
    ))
    fig1.add_hline(
        y=threshold,
        line_dash="dash",
        line_color=C["yellow"],
        annotation_text=f"Threshold ({threshold:.2f})",
        annotation_font_color=C["yellow"]
    )
    fig1.update_layout(
        title=dict(text="Live Fraud Probability Stream", font=dict(color=C["text"], size=14)),
        paper_bgcolor=C["card"],
        plot_bgcolor=C["card"],
        font=dict(color=C["text"]),
        xaxis=dict(gridcolor=C["grid"], showgrid=True, title="Transaction Index"),
        yaxis=dict(gridcolor=C["grid"], showgrid=True, title="Fraud Probability", range=[0, 1]),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with col2:
    fig2 = go.Figure(go.Pie(
        labels=["Legitimate", "Fraud"],
        values=[legit_count, fraud_count],
        hole=0.65,
        marker=dict(colors=[C["green"], C["red"]],
                    line=dict(color=C["card"], width=2)),
        textinfo="none",
        hovertemplate="%{label}: %{value}<extra></extra>"
    ))
    fig2.add_annotation(
        text=f"{fraud_rate}%<br><span style='font-size:10px'>Fraud</span>",
        x=0.5, y=0.5,
        font=dict(size=20, color=C["red"]),
        showarrow=False
    )
    fig2.update_layout(
        title=dict(text="Transaction Split", font=dict(color=C["text"], size=14)),
        paper_bgcolor=C["card"],
        plot_bgcolor=C["card"],
        font=dict(color=C["text"]),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=True,
        legend=dict(
            font=dict(color=C["text"]),
            bgcolor=C["card"]
        )
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ── CHART ROW 2 ─────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    legit_amounts = df_filtered[df_filtered["Predicted"] == 0]["Amount"]
    fraud_amounts = df_filtered[df_filtered["Predicted"] == 1]["Amount"]

    fig3 = go.Figure()
    fig3.add_trace(go.Histogram(
        x=legit_amounts,
        name="Legitimate",
        marker_color=C["blue"],
        opacity=0.65,
        nbinsx=40
    ))
    fig3.add_trace(go.Histogram(
        x=fraud_amounts,
        name="Fraud",
        marker_color=C["red"],
        opacity=0.85,
        nbinsx=40
    ))
    fig3.update_layout(
        barmode="overlay",
        title=dict(text="Amount Distribution", font=dict(color=C["text"], size=14)),
        paper_bgcolor=C["card"],
        plot_bgcolor=C["card"],
        font=dict(color=C["text"]),
        xaxis=dict(gridcolor=C["grid"], title="Amount (USD)"),
        yaxis=dict(gridcolor=C["grid"], title="Count", type="log"),
        height=280,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(font=dict(color=C["text"]), bgcolor=C["card"])
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with col4:
    hourly = df_filtered[df_filtered["Predicted"] == 1].groupby("Hour").size().reset_index()
    hourly.columns = ["Hour", "Fraud Count"]
    all_hours = pd.DataFrame({"Hour": range(24)})
    hourly = all_hours.merge(hourly, on="Hour", how="left").fillna(0)

    fig4 = go.Figure(go.Bar(
        x=hourly["Hour"],
        y=hourly["Fraud Count"],
        marker=dict(
            color=hourly["Fraud Count"],
            colorscale=[[0, C["blue"]], [0.5, C["yellow"]], [1, C["red"]]],
            showscale=False
        ),
        hovertemplate="Hour %{x}:00<br>Fraud Cases: %{y}<extra></extra>"
    ))
    fig4.update_layout(
        title=dict(text="Fraud Activity by Hour", font=dict(color=C["text"], size=14)),
        paper_bgcolor=C["card"],
        plot_bgcolor=C["card"],
        font=dict(color=C["text"]),
        xaxis=dict(gridcolor=C["grid"], title="Hour of Day (24h)", dtick=2),
        yaxis=dict(gridcolor=C["grid"], title="Fraud Cases"),
        height=280,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ── TRANSACTION TABLE ────────────────────────────────────────────
st.markdown('<div class="section-title">Transaction Monitor</div>', unsafe_allow_html=True)

search = st.text_input("", placeholder="🔍 Search Transaction ID...", label_visibility="collapsed")

display_df = df_filtered.copy()
if search:
    display_df = display_df[display_df["Transaction ID"].str.contains(search.upper())]

display_df = display_df[[
    "Transaction ID", "Time", "Amount", "Risk Score", "Status", "Actual"
]].head(50)

display_df["Amount"] = display_df["Amount"].apply(lambda x: f"${x:,.2f}")
display_df["Risk Score"] = display_df["Risk Score"].apply(lambda x: f"{x:.1f}%")
display_df = display_df.rename(columns={"Actual": "Actual Class"})
display_df["Actual Class"] = display_df["Actual Class"].map({0: "✅ Legitimate", 1: "⚠️ Fraud"})

def style_rows(row):
    if "FRAUD" in str(row["Status"]):
        return ["background-color: rgba(239,68,68,0.08); color: #F9FAFB"] * len(row)
    elif "REVIEW" in str(row["Status"]):
        return ["background-color: rgba(245,158,11,0.05); color: #F9FAFB"] * len(row)
    else:
        return ["color: #F9FAFB"] * len(row)

styled = display_df.style.apply(style_rows, axis=1).set_properties(**{
    "background-color": C["card"],
    "color": C["text"],
    "border": f"1px solid {C['border']}"
})

st.dataframe(styled, use_container_width=True, height=400)

# ── FOOTER ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<div style='text-align:center; color:#9CA3AF; font-size:0.75rem;'>"
    f"FraudGuard v1.0 &nbsp;|&nbsp; Built with XGBoost & Streamlit &nbsp;|&nbsp; "
    f"Dataset: 284,807 transactions &nbsp;|&nbsp; Model AUC-ROC: {auc_score}"
    f"</div>",
    unsafe_allow_html=True
)