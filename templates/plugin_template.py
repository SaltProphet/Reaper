"""
[PLUGIN NAME] Plugin for REAPER

[Brief description of what this plugin does - 1-2 sentences]

Example:
    from reaper import PluginManager
    from [your_plugin_file] import [YourPlugin]
    
    pm = PluginManager()
    pm.register_plugin([YourPlugin](), name="[plugin-name]")
    
    # For detection plugins:
    signals = pm.detect_[sense](source="[your-source-identifier]")
    
    # For scoring plugins:
    scored = pm.score_signal(signal)
    
    # For action plugins:
    result = pm.execute_action(scored_signal)
"""

import os
from typing import Any, Dict, List

import pluggy
from pydantic import BaseModel, Field

from reaper.models import ActionResult, ScoredSignal, SenseType, Signal

# Required: Pluggy hook implementation marker
hookimpl = pluggy.HookimplMarker("reaper")


# Optional: Plugin-specific configuration model
class PluginConfig(BaseModel):
    """
    Configuration for [Plugin Name].
    
    All sensitive values (API keys, tokens) should come from environment variables.
    """

    # Example configuration fields
    api_key: str = Field(
        ...,
        description="API key for [service]. Set via [PLUGIN_NAME]_API_KEY env var",
    )
    endpoint: str = Field(
        default="https://api.example.com",
        description="API endpoint URL",
    )
    timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Request timeout in seconds",
    )
    rate_limit: int = Field(
        default=100,
        ge=1,
        description="Maximum requests per minute",
    )

    @classmethod
    def from_env(cls) -> "PluginConfig":
        """
        Load configuration from environment variables.
        
        Required environment variables:
            [PLUGIN_NAME]_API_KEY: API key for authentication
        
        Optional environment variables:
            [PLUGIN_NAME]_ENDPOINT: Override default endpoint
            [PLUGIN_NAME]_TIMEOUT: Override default timeout
            [PLUGIN_NAME]_RATE_LIMIT: Override default rate limit
        
        Returns:
            PluginConfig instance
        
        Raises:
            KeyError: If required environment variables are missing
            ValidationError: If configuration values are invalid
        """
        return cls(
            api_key=os.environ["[PLUGIN_NAME]_API_KEY"],
            endpoint=os.environ.get("[PLUGIN_NAME]_ENDPOINT", "https://api.example.com"),
            timeout=int(os.environ.get("[PLUGIN_NAME]_TIMEOUT", "30")),
            rate_limit=int(os.environ.get("[PLUGIN_NAME]_RATE_LIMIT", "100")),
        )


# Optional: Plugin-specific data models
class PluginSpecificData(BaseModel):
    """Model for plugin-specific data stored in Signal.raw_data."""

    item_id: str = Field(..., description="Unique identifier for the item")
    title: str = Field(..., description="Item title")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# ==============================================================================
# DETECTION PLUGIN TEMPLATE
# Use this for sight, hearing, touch, taste, or smell detection plugins
# ==============================================================================


class DetectionPlugin:
    """
    [Plugin Name] detection plugin for REAPER.
    
    Detects signals from [source description].
    
    Implements: reaper_[sense]_detect hook
    
    Environment Variables:
        [PLUGIN_NAME]_API_KEY: Required API key
        [PLUGIN_NAME]_ENDPOINT: Optional API endpoint override
        [PLUGIN_NAME]_TIMEOUT: Optional timeout override (seconds)
    
    Example:
        >>> plugin = DetectionPlugin()
        >>> pm = PluginManager()
        >>> pm.register_plugin(plugin, name="[plugin-name]")
        >>> signals = pm.detect_[sense](source="[example-source]")
    """

    def __init__(self, config: PluginConfig | None = None):
        """
        Initialize the detection plugin.
        
        Args:
            config: Optional PluginConfig. If None, loads from environment.
        """
        self.config = config or PluginConfig.from_env()

    @hookimpl
    def reaper_sight_detect(self, source: str) -> List[Signal]:
        """
        Detect visual signals from the specified source.
        
        Change hook name to match your sense type:
        - reaper_sight_detect (visual)
        - reaper_hearing_detect (audio/text)
        - reaper_touch_detect (interaction)
        - reaper_taste_detect (quality/sampling)
        - reaper_smell_detect (pattern/anomaly)
        
        Args:
            source: Source identifier (e.g., "channel-name", "feed-url", "topic-id")
                   NEVER hard-code this value!
        
        Returns:
            List of Signal objects detected from the source
        
        Raises:
            RuntimeError: If detection fails due to API errors
            ValidationError: If response data is invalid
        """
        try:
            # 1. Fetch data from external source
            items = self._fetch_from_source(source)

            # 2. Convert to Signal objects
            # Use create_batch() for better performance with multiple signals
            signals_data = []
            for item in items:
                # Create plugin-specific data model
                item_data = PluginSpecificData(
                    item_id=item["id"],
                    title=item["title"],
                    metadata=item.get("metadata", {}),
                )

                signals_data.append(
                    {
                        "sense_type": SenseType.SIGHT,  # Change to match your sense
                        "source": source,  # Use the parameter, never hard-code!
                        "raw_data": item_data.model_dump(),
                        "metadata": {
                            "plugin": "[plugin-name]",
                            "endpoint": self.config.endpoint,
                        },
                    }
                )

            # Use create_batch for performance (30-40% faster)
            return Signal.create_batch(signals_data)

        except Exception as e:
            # Log error but don't expose sensitive info
            raise RuntimeError(f"Failed to detect signals from {source}: {type(e).__name__}") from e

    def _fetch_from_source(self, source: str) -> List[Dict[str, Any]]:
        """
        Fetch raw data from external source.
        
        Args:
            source: Source identifier
        
        Returns:
            List of raw item dictionaries
        
        Note:
            This is a placeholder. Implement actual API/data fetching here.
        """
        # TODO: Implement actual data fetching
        # Example:
        # response = requests.get(
        #     f"{self.config.endpoint}/items",
        #     params={"source": source},
        #     headers={"Authorization": f"Bearer {self.config.api_key}"},
        #     timeout=self.config.timeout,
        # )
        # response.raise_for_status()
        # return response.json()["items"]

        return [
            {"id": "1", "title": "Example Item 1"},
            {"id": "2", "title": "Example Item 2"},
        ]


