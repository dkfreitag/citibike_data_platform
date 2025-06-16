from kafka import KafkaConsumer

import os

def main():
    consumer = KafkaConsumer('station-status', bootstrap_servers=f'{os.environ['BROKER_PRIVATE_IP_ADDRESS']}:9092')

    for message in consumer:
        print(message.value)

if __name__ == '__main__':
    main()
