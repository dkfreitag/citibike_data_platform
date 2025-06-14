from kafka import KafkaConsumer

consumer = KafkaConsumer('station-status', bootstrap_servers='localhost:9092')

for message in consumer:
    print(message.value)