# Examples Guide - Strands Agents SDK Sample Project

This guide provides detailed explanations and usage examples for all the agents and tools in this sample project.

## Table of Contents

1. [Basic Agents](#basic-agents)
2. [Advanced Agents](#advanced-agents)
3. [Custom Tools](#custom-tools)
4. [Multi-Agent Systems](#multi-agent-systems)
5. [Best Practices](#best-practices)

## Basic Agents

### Simple Agent (`basic_agent/simple_agent.py`)

The simplest possible Strands agent using default settings.

**Key Features:**
- Uses AWS Bedrock with Claude 3.7 Sonnet (default)
- No custom tools - relies on model's built-in capabilities
- Demonstrates basic conversation flow

**Usage:**
```bash
python basic_agent/simple_agent.py
```

**Code Example:**
```python
from strands import Agent

# Create agent with default settings
agent = Agent()

# Simple conversation
response = agent("Hello! Can you introduce yourself?")
print(response)
```

**When to Use:**
- Quick prototyping
- Testing basic functionality
- Simple Q&A scenarios
- Learning Strands basics

### Agent with Built-in Tools (`basic_agent/agent_with_tools.py`)

Demonstrates using pre-built tools from the `strands-agents-tools` package.

**Key Features:**
- Uses calculator and current_time tools
- Shows both conversational and direct tool calling
- Demonstrates tool integration patterns

**Available Tools:**
- `calculator`: Mathematical calculations
- `current_time`: Current date and time

**Usage:**
```bash
python basic_agent/agent_with_tools.py
```

**Code Example:**
```python
from strands import Agent
from strands_tools import calculator, current_time

agent = Agent(
    tools=[calculator, current_time],
    system_prompt="You are a helpful assistant with calculation and time tools."
)

# Conversational tool use
response = agent("What time is it and what's 15% of 250?")

# Direct tool calling
calc_result = agent.tool.calculator(expression="sqrt(144)")
time_result = agent.tool.current_time()
```

**When to Use:**
- Need specific functionality (math, time, etc.)
- Want to leverage pre-built tools
- Building task-specific agents

### Custom Tool Agent (`basic_agent/custom_tool_agent.py`)

Shows how to create custom tools using Python decorators.

**Key Features:**
- Multiple custom tools with different purposes
- Demonstrates tool design patterns
- Shows parameter validation and error handling

**Custom Tools Included:**
- `word_count`: Count words in text
- `text_analyzer`: Comprehensive text analysis
- `password_generator`: Secure password generation
- `json_formatter`: JSON formatting and validation
- `list_operations`: List manipulation operations

**Usage:**
```bash
python basic_agent/custom_tool_agent.py
```

**Code Example:**
```python
from strands import Agent, tool

@tool
def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())

@tool
def text_analyzer(text: str) -> Dict[str, Any]:
    """Analyze text comprehensively."""
    # Implementation details...
    return analysis_results

agent = Agent(tools=[word_count, text_analyzer])
```

**Tool Design Best Practices:**
- Clear, descriptive docstrings (LLM uses these)
- Type hints for parameters and return values
- Proper error handling
- Reasonable parameter validation
- Return structured data when possible

## Advanced Agents

### Web Research Agent (`advanced_agent/web_research_agent.py`)

Demonstrates web research capabilities with search and scraping tools.

**Key Features:**
- Simulated web search (for demo purposes)
- Web page content extraction
- URL analysis and validation
- Research workflow coordination

**Tools Included:**
- `web_search_simulator`: Simulated search results
- `web_scraper`: Extract content from web pages
- `url_analyzer`: Analyze URL structure

**Usage:**
```bash
python advanced_agent/web_research_agent.py
```

**Code Example:**
```python
from strands import Agent, tool
import requests
from bs4 import BeautifulSoup

@tool
def web_scraper(url: str) -> Dict[str, Any]:
    """Scrape content from a web page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return {
        "title": soup.find('title').get_text(),
        "content": soup.get_text()[:2000]
    }

agent = Agent(
    tools=[web_scraper],
    system_prompt="You are a web research assistant..."
)
```

**Real-World Adaptations:**
- Replace `web_search_simulator` with actual search APIs (Google, Bing, DuckDuckGo)
- Add rate limiting and respect robots.txt
- Implement caching for frequently accessed content
- Add content filtering and safety checks

### File Manager Agent (`advanced_agent/file_manager_agent.py`)

Provides comprehensive file system operations with security constraints.

**Key Features:**
- Safe file operations (restricted to demo directory)
- Directory creation and listing
- File reading and writing
- File metadata and analysis

**Tools Included:**
- `create_directory`: Create directories safely
- `list_directory`: List directory contents
- `read_file`: Read text file contents
- `write_file`: Write content to files
- `file_info`: Get detailed file information

**Usage:**
```bash
python advanced_agent/file_manager_agent.py
```

**Security Features:**
- All operations restricted to safe directory
- Path traversal attack prevention
- File type validation
- Permission checking

**Code Example:**
```python
@tool
def write_file(file_path: str, content: str, append: bool = False) -> Dict[str, Any]:
    """Write content to a file safely."""
    safe_path = SAFE_DIR / file_path
    
    # Security check
    if not str(safe_path.resolve()).startswith(str(SAFE_DIR.resolve())):
        return {"success": False, "error": "Path outside safe directory"}
    
    # Write file
    with open(safe_path, 'a' if append else 'w') as f:
        f.write(content)
    
    return {"success": True, "path": str(safe_path)}
```

### Multi-Agent System (`advanced_agent/multi_agent_system.py`)

Demonstrates coordination between specialized agents.

**Key Features:**
- Multiple specialized agents (Math, Text, Format)
- Agent coordination and task delegation
- Complex workflow management
- Inter-agent communication patterns

**Specialist Agents:**
- **Math Agent**: Mathematical calculations and problem solving
- **Text Agent**: Text analysis and content insights
- **Format Agent**: Data formatting and presentation
- **Coordinator**: Task planning and agent orchestration

**Usage:**
```bash
python advanced_agent/multi_agent_system.py
```

**Code Example:**
```python
class MultiAgentSystem:
    def __init__(self):
        self.math_agent = Agent(
            tools=[calculate_math],
            system_prompt="You are a mathematics specialist..."
        )
        
        self.text_agent = Agent(
            tools=[analyze_text_content],
            system_prompt="You are a text analysis specialist..."
        )
        
        self.coordinator = Agent(
            system_prompt="You coordinate between specialist agents..."
        )
    
    def process_complex_task(self, task: str):
        # Coordinate between agents based on task requirements
        pass
```

## Custom Tools

### Tool Development Guidelines

**1. Tool Function Signature:**
```python
@tool
def tool_name(param1: type, param2: type = default) -> return_type:
    """Clear description of what the tool does.
    
    Args:
        param1: Description of parameter
        param2: Description of optional parameter
        
    Returns:
        Description of return value
    """
    # Implementation
    return result
```

**2. Error Handling:**
```python
@tool
def safe_tool(input_data: str) -> Dict[str, Any]:
    """Tool with proper error handling."""
    try:
        result = process_data(input_data)
        return {"success": True, "result": result}
    except ValueError as e:
        return {"success": False, "error": f"Invalid input: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}
```

**3. Input Validation:**
```python
@tool
def validated_tool(number: int, text: str) -> Dict[str, Any]:
    """Tool with input validation."""
    if not isinstance(number, int) or number < 0:
        return {"error": "Number must be a non-negative integer"}
    
    if not text or len(text.strip()) == 0:
        return {"error": "Text cannot be empty"}
    
    # Process validated inputs
    return {"result": f"Processed {number} items from '{text}'"}
```

### Tool Categories

**1. Data Processing Tools:**
- Text analysis and manipulation
- Mathematical calculations
- Data format conversions
- Content validation

**2. External Integration Tools:**
- Web scraping and API calls
- File system operations
- Database interactions
- Service integrations

**3. Utility Tools:**
- Password generation
- URL analysis
- Time and date operations
- Encoding/decoding functions

## Multi-Agent Systems

### Design Patterns

**1. Specialist Pattern:**
```python
# Each agent specializes in one domain
math_agent = Agent(tools=[calculator], system_prompt="Math specialist...")
text_agent = Agent(tools=[text_analyzer], system_prompt="Text specialist...")
```

**2. Coordinator Pattern:**
```python
# One agent coordinates others
coordinator = Agent(system_prompt="""
You coordinate between specialist agents:
- Math Agent: for calculations
- Text Agent: for text analysis
Use them based on task requirements.
""")
```

**3. Pipeline Pattern:**
```python
# Agents work in sequence
def process_pipeline(data):
    step1_result = agent1(data)
    step2_result = agent2(step1_result)
    return agent3(step2_result)
```

### Communication Strategies

**1. Direct Tool Calling:**
```python
# Agent A calls Agent B's tools directly
result = agent_a.tool.some_function(data)
```

**2. Message Passing:**
```python
# Agents communicate through structured messages
message = {"type": "request", "data": data, "from": "agent_a"}
response = agent_b.process_message(message)
```

**3. Shared Context:**
```python
# Agents share a common context or memory
shared_context = {"current_task": task, "results": {}}
agent_a.context = shared_context
agent_b.context = shared_context
```

## Best Practices

### Agent Design

**1. Clear System Prompts:**
```python
system_prompt = """You are a [role] with expertise in [domain].

Your capabilities:
- [capability 1]
- [capability 2]

When users ask for [task type]:
1. [step 1]
2. [step 2]
3. [step 3]

Always [behavior guideline].
"""
```

**2. Appropriate Tool Selection:**
- Use built-in tools for common tasks
- Create custom tools for specific needs
- Keep tools focused and single-purpose
- Provide comprehensive error handling

**3. Context Management:**
```python
agent = Agent(
    conversation_manager=SlidingWindowConversationManager(window_size=20),
    max_parallel_tools=4
)
```

### Error Handling

**1. Graceful Degradation:**
```python
try:
    result = agent.tool.complex_operation(data)
except Exception as e:
    # Fall back to simpler approach
    result = agent.tool.simple_operation(data)
```

**2. User-Friendly Error Messages:**
```python
if not result["success"]:
    user_message = f"I encountered an issue: {result['error']}"
    suggestion = "Please try rephrasing your request."
    return f"{user_message} {suggestion}"
```

### Performance Optimization

**1. Parallel Tool Execution:**
```python
agent = Agent(max_parallel_tools=4)  # Run up to 4 tools simultaneously
```

**2. Context Window Management:**
```python
from strands.agent.conversation_manager import SlidingWindowConversationManager

agent = Agent(
    conversation_manager=SlidingWindowConversationManager(window_size=30)
)
```

**3. Tool Result Caching:**
```python
@tool
def cached_expensive_operation(input_data: str) -> str:
    """Expensive operation with caching."""
    cache_key = hash(input_data)
    if cache_key in cache:
        return cache[cache_key]
    
    result = expensive_computation(input_data)
    cache[cache_key] = result
    return result
```

### Testing Strategies

**1. Unit Testing Tools:**
```python
def test_word_count_tool():
    result = word_count("hello world test")
    assert result == 3
```

**2. Integration Testing:**
```python
@pytest.mark.integration
def test_agent_with_tools():
    agent = Agent(tools=[word_count])
    response = agent("Count words in 'hello world'")
    assert "2" in str(response)
```

**3. Mock External Dependencies:**
```python
@patch('requests.get')
def test_web_scraper(mock_get):
    mock_get.return_value.content = b"<html>Test</html>"
    result = web_scraper("http://example.com")
    assert result["success"] is True
```

### Security Considerations

**1. Input Sanitization:**
```python
@tool
def safe_file_operation(filename: str) -> Dict[str, Any]:
    # Sanitize filename
    safe_filename = os.path.basename(filename)
    if '..' in safe_filename or safe_filename.startswith('/'):
        return {"error": "Invalid filename"}
    
    # Proceed with safe operation
```

**2. Restricted Execution:**
```python
# Use safe evaluation for mathematical expressions
safe_dict = {"__builtins__": {}, "sqrt": math.sqrt}
result = eval(expression, safe_dict)
```

**3. Rate Limiting:**
```python
@tool
def rate_limited_api_call(query: str) -> Dict[str, Any]:
    if not rate_limiter.allow_request():
        return {"error": "Rate limit exceeded"}
    
    return make_api_call(query)
```

This comprehensive guide should help you understand and extend the Strands Agents SDK sample project for your specific use cases.