# ==============================================================================
# SCORING PLUGIN TEMPLATE
# Use this for plugins that score/analyze signals
# ==============================================================================


class ScoringPlugin:
    """
    [Plugin Name] scoring plugin for REAPER.
    
    Scores signals based on [scoring criteria description].
    
    Implements: reaper_score_signal hook
    
    Example:
        >>> plugin = ScoringPlugin()
        >>> pm = PluginManager()
        >>> pm.register_plugin(plugin, name="[plugin-name]")
        >>> scored = pm.score_signal(signal)[0]
    """

    def __init__(self):
        """Initialize the scoring plugin."""
        pass

    @hookimpl
    def reaper_score_signal(self, signal: Signal) -> ScoredSignal:
        """
        Score a signal based on [criteria].
        
        Args:
            signal: Raw signal to score
        
        Returns:
            ScoredSignal with score (0.0-1.0) and analysis
        
        Note:
            Score must be in range [0.0, 1.0] or Pydantic will raise ValidationError
        """
        try:
            # 1. Calculate score based on signal data
            raw_score = self._calculate_score(signal)

            # 2. Ensure score is in valid range [0.0, 1.0]
            clamped_score = max(0.0, min(1.0, raw_score))

            # 3. Perform analysis
            analysis = self._analyze_signal(signal)

            # 4. Generate tags
            tags = self._generate_tags(signal, clamped_score)

            # 5. Return ScoredSignal
            return ScoredSignal(
                signal=signal,
                score=clamped_score,
                analysis=analysis,
                tags=tags,
            )

        except Exception as e:
            # On error, return neutral score with error info
            return ScoredSignal(
                signal=signal,
                score=0.5,
                analysis={"error": str(e), "method": "[plugin-name]"},
                tags=["error", "scoring-failed"],
            )

    def _calculate_score(self, signal: Signal) -> float:
        """
        Calculate raw score for signal.
        
        Args:
            signal: Signal to score
        
        Returns:
            Raw score (may be outside [0.0, 1.0] range)
        """
        # TODO: Implement your scoring logic
        # Example factors to consider:
        # - Signal freshness (timestamp)
        # - Data quality (raw_data completeness)
        # - Historical patterns
        # - External factors

        return 0.75  # Placeholder

    def _analyze_signal(self, signal: Signal) -> Dict[str, Any]:
        """
        Perform detailed analysis of signal.
        
        Args:
            signal: Signal to analyze
        
        Returns:
            Analysis results dictionary
        """
        # TODO: Implement analysis logic
        return {
            "method": "[plugin-name]",
            "factors": ["factor1", "factor2"],
            "confidence": 0.85,
        }

    def _generate_tags(self, signal: Signal, score: float) -> List[str]:
        """
        Generate classification tags for signal.
        
        Args:
            signal: Signal being scored
            score: Calculated score
        
        Returns:
            List of tag strings
        """
        tags = ["[plugin-name]"]

        # Add score-based tags
        if score >= 0.8:
            tags.append("high-priority")
        elif score >= 0.5:
            tags.append("medium-priority")
        else:
            tags.append("low-priority")

        # TODO: Add domain-specific tags based on signal content

        return tags


# ==============================================================================
# ACTION PLUGIN TEMPLATE
# Use this for plugins that execute actions on scored signals
# ==============================================================================


