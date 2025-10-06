import joblib
import numpy as np
import sqlite3
from datetime import datetime

model = joblib.load('irismodel.pkl')

from sklearn.datasets import load_iris
iris = load_iris()

    print("\nEnter flower measurements:")
    sepal_length = float(input("Sepal length (cm): "))
    petal_length = float(input("Petal length (cm): "))
    sepal_width = float(input("Sepal width (cm): "))
    petal_width = float(input("Petal width (cm): "))

    input_data = np.array([[sepal_length, petal_length, sepal_width, petal_width]])

    prediction = model.predict(input_data)
    print(f"\n Predicted Iris Species: {prediction[0]}")

    conn = sqlite3.connect('iris_predictions.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sepal_length REAL,
        sepal_width REAL,
        petal_length REAL,
        petal_width REAL,
        prediction TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO predictions (sepal_length, sepal_width, petal_length, petal_width, prediction, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        sepal_length,
        sepal_width,
        petal_length,
        petal_width,
        prediction,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()
    print("Prediction saved to SQLite database.")
