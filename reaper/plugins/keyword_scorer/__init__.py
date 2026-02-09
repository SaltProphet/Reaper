"""
KeywordScorer Plugin

A simple analyzer plugin that scores signals based on keyword matching.
Demonstrates real plugin implementation for Phase 2 kickoff.

Configuration:
    No environment variables required. Keywords are defined in code.

Usage:
    from reaper import PluginManager
    from reaper.plugins.keyword_scorer import KeywordScorerPlugin

    pm = PluginManager()
    pm.register_plugin(KeywordScorerPlugin(), name="keyword_scorer")

    # Score signals
    signal = Signal(sense_type=SenseType.SIGHT, source="test")
    scored = pm.score_signal(signal)
"""

import pluggy

from reaper.models import ScoredSignal, Signal

hookimpl = pluggy.HookimplMarker("reaper")


class KeywordScorerPlugin:
    """
    Scores signals based on keyword matching in raw_data.

    Scoring algorithm:
    - Base score: 0.0
    - Each high-priority keyword found: +0.3 (capped at 1.0)
    - Each medium-priority keyword found: +0.2 (capped at 1.0)
    - Each low-priority keyword found: +0.1 (capped at 1.0)

    Keywords are matched case-insensitively in signal.raw_data values.
    """

    # Default keyword priorities
    HIGH_PRIORITY_KEYWORDS = ["urgent", "critical", "blocker", "emergency", "broken"]
    MEDIUM_PRIORITY_KEYWORDS = ["bug", "issue", "problem", "error", "failure"]
    LOW_PRIORITY_KEYWORDS = ["todo", "improvement", "enhancement", "minor", "question"]

    def __init__(
        self,
        high_priority: list[str] | None = None,
        medium_priority: list[str] | None = None,
        low_priority: list[str] | None = None,
    ):
        """
        Initialize KeywordScorer with custom keyword priorities.

        Args:
            high_priority: High-priority keywords (score +0.3 each)
            medium_priority: Medium-priority keywords (score +0.2 each)
            low_priority: Low-priority keywords (score +0.1 each)
        """
        self.high_priority = high_priority or self.HIGH_PRIORITY_KEYWORDS
        self.medium_priority = medium_priority or self.MEDIUM_PRIORITY_KEYWORDS
        self.low_priority = low_priority or self.LOW_PRIORITY_KEYWORDS

    def _extract_text_from_data(self, data: dict) -> str:
        """
        Extract all text values from signal raw_data.

        Args:
            data: Dictionary of signal data

        Returns:
            Concatenated lowercase string of all values
        """
        text_parts = []
        for value in data.values():
            if isinstance(value, str):
                text_parts.append(value.lower())
            elif isinstance(value, (list, dict)):
                # Recursively handle nested structures
                text_parts.append(str(value).lower())
        return " ".join(text_parts)

    def _calculate_score(self, signal: Signal) -> tuple[float, dict]:
        """
        Calculate score based on keyword matches.

        Args:
            signal: Signal to score

        Returns:
            Tuple of (score, analysis_dict)
        """
        text = self._extract_text_from_data(signal.raw_data)

        # Count keyword matches
        high_matches = [kw for kw in self.high_priority if kw.lower() in text]
        medium_matches = [kw for kw in self.medium_priority if kw.lower() in text]
        low_matches = [kw for kw in self.low_priority if kw.lower() in text]

        # Calculate score
        score = 0.0
        score += len(high_matches) * 0.3
        score += len(medium_matches) * 0.2
        score += len(low_matches) * 0.1

        # Cap at 1.0
        score = min(score, 1.0)

        # Build analysis
        analysis = {
            "method": "keyword_matching",
            "high_priority_matches": high_matches,
            "medium_priority_matches": medium_matches,
            "low_priority_matches": low_matches,
            "total_matches": len(high_matches) + len(medium_matches) + len(low_matches),
        }

        return score, analysis

    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        """
        Score a detected signal based on keyword matching.

        Args:
            signal: Signal to score

        Returns:
            ScoredSignal: Signal with score (0.0-1.0) and analysis
        """
        score, analysis = self._calculate_score(signal)

        # Determine tags based on score
        tags = []
        if score >= 0.7:
            tags.append("high_priority")
        elif score >= 0.4:
            tags.append("medium_priority")
        else:
            tags.append("low_priority")

        if analysis["total_matches"] == 0:
            tags.append("no_keywords")

        return ScoredSignal(
            signal=signal,
            score=score,
            analysis=analysis,
            tags=tags,
        )
