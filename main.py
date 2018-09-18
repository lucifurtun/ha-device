import asyncio
import logging

from gpiozero import LED
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_2

logger = logging.getLogger(__name__)
client = None


async def check():
    while True:
        await asyncio.sleep(1)
        print("Checking...")


async def init():
    global client
    client = MQTTClient()
    await client.connect('mqtt://127.0.0.1')
    await client.subscribe([('devices/power', QOS_2)])

    while True:
        try:
            message = await client.deliver_message()
            packet = message.publish_packet
            print("%s => %s" % (packet.variable_header.topic_name, str(packet.payload.data)))
        except ClientException as ce:
            logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    #
    # loop.create_task(init())
    # loop.run_until_complete(check())
    led = LED(17)
    led.on()

    print("test")
