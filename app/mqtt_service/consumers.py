from channels.generic.websocket import AsyncWebsocketConsumer
import json


class LocationConsumer(AsyncWebsocketConsumer):
    DATA_KEYS = {'lat', 'long', 'hdg', 'desi', 'veh'}  # Coordinates, heading, designation, vehicle number

    async def connect(self):
        await self.channel_layer.group_add(
            "live_location_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "live_location_group",
            self.channel_name
        )

    async def location_update(self, event):
        message = event['message']
        try:
            payload = json.loads(message).get("VP")  # VehiclePosition
        except json.JSONDecodeError:
            return

        if not payload:
            return

        d = {k: v for k, v in payload.items() if k in self.DATA_KEYS}
        await self.send(text_data=json.dumps({"location": d}))
