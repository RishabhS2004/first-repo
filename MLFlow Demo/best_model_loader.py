from mlflow.sklearn import load_model

model = load_model("best_model")
result = model.predict([[5.1, 3.5, 1.4, 0.2]])
print("Prediction:", result)
