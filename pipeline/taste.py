"""
Taste Sense Pipeline Stub

Quality/sampling detection of signals.
Each sense = one job. Never mix pipeline roles.
"""
from typing import List

import pluggy

from reaper.models import SenseType, Signal

hookimpl = pluggy.HookimplMarker("reaper")


class TastePlugin:
    """
    Stub plugin for Taste sense (quality/sampling detection).

    This is a reference implementation. Real plugins should:
    - Never hard-code sources in core
    - Accept source as parameter
    - Return properly validated Signal objects
    """

    @hookimpl
    def reaper_taste_detect(self, source: str) -> List[Signal]:
        """
        Detect quality/sampling signals.

        Args:
            source: Plugin-specific source identifier (e.g., "quality-metric", "sampler")

        Returns:
            List of detected signals with sense_type=TASTE
        """
        # Stub implementation - real plugin would detect quality/sampling signals
        return [
            Signal(
                sense_type=SenseType.TASTE,
                source=source,
                raw_data={
                    "description": "Stub quality/sampling signal detected",
                    "stub": True,
                },
                metadata={"plugin": "TastePlugin"},
            )
        ]
