import paho.mqtt.client as mqtt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class MQTTClient:
    def __init__(self, broker_url, broker_port, topic):
        self.client = mqtt.Client()
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        if len(message):
            async_to_sync(get_channel_layer().group_send)(
                "live_location_group",
                {
                    "type": "location.update",
                    "message": message,
                },
            )

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()
