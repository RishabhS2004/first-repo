from flask import Flask, request, jsonify
from mlflow.sklearn import load_model
import numpy as np
import random

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "data" not in data:
        return jsonify({"error": "Invalid input. Provide JSON like: {'data': [[...]]}"}), 400

    try:
        # Randomly decide which model to use
        r = random.random()
        alias = "champion" if r > 0.5 else "challenger"
        model = load_model(f"models:/BestIrisModel@{alias}")

        input_data = np.array(data["data"])
        prediction = model.predict(input_data)

        return jsonify({
            "model_used": alias,
            "prediction": prediction.tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)

