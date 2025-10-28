# Life Monitor

Camera-powered desktop assistant that detects your activity (reading, coding, guitar) and auto-prepares resources.

## Quick start
- Install Python 3.10+ and required packages (no internet install here): `pip install -r requirements.txt`
- Run: `python main.py`
- Controls (MVP): press `r` (reading), `c` (coding), `g` (guitar) to simulate detection; `q` to quit.

## Architecture (MVP)
- Detector (src/life_monitor/detector.py): webcam loop + placeholder key-driven state switch; swap with real model later.
- Actions (src/life_monitor/actions.py): opens URLs/apps based on config.yaml when state changes.
- Config (config.yaml): declarative mapping from state -> urls/commands.

## Implementation plan
1) Detection MVP
   - [x] Webcam loop + keyboard-based state switch
   - [ ] Replace with model-based classifier (MediaPipe/Transformers or custom) and debounce/cooldowns
2) Action orchestration
   - [x] Trigger URLs/commands on state change
   - [ ] Add per-state cooldowns and idempotency guards
3) Context enrichment
   - [ ] Reading: enrich with book info (ISBN search/notes)
   - [ ] Coding: open project/IDE workspace
   - [ ] Guitar: open tabs/backing tracks/metronome
4) Reliability & UX
   - [ ] System tray/minimize, start/stop hotkeys, logs
   - [ ] Configurable profiles per time-of-day
5) Packaging
   - [ ] Configurable installer; Windows startup option
6) Privacy & Security
   - [ ] Local-only processing; clear data retention policy

## State -> Action mapping (edit config.yaml)
```yaml
states:
  guitar:
    urls:
      - https://www.ultimate-guitar.com/
  reading:
    urls:
      - https://scholar.google.com/
      - https://wikipedia.org/
  coding:
    commands:
      - code .
```

## Task log
- [x] Bootstrap repo structure
- [x] Add config + action runner + detector skeleton
- [x] Local git init and first commit
- [ ] Push to GitHub (needs your remote URL)

## Multi-Pi scaffold (Detection → Inference → Analysis)
- Roles (per Pi): camera (OpenCV image), audio (mic speech/guitar), wearable (watch/health), pc (desktop context), hub (central agent + web).
- How to run: set env PYTHONPATH=src and LIFE_MONITOR_ROLE, then run `python -m life_monitor.node`; messaging uses MQTT on observations/{source_id} (set MQTT_HOST/MQTT_PORT as needed).
- Code map: detection in `src\\life_monitor\\detectors\\`, inference in `src\\life_monitor\\inference\\central_agent.py`, bus in `src\\life_monitor\\bus\\mqtt_bus.py`, web in `src\\life_monitor\\web\\server.py`.
- Next steps: implement MQTT pub/sub, flesh out detectors, connect hub to ActionRunner for recommendations, build FastAPI UI to summarize daily activity.

## Unified Perception Interface
- Data flow: [Sensor Adapter] -> [Serializer (Proto/JSON)] -> MQTT topic observations\{source_id} -> [Central Agent].
- Add sensor (<50 LOC):
  1) Add message NewType in src\life_monitor\proto\observation.proto
  2) protoc --python_out=. src\life_monitor\proto\observation.proto
  3) Write NewAdapter -> publish to observations\{source_id}
  4) Add case in CentralAgent.handlers dict
