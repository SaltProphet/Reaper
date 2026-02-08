"""
Sight Sense Pipeline Stub

Visual detection of signals.
Each sense = one job. Never mix pipeline roles.
"""

from typing import List

import pluggy

from reaper.models import SenseType, Signal

hookimpl = pluggy.HookimplMarker("reaper")


class SightPlugin:
    """
    Stub plugin for Sight sense (visual detection).

    This is a reference implementation. Real plugins should:
    - Never hard-code sources in core
    - Accept source as parameter
    - Return properly validated Signal objects
    """

    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        """
        Detect visual signals.

        Args:
            source: Plugin-specific source identifier (e.g., "camera-1", "screen-capture")

        Returns:
            List of detected signals with sense_type=SIGHT
        """
        # Stub implementation - real plugin would detect visual signals
        return [
            Signal(
                sense_type=SenseType.SIGHT,
                source=source,
                raw_data={
                    "description": "Stub visual signal detected",
                    "stub": True,
                },
                metadata={"plugin": "SightPlugin"},
            )
        ]
