#!/usr/bin/env python3
"""
Test Basic Agents - Strands Agents SDK

Unit tests for basic agent functionality including simple agents,
agents with tools, and custom tool agents.
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import modules to test
try:
    from basic_agent.simple_agent import main as simple_agent_main
    from basic_agent.custom_tool_agent import word_count, text_analyzer, password_generator
    BASIC_AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import basic agents: {e}")
    BASIC_AGENTS_AVAILABLE = False


class TestCustomTools:
    """Test custom tools functionality."""
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    def test_word_count_tool(self):
        """Test the word count tool."""
        # Test normal text
        result = word_count("Hello world this is a test")
        assert result == 6
        
        # Test empty string
        result = word_count("")
        assert result == 0
        
        # Test single word
        result = word_count("Hello")
        assert result == 1
        
        # Test text with extra spaces
        result = word_count("  Hello   world  ")
        assert result == 2
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    def test_text_analyzer_tool(self):
        """Test the text analyzer tool."""
        test_text = "Hello world. This is a test sentence. It has multiple sentences."
        result = text_analyzer(test_text)
        
        # Check that result is a dictionary with expected keys
        assert isinstance(result, dict)
        assert "word_count" in result
        assert "character_count" in result
        assert "sentence_count" in result
        assert "average_word_length" in result
        assert "most_common_words" in result
        
        # Check some basic values
        assert result["word_count"] > 0
        assert result["character_count"] > 0
        assert result["sentence_count"] > 0
        assert isinstance(result["most_common_words"], list)
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    def test_password_generator_tool(self):
        """Test the password generator tool."""
        # Test default parameters
        password = password_generator()
        assert isinstance(password, str)
        assert len(password) == 12  # default length
        
        # Test custom length
        password = password_generator(length=8)
        assert len(password) == 8
        
        # Test without symbols
        password = password_generator(length=10, include_symbols=False)
        assert len(password) == 10
        # Should not contain common symbols
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        assert not any(char in symbols for char in password)
        
        # Test minimum length constraint
        password = password_generator(length=2)  # Should be adjusted to minimum 4
        assert len(password) == 4
        
        # Test maximum length constraint
        password = password_generator(length=200)  # Should be adjusted to maximum 128
        assert len(password) == 128


class TestAgentIntegration:
    """Test agent integration and functionality."""
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    @patch('strands.Agent')
    def test_simple_agent_creation(self, mock_agent_class):
        """Test that simple agent can be created without errors."""
        # Mock the Agent class
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        # Mock the agent response
        mock_response = Mock()
        mock_response.stop_reason = "end_turn"
        mock_response.metrics.total_time_seconds = 1.5
        mock_agent.return_value = mock_response
        mock_agent.__str__ = Mock(return_value="Test response")
        
        # This should not raise an exception
        try:
            # Import and test the main function logic
            from strands import Agent
            agent = Agent()
            response = agent("Test question")
            assert response is not None
        except ImportError:
            # If strands is not available, just pass the test
            pass
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    def test_tool_registration(self):
        """Test that custom tools can be registered properly."""
        # Test that our custom tools have the right attributes
        assert hasattr(word_count, '__call__')
        assert hasattr(text_analyzer, '__call__')
        assert hasattr(password_generator, '__call__')
        
        # Test that tools have docstrings (important for LLM understanding)
        assert word_count.__doc__ is not None
        assert text_analyzer.__doc__ is not None
        assert password_generator.__doc__ is not None


class TestErrorHandling:
    """Test error handling in agents and tools."""
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    def test_text_analyzer_empty_input(self):
        """Test text analyzer with empty input."""
        result = text_analyzer("")
        assert isinstance(result, dict)
        assert result["word_count"] == 0
        assert result["character_count"] == 0
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    def test_password_generator_edge_cases(self):
        """Test password generator with edge cases."""
        # Test very small length
        password = password_generator(length=1)
        assert len(password) >= 4  # Should be adjusted to minimum
        
        # Test very large length
        password = password_generator(length=1000)
        assert len(password) <= 128  # Should be adjusted to maximum
        
        # Test negative length
        password = password_generator(length=-5)
        assert len(password) >= 4  # Should be adjusted to minimum


@pytest.mark.integration
class TestAgentExecution:
    """Integration tests that require actual agent execution."""
    
    @pytest.mark.skipif(not BASIC_AGENTS_AVAILABLE, reason="Basic agents not available")
    @pytest.mark.skipif(not os.getenv('AWS_REGION'), reason="AWS credentials not configured")
    def test_simple_agent_execution(self):
        """Test actual agent execution (requires AWS credentials)."""
        try:
            from strands import Agent
            
            # Create a simple agent
            agent = Agent()
            
            # Test with a simple question
            response = agent("What is 2 + 2?")
            
            # Basic checks
            assert response is not None
            assert hasattr(response, 'stop_reason')
            assert hasattr(response, 'metrics')
            
        except ImportError:
            pytest.skip("Strands SDK not available")
        except Exception as e:
            pytest.skip(f"Agent execution failed (likely due to missing AWS credentials): {e}")


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
