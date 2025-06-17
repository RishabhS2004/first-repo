from confluent_kafka import Consumer, KafkaException
import json

# Kafka config
KAFKA_TOPIC = 'iris_data'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_GROUP_ID = 'iris_consumer_group'

# Create Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': 'earliest'  # start from the beginning
})

# Subscribe to topic
consumer.subscribe([KAFKA_TOPIC])

print(f"Waiting...\n")

try:
    while True:
        msg = consumer.poll(1.0)  # timeout = 1 second

        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        # Parse and display message
        try:
            value = msg.value().decode('utf-8')
            data = json.loads(value)
            print("📦 Received Data from Kafka:")
            print(json.dumps(data, indent=4), "\n")
        except Exception as e:
            print(f"⚠️ Failed to process message: {e}")

except KeyboardInterrupt:
    print("\n🛑 Stopping consumer...")

finally:
    consumer.close()
