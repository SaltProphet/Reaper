"""
Smell Sense Pipeline Stub

Pattern/anomaly detection of signals.
Each sense = one job. Never mix pipeline roles.
"""

from typing import List

import pluggy

from reaper.models import SenseType, Signal

hookimpl = pluggy.HookimplMarker("reaper")


class SmellPlugin:
    """
    Stub plugin for Smell sense (pattern/anomaly detection).

    This is a reference implementation. Real plugins should:
    - Never hard-code sources in core
    - Accept source as parameter
    - Return properly validated Signal objects
    """

    @hookimpl
    def reaper_smell_detect(self, source: str) -> List[Signal]:
        """
        Detect pattern/anomaly signals.

        Args:
            source: Plugin-specific source identifier (e.g., "pattern-analyzer", "anomaly-detector")

        Returns:
            List of detected signals with sense_type=SMELL
        """
        # Stub implementation - real plugin would detect pattern/anomaly signals
        return [
            Signal(
                sense_type=SenseType.SMELL,
                source=source,
                raw_data={
                    "description": "Stub pattern/anomaly signal detected",
                    "stub": True,
                },
                metadata={"plugin": "SmellPlugin"},
            )
        ]
