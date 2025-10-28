import os
from typing import Callable

try:
    import paho.mqtt.client as mqtt  # type: ignore
except Exception:  # simple stub when lib missing
    mqtt = None

class MqttBus:
    def __init__(self, host: str | None = None, port: int | None = None, client_id: str | None = None) -> None:
        self.host = host or os.getenv("MQTT_HOST", "localhost")
        self.port = int(port or os.getenv("MQTT_PORT", 1883))
        self.client_id = client_id or os.getenv("MQTT_CLIENT_ID", "life-monitor")
        self.client = None if mqtt is None else mqtt.Client(client_id=self.client_id)

    def connect(self) -> None:
        if self.client is None:
            print("paho-mqtt not installed; MQTT disabled.")
            return
        self.client.connect(self.host, self.port, keepalive=30)
        self.client.loop_start()

    def publish(self, topic: str, payload: bytes, content_type: str | None = None) -> None:
        if self.client is None:
            print(f"MQTT disabled; would publish to {topic} ({len(payload)} bytes)")
            return
        props = None
        try:
            # Only for MQTT v5; ignore if unsupported
            props = getattr(mqtt, "Properties", lambda x: None)(getattr(mqtt, "PacketTypes", object()).PUBLISH)  # type: ignore
            if props is not None and content_type:
                props.ContentType = content_type  # type: ignore
        except Exception:
            props = None
        self.client.publish(topic, payload, qos=0, retain=False, properties=props)

    def subscribe(self, topic: str, handler: Callable[[bytes, str | None], None]) -> None:
        if self.client is None:
            print(f"MQTT disabled; subscription to {topic} not active.")
            return
        def _on_msg(_cli, _ud, msg):
            ct = None
            try:
                ct = getattr(msg, "properties", None).ContentType  # type: ignore
            except Exception:
                ct = None
            handler(msg.payload, ct)
        self.client.subscribe(topic, qos=0)
        self.client.on_message = _on_msg
