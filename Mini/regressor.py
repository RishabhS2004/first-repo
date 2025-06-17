from kafka import KafkaConsumer
import json
import joblib
import os
import grpc
import clsreg_pb2
import clsreg_pb2_grpc

# Load regression model
model_path = os.path.join("regression_model.pkl")
model = joblib.load(model_path)

# === Setup gRPC client for RegressService ===
channel = grpc.insecure_channel('localhost:50051')
stub = clsreg_pb2_grpc.RegressServiceStub(channel)


# Kafka consumer setup
consumer = KafkaConsumer(
    'iris_topic',  # topic name
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Waiting...")

# Process messages
for message in consumer:
    data = message.value
    print(f"Received: {data}")

    features = [[
        data['sepal_length'],
        data['sepal_width'],
        data['petal_length']
    ]]

    # Predict the missing feature (petal width)
    predicted_petal_width = model.predict(features)[0]

    print(f"Predicted petal width: {predicted_petal_width:.2f}")

    # === Send to gRPC StoreService ===
    grpc_request = clsreg_pb2.RegressRequest(
    sepal_length=data['sepal_length'],
    sepal_width=data['sepal_width'],
    petal_length=data['petal_length'],
    predicted_petal_width=predicted_petal_width
    )

    grpc_response = stub.PredictPetalWidth(grpc_request)
    print(f"✅ gRPC StoreService Response: {grpc_response.predicted_petal_width:.2f}")