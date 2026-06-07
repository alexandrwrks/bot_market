import asyncio

import aio_pika


async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

    async with connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=b"Hello World!",
            ),
            routing_key="notification",
        )

        print("Message sent")


if __name__ == "__main__":
    asyncio.run(main())
