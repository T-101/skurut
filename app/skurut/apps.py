from django.apps import AppConfig

from skurut.clients import MQTTClient


class SkurutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skurut'

    def ready(self):
        broker_url = "mqtt.hsl.fi"
        broker_port = 1883
        topic = "/hfp/v2/journey/ongoing/vp/tram/+/+/+/+/+/+/+/4/#"
        # topic = "/hfp/v2/journey/ongoing/vp/tram/+/+/+/+/+/+/+/2/#"  # slower, good for developing

        mqtt_client = MQTTClient(broker_url, broker_port, topic)
        mqtt_client.connect()
