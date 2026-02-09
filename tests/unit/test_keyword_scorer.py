"""
Unit Tests for KeywordScorer Plugin

Tests the keyword-based scoring logic of the KeywordScorerPlugin.
"""


from reaper.models import ScoredSignal, SenseType, Signal
from reaper.plugins.keyword_scorer import KeywordScorerPlugin


class TestKeywordScorerPlugin:
    """Test KeywordScorerPlugin scoring logic."""

    def test_plugin_initialization_defaults(self):
        """Test plugin initializes with default keyword lists."""
        plugin = KeywordScorerPlugin()

        assert len(plugin.high_priority) > 0
        assert len(plugin.medium_priority) > 0
        assert len(plugin.low_priority) > 0
        assert "urgent" in plugin.high_priority
        assert "bug" in plugin.medium_priority
        assert "todo" in plugin.low_priority

    def test_plugin_initialization_custom(self):
        """Test plugin initializes with custom keyword lists."""
        plugin = KeywordScorerPlugin(
            high_priority=["custom_high"],
            medium_priority=["custom_medium"],
            low_priority=["custom_low"],
        )

        assert plugin.high_priority == ["custom_high"]
        assert plugin.medium_priority == ["custom_medium"]
        assert plugin.low_priority == ["custom_low"]

    def test_score_signal_with_high_priority_keyword(self):
        """Test scoring signal with high-priority keyword."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "This is urgent and needs attention"},
        )

        scored = plugin.reaper_score_signal(signal)

        assert isinstance(scored, ScoredSignal)
        assert scored.signal == signal
        assert scored.score == 0.3  # One high-priority keyword
        assert "urgent" in scored.analysis["high_priority_matches"]
        assert "low_priority" in scored.tags  # 0.3 < 0.4 threshold

    def test_score_signal_with_medium_priority_keyword(self):
        """Test scoring signal with medium-priority keyword."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.HEARING,
            source="test",
            raw_data={"text": "Found a bug in the system"},
        )

        scored = plugin.reaper_score_signal(signal)

        assert scored.score == 0.2  # One medium-priority keyword
        assert "bug" in scored.analysis["medium_priority_matches"]
        assert "low_priority" in scored.tags

    def test_score_signal_with_low_priority_keyword(self):
        """Test scoring signal with low-priority keyword."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.TOUCH,
            source="test",
            raw_data={"text": "This is a minor enhancement"},
        )

        scored = plugin.reaper_score_signal(signal)

        assert scored.score == 0.2  # Two low-priority keywords: minor + enhancement
        assert "minor" in scored.analysis["low_priority_matches"]
        assert "enhancement" in scored.analysis["low_priority_matches"]
        assert "low_priority" in scored.tags

    def test_score_signal_with_multiple_keywords(self):
        """Test scoring signal with multiple keywords."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.SMELL,
            source="test",
            raw_data={
                "title": "Critical bug detected",
                "description": "This is urgent and broken",
            },
        )

        scored = plugin.reaper_score_signal(signal)

        # critical (0.3) + urgent (0.3) + broken (0.3) + bug (0.2) = 1.1 -> capped at 1.0
        assert scored.score == 1.0
        assert len(scored.analysis["high_priority_matches"]) == 3
        assert len(scored.analysis["medium_priority_matches"]) == 1
        assert scored.analysis["total_matches"] == 4
        assert "high_priority" in scored.tags

    def test_score_signal_with_no_keywords(self):
        """Test scoring signal with no matching keywords."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.TASTE,
            source="test",
            raw_data={"text": "Just some normal text"},
        )

        scored = plugin.reaper_score_signal(signal)

        assert scored.score == 0.0
        assert scored.analysis["total_matches"] == 0
        assert "no_keywords" in scored.tags
        assert "low_priority" in scored.tags

    def test_score_signal_with_empty_raw_data(self):
        """Test scoring signal with empty raw_data."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={},
        )

        scored = plugin.reaper_score_signal(signal)

        assert scored.score == 0.0
        assert scored.analysis["total_matches"] == 0
        assert "no_keywords" in scored.tags

    def test_score_signal_case_insensitive(self):
        """Test keyword matching is case-insensitive."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "URGENT CRITICAL BUG"},
        )

        scored = plugin.reaper_score_signal(signal)

        assert scored.score == 0.8  # urgent (0.3) + critical (0.3) + bug (0.2) = 0.8
        assert "urgent" in scored.analysis["high_priority_matches"]
        assert "critical" in scored.analysis["high_priority_matches"]
        assert "bug" in scored.analysis["medium_priority_matches"]

    def test_score_signal_with_nested_data(self):
        """Test scoring with nested data structures."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.HEARING,
            source="test",
            raw_data={
                "metadata": {
                    "tags": ["urgent", "bug"],
                    "priority": "critical",
                },
                "content": "This is broken",
            },
        )

        scored = plugin.reaper_score_signal(signal)

        # Should find keywords in nested structures
        assert scored.score >= 0.6  # At least critical + bug + broken
        assert scored.analysis["total_matches"] >= 2

    def test_tagging_logic(self):
        """Test that tags are assigned correctly based on score."""
        plugin = KeywordScorerPlugin()

        # High priority (score >= 0.7)
        signal_high = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "urgent critical blocker"},
        )
        scored_high = plugin.reaper_score_signal(signal_high)
        assert "high_priority" in scored_high.tags

        # Medium priority (0.4 <= score < 0.7)
        signal_medium = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "bug issue"},
        )
        scored_medium = plugin.reaper_score_signal(signal_medium)
        assert "medium_priority" in scored_medium.tags

        # Low priority (score < 0.4)
        signal_low = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "todo"},
        )
        scored_low = plugin.reaper_score_signal(signal_low)
        assert "low_priority" in scored_low.tags

    def test_analysis_structure(self):
        """Test that analysis contains expected keys and structure."""
        plugin = KeywordScorerPlugin()
        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": "urgent bug todo"},
        )

        scored = plugin.reaper_score_signal(signal)
        analysis = scored.analysis

        assert "method" in analysis
        assert analysis["method"] == "keyword_matching"
        assert "high_priority_matches" in analysis
        assert "medium_priority_matches" in analysis
        assert "low_priority_matches" in analysis
        assert "total_matches" in analysis
        assert isinstance(analysis["high_priority_matches"], list)
        assert isinstance(analysis["medium_priority_matches"], list)
        assert isinstance(analysis["low_priority_matches"], list)
        assert isinstance(analysis["total_matches"], int)

    def test_score_capped_at_one(self):
        """Test that score never exceeds 1.0 even with many keywords."""
        plugin = KeywordScorerPlugin()

        # Create signal with many high-priority keywords
        keywords = " ".join(plugin.high_priority * 5)  # Repeat keywords multiple times
        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={"text": keywords},
        )

        scored = plugin.reaper_score_signal(signal)

        assert scored.score <= 1.0
        assert scored.score == 1.0  # Should be capped

    def test_extract_text_from_various_types(self):
        """Test text extraction handles different data types."""
        plugin = KeywordScorerPlugin()

        signal = Signal(
            sense_type=SenseType.SIGHT,
            source="test",
            raw_data={
                "string": "urgent",
                "number": 123,
                "list": ["bug", "issue"],
                "dict": {"nested": "critical"},
                "bool": True,
            },
        )

        scored = plugin.reaper_score_signal(signal)

        # Should find keywords despite different types
        assert scored.score > 0
        assert scored.analysis["total_matches"] >= 2  # At least urgent and critical
