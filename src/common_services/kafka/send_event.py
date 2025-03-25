from confluent_kafka import Producer

conf = {"bootstrap.servers": "kafka:9092"}

producer = Producer(conf)


def send_event(event: str, key: str, value: str):
    producer.produce(event, key=key, value=value)
    producer.flush()
