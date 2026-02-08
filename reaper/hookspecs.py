"""
REAPER Plugin Hook Specifications

Pluggy hook specifications for the 5-sense pipeline.
Each sense = one job, implemented as a plugin.
"""
from typing import List

import pluggy

from reaper.models import ActionResult, ScoredSignal, Signal

hookspec = pluggy.HookspecMarker("reaper")


class HookSpecs:
    """Hook specifications container."""
    pass


    @hookspec
    def reaper_sight_detect(source: str) -> List[Signal]:
        """
        Sight sense: Visual detection of signals.

        Args:
            source: Plugin-specific source identifier (never hard-coded in core)

        Returns:
            List of detected signals with sense_type=SIGHT
        """
        pass

    @hookspec
    def reaper_hearing_detect(source: str) -> List[Signal]:
        """
        Hearing sense: Audio/textual detection of signals.

        Args:
            source: Plugin-specific source identifier (never hard-coded in core)

        Returns:
            List of detected signals with sense_type=HEARING
        """
        pass

    @hookspec
    def reaper_touch_detect(source: str) -> List[Signal]:
        """
        Touch sense: Physical/interaction detection of signals.

        Args:
            source: Plugin-specific source identifier (never hard-coded in core)

        Returns:
            List of detected signals with sense_type=TOUCH
        """
        pass

    @hookspec
    def reaper_taste_detect(source: str) -> List[Signal]:
        """
        Taste sense: Quality/sampling detection of signals.

        Args:
            source: Plugin-specific source identifier (never hard-coded in core)

        Returns:
            List of detected signals with sense_type=TASTE
        """
        pass

    @hookspec
    def reaper_smell_detect(source: str) -> List[Signal]:
        """
        Smell sense: Pattern/anomaly detection of signals.

        Args:
            source: Plugin-specific source identifier (never hard-coded in core)

        Returns:
            List of detected signals with sense_type=SMELL
        """
        pass

    @hookspec
    def reaper_score_signal(signal: Signal) -> ScoredSignal:
        """
        Score a detected signal.

        Args:
            signal: Raw signal to score

        Returns:
            Scored signal with analysis
        """
        pass

    @hookspec
    def reaper_action_execute(scored_signal: ScoredSignal) -> ActionResult:
        """
        Action sense: Execute action based on scored signal.

        Args:
            scored_signal: Signal with score to act upon

        Returns:
            Result of the action taken
        """
        pass
