import os
from typing import Optional

from .inference.central_agent import CentralAgent
from .adapters.template_adapter import TemplateAdapter

ROLE_ENV = "LIFE_MONITOR_ROLE"

ROLE_HELP = (
    "Roles: camera, audio, wearable, pc, hub. "
    "Set via env LIFE_MONITOR_ROLE or pass to main(role)."
)


def main(role: Optional[str] = None) -> None:
    role = role or os.getenv(ROLE_ENV, "camera")
    print(f"Node starting with role: {role}")
    print(ROLE_HELP)
    if role == "hub":
        CentralAgent().run_mqtt()
    else:
        # Demo: publish template observation; replace with real adapter
        src = os.getenv("SOURCE_ID", role)
        TemplateAdapter(src).run_once()

if __name__ == "__main__":
    main()
