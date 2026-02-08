"""
Custom Plugin Example

This example shows how to create a custom plugin from scratch.

Run from repository root:
    python examples/custom_plugin_example.py
"""

from typing import List

import pluggy

from pipeline.action import ActionPlugin
from reaper import PluginManager
from reaper.models import ScoredSignal, SenseType, Signal

# Create the hookimpl marker
hookimpl = pluggy.HookimplMarker("reaper")


class CustomNewsPlugin:
    """
    Custom plugin that detects news signals.
    
    This is a Hearing plugin that monitors text-based news sources.
    """

    def __init__(self, keywords: List[str] = None):
        """
        Initialize with optional keyword filters.
        
        Args:
            keywords: List of keywords to filter for (e.g., ["AI", "Python"])
        """
        self.keywords = keywords or ["technology", "innovation"]

    @hookimpl
    def reaper_hearing_detect(self, source: str) -> List[Signal]:
        """
        Detect news signals from a text source.
        
        Args:
            source: The news source identifier
            
        Returns:
            List of Signal objects
        """
        print(f"    → CustomNewsPlugin detecting from '{source}'")

        # In a real plugin, you'd fetch from an API or RSS feed
        # For this example, we'll simulate some news items
        mock_news = [
            {
                "title": "New AI breakthrough announced",
                "content": "Researchers unveil revolutionary AI technology...",
                "url": f"https://{source}/article1",
                "keywords": ["AI", "technology"],
            },
            {
                "title": "Python 3.12 released",
                "content": "Latest Python version brings performance improvements...",
                "url": f"https://{source}/article2",
                "keywords": ["Python", "technology"],
            },
            {
                "title": "Open source project gains traction",
                "content": "Community-driven project reaches 10k stars...",
                "url": f"https://{source}/article3",
                "keywords": ["open-source", "innovation"],
            },
        ]

        # Filter by keywords
        filtered_news = [
            item for item in mock_news
            if any(kw.lower() in [k.lower() for k in item["keywords"]]
                   for kw in self.keywords)
        ]

        # Convert to Signal objects
        signals = []
        for item in filtered_news:
            signal = Signal(
                sense_type=SenseType.HEARING,
                source=source,
                raw_data={
                    "title": item["title"],
                    "content": item["content"],
                    "url": item["url"],
                    "keywords": item["keywords"],
                }
            )
            signals.append(signal)

        return signals


class CustomPriorityScorer:
    """
    Custom scoring plugin that prioritizes based on keywords.
    """

    def __init__(self, high_priority_keywords: List[str] = None):
        """
        Initialize with high-priority keywords.
        
        Args:
            high_priority_keywords: Keywords that increase signal score
        """
        self.high_priority_keywords = high_priority_keywords or ["AI", "Python"]

    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        """
        Score a signal based on keyword matching.
        
        Args:
            signal: The signal to score
            
        Returns:
            ScoredSignal with calculated score
        """
        # Base score
        score = 0.5

        # Check if signal has our high-priority keywords
        if "keywords" in signal.raw_data:
            keywords = signal.raw_data["keywords"]
            matches = [kw for kw in keywords if kw in self.high_priority_keywords]

            # Increase score for each match
            score += len(matches) * 0.2
            score = min(1.0, score)  # Cap at 1.0

        # Add tags based on score
        tags = []
        if score >= 0.8:
            tags.append("urgent")
        if score >= 0.6:
            tags.append("important")
        tags.append("custom-scored")

        return ScoredSignal(
            signal=signal,
            score=score,
            analysis={
                "method": "keyword-priority",
                "matched_keywords": matches if "keywords" in signal.raw_data else [],
            },
            tags=tags
        )


def main():
    print("=" * 70)
    print("REAPER Custom Plugin Example")
    print("=" * 70)

    # Step 1: Initialize Plugin Manager
    print("\n[1] Initializing Plugin Manager...")
    pm = PluginManager()

    # Step 2: Register Custom Plugins
    print("\n[2] Registering custom plugins...")

    # Create plugin instances with configuration
    news_plugin = CustomNewsPlugin(keywords=["AI", "Python", "technology"])
    priority_scorer = CustomPriorityScorer(high_priority_keywords=["AI", "Python"])

    # Register plugins
    pm.register_plugin(news_plugin, name="custom-news")
    pm.register_plugin(priority_scorer, name="custom-scorer")
    pm.register_plugin(ActionPlugin(), name="action")

    print("    ✓ CustomNewsPlugin registered")
    print("    ✓ CustomPriorityScorer registered")
    print("    ✓ ActionPlugin registered")

    # Step 3: Detect Signals
    print("\n[3] Detecting news signals...")
    source = "tech-news-feed"
    signals = pm.detect_hearing(source=source)

    print(f"    ✓ Detected {len(signals)} news signals")
    for i, signal in enumerate(signals, 1):
        title = signal.raw_data.get("title", "Unknown")
        keywords = signal.raw_data.get("keywords", [])
        print(f"    {i}. {title}")
        print(f"       Keywords: {', '.join(keywords)}")

    # Step 4: Score Signals
    print("\n[4] Scoring signals with custom scorer...")
    scored_signals = []
    for signal in signals:
        scored = pm.score_signal(signal)[0]
        scored_signals.append(scored)

        title = signal.raw_data.get("title", "Unknown")
        print(f"    {title[:40]:40s} → Score: {scored.score:.2f}, Tags: {scored.tags}")

    # Step 5: Execute Actions
    print("\n[5] Executing actions on high-priority signals...")
    threshold = 0.6
    high_priority = [s for s in scored_signals if s.score >= threshold]

    print(f"    Found {len(high_priority)} signals above threshold {threshold}")

    for scored in high_priority:
        result = pm.execute_action(scored)[0]
        title = scored.signal.raw_data.get("title", "Unknown")
        status = "✓" if result.success else "✗"
        print(f"    {status} Actioned: {title}")

    # Summary
    print("\n" + "=" * 70)
    print("Custom Plugin Summary")
    print("=" * 70)
    print("Plugin:                   CustomNewsPlugin")
    print(f"Keywords monitored:       {news_plugin.keywords}")
    print(f"Signals detected:         {len(signals)}")
    print(f"High-priority signals:    {len(high_priority)}")
    print(f"Actions executed:         {len(high_priority)}")
    print("=" * 70)

    print("\n💡 Key Takeaways:")
    print("   1. Custom plugins are easy to create with @hookimpl")
    print("   2. Configuration is passed via constructor parameters")
    print("   3. Plugins remain independent and testable")
    print("   4. Each plugin has a single, clear responsibility")


if __name__ == "__main__":
    main()
