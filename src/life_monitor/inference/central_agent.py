from typing import Dict, Any, Callable
import time
from life_monitor.serialization import Serializer
from life_monitor.bus.mqtt_bus import MqttBus

Handler = Callable[[Dict[str, Any]], None]

class CentralAgent:
    """Central decision-maker: recommend resources, predict next state."""
    def __init__(self) -> None:
        self.serializer = Serializer()
        self.bus = MqttBus()
        self.handlers: dict[str, Handler] = {
            "image": self._handle_image,
            "audio": self._handle_audio,
            "wearable": self._handle_wearable,
            "pc": self._handle_pc,
            "kv": self._handle_kv,
        }

    def run_mqtt(self) -> None:
        self.bus.connect()
        self.bus.subscribe("observations/#", self._on_raw_message)
        print("CentralAgent: subscribed to observations/# (MQTT)")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            print("CentralAgent: shutting down")

    def _on_raw_message(self, payload: bytes, content_type: str | None) -> None:
        event = self.serializer.loads(payload)
        kind = event.get("kind", "unknown")
        handler = self.handlers.get(kind)
        if handler:
            handler(event)
        else:
            print(f"Unhandled event kind={kind} from {event.get('source_id')}")

    # Handlers (extend as needed)
    def _handle_image(self, e: Dict[str, Any]) -> None:
        print(f"[image] {e['source_id']} -> {e['payload']}")

    def _handle_audio(self, e: Dict[str, Any]) -> None:
        print(f"[audio] {e['source_id']} -> {e['payload']}")

    def _handle_wearable(self, e: Dict[str, Any]) -> None:
        print(f"[wearable] {e['source_id']} -> {e['payload']}")

    def _handle_pc(self, e: Dict[str, Any]) -> None:
        print(f"[pc] {e['source_id']} -> {e['payload']}")

    def _handle_kv(self, e: Dict[str, Any]) -> None:
        print(f"[kv] {e['source_id']} -> {e['payload']}")
