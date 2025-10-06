import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

df = pd.read_csv("data/customers_clean.csv")

df.ffill(inplace=True)
if 'Churn' not in df.columns:
    raise ValueError("Target column 'Churn' not found.")

if df['gender'].dtype == object:
    df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})

X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

os.makedirs("processed", exist_ok=True)
joblib.dump((X_train_scaled, X_test_scaled, y_train, y_test), "processed/data_split.pkl")
joblib.dump(scaler, "processed/scaler.pkl")
