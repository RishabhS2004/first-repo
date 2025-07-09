from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model/churn_model.pkl")
scaler = joblib.load("processed/scaler.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        print("Request received.")
        data = request.get_json(force=True)
        print("Data received:", data)

        features = np.array(data["features"]).reshape(1, -1)
        scaled = scaler.transform(features)
        prediction = model.predict(scaled)

        return jsonify({"churn": int(prediction[0])})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
