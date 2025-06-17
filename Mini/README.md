# Mini_Project

This project demonstrates real-time Iris flower classification and regression using:

- Flask (REST API)
- Kafka (data pipeline)
- gRPC (microservices)
- SQLite (storage)
- scikit-learn (training models)

# Components

- `iris_producer.py`: Accepts POST data and pushes to Kafka.
- `iris_consumer.py`: Consumes data and routes it to appropriate service.
- `classifier.py`: Classifies flower species.
- `regressor.py`: Predicts petal width.
- `store_service.py`: gRPC server for handling storage and predictions.
- `model_trainer.py`: Used to train and generate `pkl` models.
- `clsreg.proto`: gRPC message and service definitions.
- `clsreg_pb2.py`, `clsreg_pb2_grpc.py`: Auto-generated protobuf files.
- `iris_data`: SQLite database file.

Run Flask, Kafka, gRPC services, and test via pushing values through Postman.