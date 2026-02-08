"""
Tests for REAPER plugin manager.

Validates Pluggy integration and plugin registration.
"""
import pytest
from reaper import PluginManager, Signal, ScoredSignal, ActionResult, SenseType
from pipeline.sight import SightPlugin
from pipeline.hearing import HearingPlugin
from pipeline.touch import TouchPlugin
from pipeline.taste import TastePlugin
from pipeline.smell import SmellPlugin
from pipeline.action import ActionPlugin
from pipeline.scoring import ScoringPlugin


class TestPluginManager:
    """Test plugin manager functionality."""
    
    def test_plugin_manager_creation(self):
        """Test creating a plugin manager."""
        pm = PluginManager()
        assert pm is not None
        assert len(pm.list_plugins()) == 0
    
    def test_register_plugin(self):
        """Test registering a plugin."""
        pm = PluginManager()
        plugin = SightPlugin()
        pm.register_plugin(plugin, name="test-sight")
        assert len(pm.list_plugins()) == 1
    
    def test_unregister_plugin(self):
        """Test unregistering a plugin."""
        pm = PluginManager()
        plugin = SightPlugin()
        pm.register_plugin(plugin)
        pm.unregister_plugin(plugin)
        assert len(pm.list_plugins()) == 0
    
    def test_detect_sight(self):
        """Test sight detection via plugin."""
        pm = PluginManager()
        pm.register_plugin(SightPlugin())
        signals = pm.detect_sight(source="test-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.SIGHT for s in signals)
    
    def test_detect_hearing(self):
        """Test hearing detection via plugin."""
        pm = PluginManager()
        pm.register_plugin(HearingPlugin())
        signals = pm.detect_hearing(source="test-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.HEARING for s in signals)
    
    def test_detect_touch(self):
        """Test touch detection via plugin."""
        pm = PluginManager()
        pm.register_plugin(TouchPlugin())
        signals = pm.detect_touch(source="test-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.TOUCH for s in signals)
    
    def test_detect_taste(self):
        """Test taste detection via plugin."""
        pm = PluginManager()
        pm.register_plugin(TastePlugin())
        signals = pm.detect_taste(source="test-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.TASTE for s in signals)
    
    def test_detect_smell(self):
        """Test smell detection via plugin."""
        pm = PluginManager()
        pm.register_plugin(SmellPlugin())
        signals = pm.detect_smell(source="test-source")
        assert len(signals) > 0
        assert all(s.sense_type == SenseType.SMELL for s in signals)
    
    def test_score_signal(self):
        """Test signal scoring via plugin."""
        pm = PluginManager()
        pm.register_plugin(ScoringPlugin())
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = pm.score_signal(signal)
        assert len(scored) > 0
        assert all(isinstance(s, ScoredSignal) for s in scored)
    
    def test_execute_action(self):
        """Test action execution via plugin."""
        pm = PluginManager()
        pm.register_plugin(ActionPlugin())
        signal = Signal(sense_type=SenseType.SIGHT, source="test")
        scored = ScoredSignal(signal=signal, score=0.8)
        results = pm.execute_action(scored)
        assert len(results) > 0
        assert all(isinstance(r, ActionResult) for r in results)
    
    def test_full_pipeline(self):
        """Test complete pipeline with all plugins."""
        pm = PluginManager()
        pm.register_plugin(SightPlugin())
        pm.register_plugin(ScoringPlugin())
        pm.register_plugin(ActionPlugin())
        
        # Detect
        signals = pm.detect_sight(source="test-source")
        assert len(signals) > 0
        
        # Score
        scored = pm.score_signal(signals[0])
        assert len(scored) > 0
        
        # Act
        results = pm.execute_action(scored[0])
        assert len(results) > 0
        assert results[0].success is True
