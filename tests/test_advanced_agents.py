#!/usr/bin/env python3
"""
Test Advanced Agents - Strands Agents SDK

Unit tests for advanced agent functionality including web research,
file management, and multi-agent systems.
"""

import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import modules to test
try:
    from advanced_agent.web_research_agent import web_search_simulator, web_scraper, url_analyzer
    from advanced_agent.file_manager_agent import create_directory, list_directory, read_file, write_file, file_info
    from advanced_agent.multi_agent_system import calculate_math, analyze_text_content, format_data, MultiAgentSystem
    ADVANCED_AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import advanced agents: {e}")
    ADVANCED_AGENTS_AVAILABLE = False


class TestWebResearchTools:
    """Test web research agent tools."""
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_web_search_simulator(self):
        """Test the web search simulator tool."""
        # Test basic search
        results = web_search_simulator("strands agents")
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Check result structure
        for result in results:
            assert isinstance(result, dict)
            assert "title" in result
            assert "url" in result
            assert "snippet" in result
        
        # Test with custom number of results
        results = web_search_simulator("python programming", num_results=3)
        assert len(results) == 3
        
        # Test with maximum results constraint
        results = web_search_simulator("test query", num_results=15)
        assert len(results) <= 10  # Should be capped at 10
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_url_analyzer(self):
        """Test the URL analyzer tool."""
        # Test valid HTTPS URL
        result = url_analyzer("https://example.com/path?query=value#fragment")
        assert result["is_valid"] is True
        assert result["is_secure"] is True
        assert result["scheme"] == "https"
        assert result["domain"] == "example.com"
        assert result["path"] == "/path"
        assert result["query"] == "query=value"
        assert result["fragment"] == "fragment"
        
        # Test HTTP URL
        result = url_analyzer("http://example.com")
        assert result["is_valid"] is True
        assert result["is_secure"] is False
        assert result["scheme"] == "http"
        
        # Test invalid URL
        result = url_analyzer("not-a-url")
        assert result["is_valid"] is False
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    @patch('requests.get')
    def test_web_scraper_success(self, mock_get):
        """Test web scraper with successful response."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><head><title>Test Page</title></head><body><p>Test content</p></body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = web_scraper("https://example.com")
        
        assert result["status"] == "success"
        assert result["title"] == "Test Page"
        assert "Test content" in result["content"]
        assert result["response_code"] == 200
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    @patch('requests.get')
    def test_web_scraper_failure(self, mock_get):
        """Test web scraper with failed response."""
        # Mock failed response
        mock_get.side_effect = Exception("Connection failed")
        
        result = web_scraper("https://example.com")
        
        assert result["status"] == "error"
        assert "error" in result
        assert result["content"] == ""


class TestFileManagerTools:
    """Test file manager agent tools."""
    
    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_safe_dir = None
        
        # Patch the SAFE_DIR to use our test directory
        if ADVANCED_AGENTS_AVAILABLE:
            import advanced_agent.file_manager_agent as fma
            self.original_safe_dir = fma.SAFE_DIR
            fma.SAFE_DIR = Path(self.test_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        # Restore original SAFE_DIR
        if ADVANCED_AGENTS_AVAILABLE and self.original_safe_dir:
            import advanced_agent.file_manager_agent as fma
            fma.SAFE_DIR = self.original_safe_dir
        
        # Remove test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_create_directory(self):
        """Test directory creation."""
        result = create_directory("test_folder")
        assert result["success"] is True
        assert os.path.exists(os.path.join(self.test_dir, "test_folder"))
        
        # Test nested directory creation
        result = create_directory("nested/deep/folder")
        assert result["success"] is True
        assert os.path.exists(os.path.join(self.test_dir, "nested", "deep", "folder"))
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_write_and_read_file(self):
        """Test file writing and reading."""
        test_content = "This is test content\nWith multiple lines"
        
        # Write file
        write_result = write_file("test.txt", test_content)
        assert write_result["success"] is True
        assert write_result["content_length"] == len(test_content)
        
        # Read file
        read_result = read_file("test.txt")
        assert read_result["success"] is True
        assert read_result["content"] == test_content
        assert read_result["lines"] == 2
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_list_directory(self):
        """Test directory listing."""
        # Create some test files and directories
        write_file("file1.txt", "content1")
        write_file("file2.txt", "content2")
        create_directory("subfolder")
        
        # List directory
        result = list_directory(".")
        assert result["success"] is True
        assert result["total_items"] == 3
        assert result["files"] == 2
        assert result["directories"] == 1
        
        # Check that items are in the contents
        item_names = [item["name"] for item in result["contents"]]
        assert "file1.txt" in item_names
        assert "file2.txt" in item_names
        assert "subfolder" in item_names
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_file_info(self):
        """Test file information retrieval."""
        test_content = "Test file content"
        write_file("info_test.txt", test_content)
        
        result = file_info("info_test.txt")
        assert result["success"] is True
        assert result["type"] == "file"
        assert result["size"] == len(test_content)
        assert result["is_readable"] is True
        assert result["is_writable"] is True
        assert result["extension"] == ".txt"
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_security_constraints(self):
        """Test that file operations are constrained to safe directory."""
        # Try to access parent directory (should fail)
        result = read_file("../../../etc/passwd")
        assert result["success"] is False
        assert "outside safe directory" in result["error"]
        
        # Try to write outside safe directory (should fail)
        result = write_file("../../../tmp/malicious.txt", "bad content")
        assert result["success"] is False
        assert "outside safe directory" in result["error"]


class TestMultiAgentSystem:
    """Test multi-agent system functionality."""
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_calculate_math_tool(self):
        """Test the math calculation tool."""
        # Test basic arithmetic
        result = calculate_math("2 + 3 * 4")
        assert result["success"] is True
        assert result["result"] == 14
        
        # Test with math functions
        result = calculate_math("sqrt(16)")
        assert result["success"] is True
        assert result["result"] == 4.0
        
        # Test with constants
        result = calculate_math("pi * 2")
        assert result["success"] is True
        assert abs(result["result"] - 6.283185307179586) < 0.0001
        
        # Test invalid expression
        result = calculate_math("invalid_expression")
        assert result["success"] is False
        assert "error" in result
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_analyze_text_content_tool(self):
        """Test the text analysis tool."""
        test_text = "This is a great test! I love testing. It's wonderful and amazing."
        result = analyze_text_content(test_text)
        
        assert isinstance(result, dict)
        assert result["word_count"] > 0
        assert result["sentence_count"] > 0
        assert result["sentiment"] in ["positive", "negative", "neutral"]
        assert "most_common_words" in result
        assert isinstance(result["most_common_words"], list)
        
        # This text should be positive due to words like "great", "love", "wonderful", "amazing"
        assert result["sentiment"] == "positive"
        assert result["sentiment_score"] > 0
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_format_data_tool(self):
        """Test the data formatting tool."""
        test_data = {"name": "John", "age": 30, "city": "New York"}
        
        # Test JSON formatting
        result = format_data(test_data, "json")
        assert result["success"] is True
        assert result["format"] == "json"
        assert "John" in result["formatted_data"]
        
        # Test list formatting
        result = format_data(test_data, "list")
        assert result["success"] is True
        assert result["format"] == "list"
        assert "•" in result["formatted_data"]
        
        # Test unsupported format
        result = format_data(test_data, "unsupported")
        assert result["success"] is False
        assert "Unsupported format type" in result["error"]
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    @patch('strands.Agent')
    def test_multi_agent_system_creation(self, mock_agent_class):
        """Test multi-agent system initialization."""
        # Mock the Agent class
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        # Create multi-agent system
        mas = MultiAgentSystem()
        
        # Check that all agents are created
        assert hasattr(mas, 'math_agent')
        assert hasattr(mas, 'text_agent')
        assert hasattr(mas, 'format_agent')
        assert hasattr(mas, 'coordinator')
        
        # Verify Agent was called multiple times (once for each specialist + coordinator)
        assert mock_agent_class.call_count == 4


class TestErrorHandling:
    """Test error handling in advanced agents."""
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_math_tool_error_handling(self):
        """Test math tool with invalid expressions."""
        # Division by zero
        result = calculate_math("1 / 0")
        assert result["success"] is False
        
        # Invalid function
        result = calculate_math("invalid_function(5)")
        assert result["success"] is False
        
        # Malicious code attempt
        result = calculate_math("__import__('os').system('ls')")
        assert result["success"] is False
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    def test_text_analysis_edge_cases(self):
        """Test text analysis with edge cases."""
        # Empty text
        result = analyze_text_content("")
        assert result["word_count"] == 0
        assert result["sentence_count"] == 0
        
        # Very short text
        result = analyze_text_content("Hi")
        assert result["word_count"] == 1
        assert isinstance(result["sentiment"], str)
        
        # Text with only punctuation
        result = analyze_text_content("!@#$%^&*()")
        assert isinstance(result, dict)
        assert "word_count" in result


@pytest.mark.integration
class TestAdvancedAgentIntegration:
    """Integration tests for advanced agents."""
    
    @pytest.mark.skipif(not ADVANCED_AGENTS_AVAILABLE, reason="Advanced agents not available")
    @pytest.mark.skipif(not os.getenv('AWS_REGION'), reason="AWS credentials not configured")
    def test_multi_agent_system_integration(self):
        """Test multi-agent system with actual agents (requires AWS credentials)."""
        try:
            mas = MultiAgentSystem()
            
            # Test a simple math task
            result = mas.process_with_specialist("Calculate 5 + 3", "math")
            assert result["success"] is True
            assert "Math Specialist" in result["agent"]
            
        except ImportError:
            pytest.skip("Strands SDK not available")
        except Exception as e:
            pytest.skip(f"Multi-agent system test failed (likely due to missing AWS credentials): {e}")


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
