import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import joblib
import os
from datetime import datetime

print("Loading dataset...")
df = pd.read_csv("data/creditcard.csv")
print(f"Dataset loaded: {len(df):,} transactions, {df['Class'].sum()} fraud cases")

# Features
X = df.drop(columns=["Class", "Time"])
y = df["Class"]

# Scale Amount
scaler = StandardScaler()
X["Amount"] = scaler.fit_transform(X[["Amount"]])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# SMOTE
print("Applying SMOTE...")
sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)
print(f"After SMOTE: {sum(y_train_res==0):,} legitimate, {sum(y_train_res==1):,} fraud")

# Train model
print("Training XGBoost...")
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    scale_pos_weight=100,
    eval_metric='auc',
    random_state=42,
    use_label_encoder=False
)
model.fit(X_train_res, y_train_res)

# Find best threshold
y_probs = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_probs)
print(f"AUC-ROC: {auc:.4f}")

best_threshold = 0.3
best_f1 = 0
from sklearn.metrics import f1_score
for t in np.arange(0.1, 0.9, 0.01):
    preds = (y_probs >= t).astype(int)
    f1 = f1_score(y_test, preds)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = t

print(f"Best threshold: {best_threshold:.2f} | Best F1: {best_f1:.4f}")
y_pred = (y_probs >= best_threshold).astype(int)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("model", exist_ok=True)
model_data = {
    "model": model,
    "scaler": scaler,
    "threshold": best_threshold,
    "auc_score": round(auc, 4),
    "train_date": datetime.now().strftime("%Y-%m-%d")
}
joblib.dump(model_data, "model/fraud_model.pkl")
print("Model saved to model/fraud_model.pkl")

# Save sample data
sample = df.sample(n=min(1000, len(df)), random_state=42).copy()
sample["Amount_scaled"] = scaler.transform(sample[["Amount"]])
joblib.dump(sample, "model/sample_data.pkl")
print("Sample data saved to model/sample_data.pkl")
print(f"\nDone. AUC-ROC: {auc:.4f} | Threshold: {best_threshold:.2f}")