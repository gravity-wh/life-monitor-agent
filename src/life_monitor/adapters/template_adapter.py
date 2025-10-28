import time
from life_monitor.serialization import Serializer, topic_for
from life_monitor.bus.mqtt_bus import MqttBus

class TemplateAdapter:
    def __init__(self, source_id: str) -> None:
        self.source_id = source_id; self.ser = Serializer(); self.bus = MqttBus()
    def run_once(self) -> None:
        payload = {'activity': 'reading', 'confidence': 0.9}
        obs = self.ser.build(self.source_id, kind='image', payload=payload)
        data, ct = self.ser.dumps(obs); self.bus.connect(); self.bus.publish(topic_for(self.source_id), data, content_type=ct)
    def run_loop(self, interval_s: float = 5.0) -> None:
        self.bus.connect()
        while True:
            payload = {'activity': 'reading', 'confidence': 0.9}
            obs = self.ser.build(self.source_id, kind='image', payload=payload)
            data, ct = self.ser.dumps(obs); self.bus.publish(topic_for(self.source_id), data, content_type=ct)
            time.sleep(interval_s)
