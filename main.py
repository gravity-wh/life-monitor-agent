import time
import sys, os
import yaml
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from life_monitor.detector import Detector
from life_monitor.actions import ActionRunner


def load_config(path: str = 'config.yaml'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def main() -> None:
    cfg = load_config()
    runner = ActionRunner(cfg)
    det = Detector()
    last_state = None
    print("Life Monitor started. Press r/c/g to simulate reading/coding/guitar; q to quit.")

    try:
        while True:
            frame = det.get_frame()
            state, key = det.get_state(frame)
            if state != last_state:
                if state:
                    print(f"Detected state: {state}")
                    runner.trigger_for(state)
                last_state = state
            if Detector.should_quit(key):
                break
            time.sleep(0.01)
    finally:
        det.release()


if __name__ == '__main__':
    main()