class ActionPlugin:
    """
    [Plugin Name] action plugin for REAPER.
    
    Executes [action description] on scored signals.
    
    Implements: reaper_action_execute hook
    
    Environment Variables:
        [PLUGIN_NAME]_API_KEY: Required API key
        [PLUGIN_NAME]_ENDPOINT: Optional API endpoint override
    
    Example:
        >>> plugin = ActionPlugin()
        >>> pm = PluginManager()
        >>> pm.register_plugin(plugin, name="[plugin-name]")
        >>> result = pm.execute_action(scored_signal)[0]
    """

    def __init__(self, config: PluginConfig | None = None):
        """
        Initialize the action plugin.
        
        Args:
            config: Optional PluginConfig. If None, loads from environment.
        """
        self.config = config or PluginConfig.from_env()

    @hookimpl
    def reaper_action_execute(self, scored_signal: ScoredSignal) -> ActionResult:
        """
        Execute action on a scored signal.
        
        Args:
            scored_signal: Scored signal to act upon
        
        Returns:
            ActionResult indicating success/failure and details
        """
        try:
            # 1. Decide whether to act based on score/tags
            if not self._should_act(scored_signal):
                return ActionResult(
                    signal=scored_signal,
                    action_type="[action-type]",
                    success=True,
                    result_data={"skipped": True, "reason": "Score below threshold"},
                )

            # 2. Perform the action
            result_data = self._perform_action(scored_signal)

            # 3. Return success result
            return ActionResult(
                signal=scored_signal,
                action_type="[action-type]",
                success=True,
                result_data=result_data,
            )

        except Exception as e:
            # 4. Return failure result on error
            return ActionResult(
                signal=scored_signal,
                action_type="[action-type]",
                success=False,
                result_data={},
                error=f"{type(e).__name__}: {str(e)}",
            )

    def _should_act(self, scored_signal: ScoredSignal) -> bool:
        """
        Determine if action should be taken on this signal.
        
        Args:
            scored_signal: Scored signal to evaluate
        
        Returns:
            True if action should be taken, False otherwise
        """
        # TODO: Implement action criteria
        # Common criteria:
        # - Score threshold: scored_signal.score >= 0.7
        # - Specific tags: "high-priority" in scored_signal.tags
        # - Time-based: Check signal.timestamp
        # - Rate limiting: Track recent actions

        return scored_signal.score >= 0.7

    def _perform_action(self, scored_signal: ScoredSignal) -> Dict[str, Any]:
        """
        Perform the actual action.
        
        Args:
            scored_signal: Scored signal to act on
        
        Returns:
            Dictionary with action result details
        
        Raises:
            RuntimeError: If action fails
        """
        # TODO: Implement actual action
        # Examples:
        # - Send notification (Slack, Discord, email)
        # - Create issue (GitHub, Jira)
        # - Update database
        # - Trigger workflow
        # - Call webhook

        # Example:
        # response = requests.post(
        #     f"{self.config.endpoint}/notify",
        #     json={
        #         "message": scored_signal.signal.raw_data.get("title"),
        #         "score": scored_signal.score,
        #         "source": scored_signal.signal.source,
        #     },
        #     headers={"Authorization": f"Bearer {self.config.api_key}"},
        #     timeout=self.config.timeout,
        # )
        # response.raise_for_status()
        # return response.json()

        return {
            "status": "completed",
            "timestamp": scored_signal.signal.timestamp.isoformat(),
            "message": "Action completed successfully",
        }


# ==============================================================================
# PLUGIN REGISTRATION EXAMPLE
# ==============================================================================

if __name__ == "__main__":
    """
    Example of registering and using the plugin.
    
    Run this file directly to test your plugin:
        python plugin_template.py
    """
    from reaper import PluginManager

    # Initialize plugin manager
    pm = PluginManager()

    # Register detection plugin
    detection = DetectionPlugin()
    pm.register_plugin(detection, name="example-detection")

    # Register scoring plugin
    scoring = ScoringPlugin()
    pm.register_plugin(scoring, name="example-scoring")

    # Register action plugin
    action = ActionPlugin()
    pm.register_plugin(action, name="example-action")

    # Example pipeline execution
    print("Running example pipeline...\n")

    # 1. Detect signals
    print("1. Detecting signals...")
    signals = pm.detect_sight(source="example-source")
    print(f"   Detected {len(signals)} signals\n")

    # 2. Score signals
    print("2. Scoring signals...")
    for signal in signals:
        scored = pm.score_signal(signal)[0]
        print(f"   Signal {signal.raw_data.get('item_id')}: score={scored.score:.2f}")

        # 3. Execute actions on high-scoring signals
        if scored.score >= 0.7:
            print("   Executing action...")
            result = pm.execute_action(scored)[0]
            print(f"   Action {'succeeded' if result.success else 'failed'}\n")
