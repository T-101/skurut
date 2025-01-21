import json
import paho.mqtt.client as mqtt
import redis

from django.conf import settings

REDIS_URL = settings.CACHES.get("default").get("LOCATION")

redis_client = redis.StrictRedis.from_url(REDIS_URL + "?decode_responses=True")
REDIS_CHANNEL = "mqtt_messages"


class MQTTClient:
    DATA_KEYS = {'lat', 'long', 'hdg', 'desi', 'veh'}

    def __init__(self, broker_url, broker_port, topic):
        self.client = mqtt.Client()
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        print("MQTT connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode("utf-8")).get("VP")
        d = {k: v for k, v in payload.items() if k in self.DATA_KEYS}
        redis_client.publish(REDIS_CHANNEL, json.dumps(d))

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()
