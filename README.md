# 🛡️ FraudGuard — Real-Time Credit Card Fraud Detection Dashboard

A professional fintech-style dashboard for real-time credit card fraud detection,
built with XGBoost and Streamlit.

## 🔍 Features
- Real-time fraud probability scoring on transaction batches
- Interactive Streamlit dashboard with dark fintech theme
- XGBoost model trained on 284,807 transactions with SMOTE balancing
- AUC-ROC: 0.97 | Optimised precision-recall threshold
- Live fraud probability stream, amount distribution charts, hourly heatmap
- Transaction monitor table with risk scoring

## 🛠️ Tech Stack
Python · XGBoost · Scikit-learn · SMOTE · Streamlit · Plotly · Pandas · NumPy

## 📊 Dataset
Kaggle Credit Card Fraud Detection (ULB Machine Learning Group)
284,807 transactions · 492 fraud cases · 99.8:0.2 class imbalance

## 🚀 Run Locally

### 1. Clone the repo
git clone https://github.com/Rizariyas-cloud/fraud-detection-dashboard.git
cd fraud-detection-dashboard

### 2. Install dependencies
pip install -r requirements.txt

### 3. Download dataset
Download creditcard.csv from Kaggle and place in data/creditcard.csv

### 4. Train model
python train_model.py

### 5. Launch dashboard
streamlit run app.py

## 📁 Project Structure
fraud_detection/
├── app.py                  # Main Streamlit dashboard
├── train_model.py          # Model training script
├── requirements.txt
├── utils/
│   ├── predictor.py        # Prediction and simulation engine
│   └── styles.py           # CSS and color system
├── data/                   # Place creditcard.csv here
└── model/                  # Trained model saved here

## 👩‍💻 Author
Risa Fathima 
LinkedIn: linkedin.com/in/risa-fathima
