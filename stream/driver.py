import pika
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name", help="Driver name")
parser.add_argument("pattern", help="RabbitMQ binding pattern")
args = parser.parse_args()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

result = channel.queue_declare(
    queue="",
    exclusive=True,
    auto_delete=True
)

queue_name = result.method.queue

channel.queue_bind(
    exchange="rapido-dispatch",
    queue=queue_name,
    routing_key=args.pattern
)

print(f"Driver: {args.name}", flush=True)
print(f"Listening for pattern: {args.pattern}", flush=True)


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)

        # Reject messages that do not contain the zone field
        if "zone" not in message:
            print(
                f"[{args.name}] REJECTED: Missing zone | {message}",
                flush=True
            )

            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )
            return

        # Process valid messages
        print(
            f"[{args.name}] PROCESSED: {method.routing_key} | {message}",
            flush=True
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        print(f"[{args.name}] REJECTED: Invalid JSON", flush=True)
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False
)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\nDriver {args.name} stopped.")
finally:
    connection.close()