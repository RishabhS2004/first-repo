import sqlite3
import time
import pandas as pd

def display_predictions():
    conn = sqlite3.connect("iris_predictions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    rows = cursor.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Prediction", "Timestamp"])
        print(df)
    else:
        print("No predictions yet.")

    conn.close()

print("📡 ServiceB: Monitoring predictions every 30 seconds...\n")
while True:
    display_predictions()
    time.sleep(30)