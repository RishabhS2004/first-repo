from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json

app = Flask(__name__)

# Kafka config
KAFKA_TOPIC = "iris_topic"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

producer = Producer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
})


def validate_input(data):
    errors = {}
    cleaned_data = {}

    # Mandatory fields for regressor
    for field in ['sepal_length', 'sepal_width', 'petal_length']:
        value = data.get(field)
        if value is None:
            errors[field] = "Missing"
        else:
            try:
                float_value = float(value)
                if 0 <= float_value <= 50:
                    cleaned_data[field] = float_value
                else:
                    errors[field] = "Out of range (0-50)"
            except ValueError:
                errors[field] = "Not a valid float"

    # Optional field for classifier
    if 'petal_width' in data:
        try:
            pw = float(data['petal_width'])
            if 0 <= pw <= 50:
                cleaned_data['petal_width'] = pw
            else:
                errors['petal_width'] = "Out of range (0-50)"
        except ValueError:
            errors['petal_width'] = "Not a valid float"

    return errors, cleaned_data


@app.route('/iris', methods=['POST'])
def receive_iris():
    if not request.is_json:
        return jsonify({'error': 'Request must be in JSON format'}), 400

    data = request.get_json()
    errors, cleaned_data = validate_input(data)

    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400

    try:
        producer.produce(KAFKA_TOPIC, key="iris", value=json.dumps(cleaned_data))
        producer.flush()
    except Exception as e:
        return jsonify({'error': 'Failed to publish to Kafka topic', 'details': str(e)}), 500

    return jsonify({'message': 'Successfully published to Kafka topic', 'data': cleaned_data}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
