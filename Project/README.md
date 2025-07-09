# 🧠 Customer Churn Prediction Pipeline (End-to-End MLOps)

This project implements a complete MLOps workflow to predict customer churn using a Random Forest and Logistic Regression model.
The system includes data preprocessing, model training, and a production-ready Flask API served via Docker.

---

## 📊 Problem Statement

Customer churn prediction helps businesses identify which customers are likely to stop using their service.
Predicting churn enables targeted retention strategies, improving customer lifetime value.

---

## 🏗️ Project Structure

Project/
├── app.py # Flask API for serving predictions
├── preprocess.py # Data cleaning and feature processing
├── train.py # Model training and saving
├── requirements.txt # Python dependencies
├── Dockerfile # Container definition
├── .dockerignore # Ignore unnecessary files in image
├── data/
│ └── customers_clean.csv
├── model/
│ └── churn_model.pkl
├── processed/
│ └── scaler.pkl


---

## 🚀 How It Works

1. **Preprocessing**:
   - Handles missing values
   - Encodes categorical variables
   - Scales numerical features

2. **Model Training**:
   - Trains both Random Forest & Logistic Regression
   - Evaluates and saves the best model (`churn_model.pkl`)

3. **Serving**:
   - A Flask API loads the model and scaler
   - Accepts JSON input and returns churn prediction

---

## 🐳 Dockerized Workflow

Build and run the entire pipeline and API inside Docker:

### 🔨 Build the image

docker build -t churn-api .

### ▶️ Run the container

docker run -p 5000:5000 churn-api

## 📮 Sample API Usage

Endpoint:

POST http://localhost:5000/predict

Request Body:

{
  "features": [34, 1, 5, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 2, 70.35, 1397.5, 0]
}

Response:

{
  "churn": 1
}

## 📦 Setup (For Local Development)

Clone the repo
Create virtual environment (optional)
Install dependencies

pip install -r requirements.txt

Run:

python preprocess.py
python train.py
python app.py

## 🧪 Dependencies

Python 3.11
pandas
scikit-learn
Flask
joblib
numpy
mlflow (optional)
