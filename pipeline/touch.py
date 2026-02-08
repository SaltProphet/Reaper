"""
Touch Sense Pipeline Stub

Physical/interaction detection of signals.
Each sense = one job. Never mix pipeline roles.
"""
from typing import List

import pluggy

from reaper.models import SenseType, Signal

hookimpl = pluggy.HookimplMarker("reaper")


class TouchPlugin:
    """
    Stub plugin for Touch sense (physical/interaction detection).

    This is a reference implementation. Real plugins should:
    - Never hard-code sources in core
    - Accept source as parameter
    - Return properly validated Signal objects
    """

    @hookimpl
    def reaper_touch_detect(self, source: str) -> List[Signal]:
        """
        Detect physical/interaction signals.

        Args:
            source: Plugin-specific source identifier (e.g., "sensor-1", "api-endpoint")

        Returns:
            List of detected signals with sense_type=TOUCH
        """
        # Stub implementation - real plugin would detect physical/interaction signals
        return [
            Signal(
                sense_type=SenseType.TOUCH,
                source=source,
                raw_data={
                    "description": "Stub physical/interaction signal detected",
                    "stub": True,
                },
                metadata={"plugin": "TouchPlugin"}
            )
        ]
