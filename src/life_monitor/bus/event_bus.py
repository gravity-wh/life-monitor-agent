from typing import Callable, Dict, Any, List

class EventBus:
    """Simple in-process pub/sub; swap with MQTT/ZeroMQ for multi-Pi."""
    def __init__(self) -> None:
        self._subs: List[Callable[[Dict[str, Any]], None]] = []

    def publish(self, event: Dict[str, Any]) -> None:
        for h in list(self._subs):
            try:
                h(event)
            except Exception as e:
                print(f"Handler error: {e}")

    def subscribe(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        self._subs.append(handler)
