"""
Hearing Sense Pipeline Stub

Audio/textual detection of signals.
Each sense = one job. Never mix pipeline roles.
"""

from typing import List

import pluggy

from reaper.models import SenseType, Signal

hookimpl = pluggy.HookimplMarker("reaper")


class HearingPlugin:
    """
    Stub plugin for Hearing sense (audio/textual detection).

    This is a reference implementation. Real plugins should:
    - Never hard-code sources in core
    - Accept source as parameter
    - Return properly validated Signal objects
    """

    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        """
        Detect audio/textual signals.

        Args:
            source: Plugin-specific source identifier (e.g., "microphone-1", "log-stream")

        Returns:
            List of detected signals with sense_type=HEARING
        """
        # Stub implementation - real plugin would detect audio/textual signals
        return [
            Signal(
                sense_type=SenseType.HEARING,
                source=source,
                raw_data={
                    "description": "Stub audio/textual signal detected",
                    "stub": True,
                },
                metadata={"plugin": "HearingPlugin"},
            )
        ]
