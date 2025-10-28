# Life-Monitor Dev Tasks (Quick Pickup)

Timestamp: 2025-10-28T07:08:09.601Z

Vision: Unified Perception Interface — All sensors → normalized Observation (Proto/JSON) → MQTT observations/{source_id} → Central Agent → actions/UI.

What’s Done
- Repo scaffolded for multi-Pi: detectors/, inference/, bus/, web/, adapters/, serialization/, proto/.
- MQTT bus (paho-mqtt) and CentralAgent subscribing to observations/# with handler dispatch by kind.
- Serializer with Protobuf-first and JSON fallback, topic helper (topic_for).
- Adapter template publishing Observation in <50 LOC; node role runner (hub vs sensor) wired.
- README updated with data flow, extension checklist; requirements include protobuf and paho-mqtt.

Next Up (Priority)
- Generate proto: protoc --python_out=. src\life-monitor\proto\observation.proto (commit observation_pb2.py).
- Implement adapters: PiCameraAdapter (image), MicAdapter (speech/guitar), WearableAdapter (health), PCFocusAdapter (desktop context); use run_loop.
- CentralAgent: connect to ActionRunner for recommendations; add persistence (SQLite) for daily summaries, and FastAPI web UI.
- Robust MQTT: auth/TLS, reconnect/backoff; structured logging and metrics; config via env/config.yaml.

Quick Run
- Hub: $env:PYTHONPATH="src"; $env:LIFE_MONITOR_ROLE="hub"; python -m life_monitor.node
- Sensor demo: $env:PYTHONPATH="src"; $env:LIFE_MONITOR_ROLE="camera"; $env:SOURCE_ID="pi-cam-1"; python -m life_monitor.node

Extension Checklist (Add New Sensor)
1) Add message NewType in src\life_monitor\proto\observation.proto
2) protoc --python_out=. src\life_monitor\proto\observation.proto
3) Write NewAdapter → publish to observations/{source_id}
4) Add case in CentralAgent.handlers dict

Repo Map (mini)
- src\life_monitor\proto\observation.proto — schema
- src\life_monitor\serialization\serializer.py — (de)serialization
- src\life_monitor\bus\mqtt_bus.py — transport
- src\life_monitor\inference\central_agent.py — reasoning
- src\life_monitor\adapters\template_adapter.py — sensor template
