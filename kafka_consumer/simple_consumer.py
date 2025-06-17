import os

from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

def main():
    consumer = KafkaConsumer('station-status', bootstrap_servers=f'{os.getenv('BROKER_PRIVATE_IP_ADDRESS')}:9092')

    for message in consumer:
        print(message.value)

if __name__ == '__main__':
    main()
