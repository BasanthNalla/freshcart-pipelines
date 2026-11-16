
import pika
import json
import random
import time
from datetime import datetime, timezone

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

cities = ["bangalore", "chennai"]

zones = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "velachery", "adyar"]
}

request_types = ["ride", "food"]
request_id = 1

print("Dispatcher started with invalid messages enabled...", flush=True)

try:
    while True:
        city = random.choice(cities)
        zone = random.choice(zones[city])
        request_type = random.choice(request_types)

        routing_key = f"{city}.{zone}.{request_type}"

        message = {
            "id": request_id,
            "city": city,
            "type": request_type,
            "ts": datetime.now(timezone.utc).isoformat()
        }

        # Every 10th message is invalid (missing zone)
        if request_id % 10 != 0:
            message["zone"] = zone
            print(f"VALID message: {request_id}", flush=True)
        else:
            print(f"INVALID message: {request_id} (zone missing)", flush=True)

        channel.basic_publish(
            exchange="rapido-dispatch",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json"
            )
        )

        print(f"Published: {routing_key} | {message}", flush=True)

        request_id += 1
        time.sleep(2)

except KeyboardInterrupt:
    print("Dispatcher stopped.")

finally:
    connection.close()
