from random import choice
from confluent_kafka import Producer

if __name__ == "__main__":
    config = {
        'bootstrap.servers': 'localhost:9092',
        'acks': 'all'
    }

    topic = "testing"

    producer = Producer(config)
    user_id = "Producer2"
    product = "Message from Producer2"

    producer.produce(topic, product, user_id)
    producer.poll(0)
    producer.flush()