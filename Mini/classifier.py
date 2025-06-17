from kafka import KafkaConsumer
import json
import joblib
import grpc
import clsreg_pb2
import clsreg_pb2_grpc
import os
from sklearn.datasets import load_iris
from sklearn.preprocessing import LabelEncoder

# Load the model
model_path = os.path.join("classification_model.pkl")
model = joblib.load(model_path)

# Recreate encoder inline (not saved or loaded from file)
iris = load_iris()
encoder = LabelEncoder()
encoder.fit(iris.target_names)  # ['setosa', 'versicolor', 'virginica']

# === Setup gRPC client for ClassifyService ===
channel = grpc.insecure_channel('localhost:50051')
stub = clsreg_pb2_grpc.ClassifyServiceStub(channel)

# Setup Kafka consumer
consumer = KafkaConsumer(
    'iris_data',  # topic name
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Waiting...")

# Loop to process incoming messages
for message in consumer:
    data = message.value
    print(f"Received: {data}")

    # Extract and order features correctly
    features = [[
        data['sepal_length'],
        data['sepal_width'],
        data['petal_length'],
        data['petal_width']
    ]]

    # Predict the class index
    prediction_index = model.predict(features)[0]

    # Decode the class name
    prediction_name = encoder.inverse_transform([prediction_index])[0]

    print(f"Predicted class: {prediction_name}")

    # === Send to gRPC StoreService ===
    grpc_request = clsreg_pb2.ClassifyRequest(
        sepal_length=data['sepal_length'],
        sepal_width=data['sepal_width'],
        petal_length=data['petal_length'],
        petal_width=data['petal_width'],
        predicted_class=prediction_name
    )

    grpc_response = stub.PredictClass(grpc_request)
    print(f"✅ gRPC StoreService Response: {grpc_response.predicted_class}")