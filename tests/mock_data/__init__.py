"""
Mock Data Generator for Tests

Helper utilities to generate mock Signal objects for testing.
Provides configurable signal generation with various sense types and data.
"""

from datetime import datetime, timezone
from typing import Any

from reaper.models import SenseType, Signal


class MockDataGenerator:
    """
    Generate mock Signal objects for testing.

    Usage:
        from tests.mock_data.mock_generator import MockDataGenerator

        gen = MockDataGenerator()

        # Generate single signal
        signal = gen.signal(
            sense_type=SenseType.SIGHT,
            source="test-camera",
            raw_data={"frame": 1}
        )

        # Generate batch of signals
        signals = gen.signals_batch(
            sense_type=SenseType.HEARING,
            source="test-mic",
            count=5
        )
    """

    @staticmethod
    def signal(
        sense_type: SenseType = SenseType.SIGHT,
        source: str = "mock-source",
        raw_data: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> Signal:
        """
        Generate a single mock Signal.

        Args:
            sense_type: Sense type for the signal
            source: Source identifier
            raw_data: Raw signal data (default: {"mock": True})
            metadata: Additional metadata (default: {})
            timestamp: Signal timestamp (default: current UTC time)

        Returns:
            Mock Signal instance
        """
        if raw_data is None:
            raw_data = {"mock": True}
        if metadata is None:
            metadata = {}
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        return Signal(
            sense_type=sense_type,
            source=source,
            raw_data=raw_data,
            metadata=metadata,
            timestamp=timestamp,
        )

    @staticmethod
    def signals_batch(
        sense_type: SenseType = SenseType.SIGHT,
        source: str = "mock-source",
        count: int = 3,
        raw_data_template: dict[str, Any] | None = None,
    ) -> list[Signal]:
        """
        Generate multiple mock Signals with shared timestamp.

        Args:
            sense_type: Sense type for all signals
            source: Source identifier (appends index: source-0, source-1, ...)
            count: Number of signals to generate
            raw_data_template: Base raw_data (adds 'index' key for each signal)

        Returns:
            List of mock Signal instances
        """
        if raw_data_template is None:
            raw_data_template = {"mock": True}

        shared_timestamp = datetime.now(timezone.utc)

        signals = []
        for i in range(count):
            raw_data = raw_data_template.copy()
            raw_data["index"] = i

            signal = Signal(
                sense_type=sense_type,
                source=f"{source}-{i}",
                raw_data=raw_data,
                timestamp=shared_timestamp,
            )
            signals.append(signal)

        return signals

    @staticmethod
    def signal_with_keywords(
        keywords: list[str],
        sense_type: SenseType = SenseType.SIGHT,
        source: str = "mock-source",
    ) -> Signal:
        """
        Generate a mock Signal containing specific keywords for scoring tests.

        Args:
            keywords: Keywords to include in raw_data
            sense_type: Sense type for the signal
            source: Source identifier

        Returns:
            Mock Signal with keywords in raw_data
        """
        raw_data = {
            "text": " ".join(keywords),
            "keywords": keywords,
            "mock": True,
        }

        return Signal(
            sense_type=sense_type,
            source=source,
            raw_data=raw_data,
        )

    @staticmethod
    def signals_with_mixed_keywords(count: int = 5) -> list[Signal]:
        """
        Generate signals with varying keyword priorities for testing.

        Args:
            count: Number of signals to generate

        Returns:
            List of signals with different keyword priorities:
            - High priority: urgent, critical
            - Medium priority: bug, issue
            - Low priority: todo, minor
            - No keywords: empty text
        """
        keyword_sets = [
            ["urgent", "critical"],  # High priority
            ["bug", "issue"],  # Medium priority
            ["todo", "minor"],  # Low priority
            [],  # No keywords
            ["urgent", "bug", "todo"],  # Mixed priorities
        ]

        signals = []
        for i in range(min(count, len(keyword_sets))):
            keywords = keyword_sets[i]
            signal = MockDataGenerator.signal_with_keywords(
                keywords=keywords,
                source=f"mixed-source-{i}",
            )
            signals.append(signal)

        return signals
