This project demonstrates a basic event-driven architecture using Apache Kafka, where:

- Two independent Python producers send messages to a Kafka topic.
- A single Python subscriber (consumer) listens to the topic and displays messages from both producers.

---

## Project Structure

KafkaDemoFolder/
	── producer1.py         # Sends messages to Kafka as 'Producer1'
	── producer2.py         # Sends messages to Kafka as 'Producer2'
	── subscriber.py        # Consumes messages from the topic and prints them
	── README.md            # Project description

---

## Components and Flow

1. Kafka Topic: All programs use a common topic, e.g., `test2`.
2. Producer 1: Sends a message like "Message from producer 1" with user ID "Producer1".
3. Producer 2: Sends a similar message with user ID "Producer2".
4. Subscriber:
   - Subscribes to the topic.
   - Polls and prints all messages, showing messages from both producers in real time.