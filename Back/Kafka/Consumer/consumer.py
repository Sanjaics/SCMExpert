from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import json
import os
from dotenv import load_dotenv


load_dotenv()

bootstrap_servers=os.getenv("bootstrap_servers")

mongouri=os.getenv("MONGO_DB_URL")
conn = MongoClient(mongouri)
database = conn[os.getenv("database")]
collection2 = database[os.getenv("collection2")]

topicname=os.getenv("topicname")

consumer = KafkaConsumer(
    topicname,
     bootstrap_servers=[bootstrap_servers],
     group_id='my-group',
     api_version=(0, 11, 5),
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    try:
        data = json.loads(message.value)
        collection2.insert_one(data)
        print(f"{data} added to {collection2}")
    except Exception as e:
        print(f"Error: {e}")