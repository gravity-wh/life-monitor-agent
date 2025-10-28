import subprocess
import webbrowser
from typing import Dict, Any


class ActionRunner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}

    def trigger_for(self, state: str) -> None:
        states = self.config.get('states') or {}
        spec = states.get(state) or {}
        for url in spec.get('urls') or []:
            try:
                webbrowser.open(url)
            except Exception as e:
                print(f"Failed to open URL {url}: {e}")
        for cmd in spec.get('commands') or []:
            try:
                # shell=True for Windows command resolution (e.g., "code .")
                subprocess.Popen(cmd, shell=True)
            except Exception as e:
                print(f"Failed to run command '{cmd}': {e}")
