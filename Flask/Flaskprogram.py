from flask import Flask, request, jsonify
import sqlite3
import joblib
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
model = joblib.load('irismodel.pkl')

def init_db():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        sepal_length REAL,
        sepal_width REAL,
        petal_length REAL,
        petal_width REAL,
        predicted_class REAL,
        timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        user_id = data['user_id']
        sepal_length = float(data['sepal_length'])
        sepal_width = float(data['sepal_width'])
        petal_length = float(data['petal_length'])
        petal_width = float(data['petal_width'])
    except (KeyError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400
    input_data = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                              columns=["sepal.length", "sepal.width", "petal.length", "petal.width"])
    predicted_class_num = model.predict(input_data)[0]
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO predictions (
        user_id, sepal_length, sepal_width, petal_length, petal_width, predicted_class, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, sepal_length, sepal_width, petal_length, petal_width,
        predicted_class_num, datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return jsonify({'predicted_class': predicted_class_num})

if __name__ == '__main__':
    app.run(debug=True)