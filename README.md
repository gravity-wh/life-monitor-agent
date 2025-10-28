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
