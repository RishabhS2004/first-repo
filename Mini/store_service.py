import grpc
from concurrent import futures
import sqlite3
import clsreg_pb2
import clsreg_pb2_grpc
import joblib
import os

# Load models
classification_model = joblib.load("classification_model.pkl")
regression_model = joblib.load("regression_model.pkl")

# === Setup SQLite database ===
conn = sqlite3.connect("iris_data.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Classification (
        sepal_length REAL,
        sepal_width REAL,
        petal_length REAL,
        petal_width REAL,
        predicted_class TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Regression (
        sepal_length REAL,
        sepal_width REAL,
        petal_length REAL,
        predicted_petal_width REAL
    )
""")
conn.commit()

# === ClassifyService Implementation ===
class ClassifyServiceServicer(clsreg_pb2_grpc.ClassifyServiceServicer):
    def PredictClass(self, request, context):
        features = [[
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            request.petal_width
        ]]

        prediction_index = classification_model.predict(features)[0]

        # Recreate label names directly from dataset (no saved encoder)
        iris_classes = ['setosa', 'versicolor', 'virginica']
        predicted_class = iris_classes[prediction_index]

        print(f"🟢 Class Prediction: {predicted_class}")

        # Store in Classification table
        cursor.execute("""
            INSERT INTO Classification (sepal_length, sepal_width, petal_length, petal_width, predicted_class)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            request.petal_width,
            predicted_class
        ))
        conn.commit()
        print("📌 Updated Classification Table:")
        for row in cursor.execute("SELECT * FROM Classification"):
            print(row)
        print("-" * 50)

        return clsreg_pb2.ClassifyRequest(
        sepal_length=request.sepal_length,
        sepal_width=request.sepal_width,
        petal_length=request.petal_length,
        petal_width=request.petal_width,
        predicted_class=predicted_class
)

# === RegressService Implementation ===
class RegressServiceServicer(clsreg_pb2_grpc.RegressServiceServicer):
    def PredictPetalWidth(self, request, context):
        predicted_value = request.predicted_petal_width  # Value comes from client (regressor.py)

        print(f"🟢 Regress Prediction: {predicted_value:.2f}")

        # Store in Regression table
        cursor.execute("""
            INSERT INTO Regression (sepal_length, sepal_width, petal_length, predicted_petal_width)
            VALUES (?, ?, ?, ?)
        """, (
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            predicted_value
        ))
        conn.commit()

        print("📌 Updated Regression Table:")
        for row in cursor.execute("SELECT * FROM Regression"):
            print(row)
        print("-" * 50)

        # ✅ Return all fields back (echo response)
        return clsreg_pb2.RegressRequest(
            sepal_length=request.sepal_length,
            sepal_width=request.sepal_width,
            petal_length=request.petal_length,
            predicted_petal_width=predicted_value
        )



# === Run gRPC server ===
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clsreg_pb2_grpc.add_ClassifyServiceServicer_to_server(ClassifyServiceServicer(), server)
    clsreg_pb2_grpc.add_RegressServiceServicer_to_server(RegressServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 gRPC Store Service is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()