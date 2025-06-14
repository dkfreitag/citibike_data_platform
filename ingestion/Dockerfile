FROM python:3.12
WORKDIR /

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 9092

CMD ["python3", "ec2_producer.py"]
