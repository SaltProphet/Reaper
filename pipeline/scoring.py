"""
Scoring Pipeline Stub

Score detected signals for prioritization.
Separate from detection - never mix pipeline roles.
"""

import pluggy

from reaper.models import ScoredSignal, Signal

hookimpl = pluggy.HookimplMarker("reaper")


class ScoringPlugin:
    """
    Stub plugin for scoring signals.

    This is a reference implementation. Real plugins should:
    - Never hard-code scoring logic in core
    - Implement domain-specific scoring algorithms
    - Return properly validated ScoredSignal objects
    """

    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        """
        Score a detected signal.

        Args:
            signal: Raw signal to score

        Returns:
            Scored signal with analysis
        """
        # Stub implementation - real plugin would apply sophisticated scoring
        return ScoredSignal(
            signal=signal,
            score=0.5,  # Neutral score for stub
            analysis={
                "description": "Stub scoring applied",
                "stub": True,
            },
            tags=["stub"],
        )
