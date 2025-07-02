# 🧪 Strands SDK Agent Testing Suite

Comprehensive testing framework for all 6 Strands SDK agents. This suite provides direct agent testing through Python unit tests and integration tests.

## 🚀 Quick Start

### **Setup Testing Environment**
```bash
# Install testing dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/
```

### **Run Tests**
```bash
# Test all agents
python tests/test_agents.py

# Test basic agents only
python -m pytest tests/test_basic_agents.py

# Test advanced agents only  
python -m pytest tests/test_advanced_agents.py

# Run with verbose output
python -m pytest tests/ -v
```

## 🎯 Test Overview

### **Test Categories**
- **🤖 Basic Agent Tests** - Simple conversational agents
- **🔧 Advanced Agent Tests** - Complex agents with tools and capabilities
- **🧪 Integration Tests** - End-to-end agent functionality
- **⚡ Unit Tests** - Individual component testing

### **Agents Tested**
1. **Simple Agent** - Basic conversational AI
2. **Agent with Tools** - Calculator, web search, file operations
3. **Custom Tool Agent** - Custom Python function tools
4. **Web Research Agent** - Advanced web research capabilities
5. **File Manager Agent** - File system operations
6. **Multi-Agent System** - Collaborative agent interactions

## 📋 Test Files

### **Main Test Files**
- `test_agents.py` - Comprehensive agent functionality tests
- `test_basic_agents.py` - Basic agent conversation tests
- `test_advanced_agents.py` - Advanced agent capability tests

### **Generated Reports**
- Test results are displayed in console output
- Use pytest's built-in reporting for detailed analysis
- Add `--html=report.html` for HTML test reports

## 🔧 How Testing Works

### **Direct Agent Testing**
```python
# Example test structure
def test_simple_agent():
    """Test basic agent conversation"""
    agent = create_simple_agent()
    response = agent.chat("Hello, how are you?")
    assert response is not None
    assert len(response) > 0
```

### **Tool Integration Testing**
```python
# Example tool test
def test_agent_with_calculator():
    """Test agent calculator functionality"""
    agent = create_agent_with_tools()
    response = agent.chat("What is 15 + 27?")
    assert "42" in response
```

### **Multi-Agent Testing**
```python
# Example multi-agent test
def test_multi_agent_collaboration():
    """Test agent collaboration"""
    system = create_multi_agent_system()
    result = system.process_complex_task("Research and analyze topic")
    assert result.success
```

## 🛠️ Test Configuration

### **Environment Variables**
Create a `.env` file in the project root:
```bash
# Model Configuration
MODEL_PROVIDER=bedrock
AWS_REGION=us-east-1

# Testing Configuration
TEST_TIMEOUT=30
VERBOSE_TESTING=true
```

### **AWS Configuration**
Ensure AWS credentials are configured:
```bash
aws configure
# or set environment variables:
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## 🐛 Troubleshooting

### **Common Issues**

**Import Errors:**
```bash
# Ensure project is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**AWS Credential Issues:**
```bash
# Check AWS configuration
aws sts get-caller-identity

# Configure if needed
aws configure
```

**Model Access Issues:**
- Ensure Claude 3.7 Sonnet is enabled in AWS Bedrock console
- Check region availability for your selected models
- Verify IAM permissions for Bedrock access

**Timeout Issues:**
```bash
# Increase timeout in test configuration
export TEST_TIMEOUT=60
```

## 📊 Test Results Analysis

### **Understanding Test Output**
- ✅ **PASS** - Agent responded correctly
- ❌ **FAIL** - Agent failed to respond or gave incorrect response
- ⚠️ **SKIP** - Test skipped due to configuration issues
- 🔄 **RETRY** - Test retried due to temporary issues

### **Performance Metrics**
- **Response Time** - How quickly agents respond
- **Success Rate** - Percentage of successful interactions
- **Tool Usage** - Effectiveness of tool integration
- **Error Handling** - How well agents handle edge cases

## 📈 Best Practices

### **Running Tests**
1. **Start with Basic Tests**: Run simple agent tests first
2. **Check Configuration**: Ensure AWS and environment setup
3. **Monitor Output**: Watch for error patterns
4. **Analyze Results**: Review failed tests for improvements

### **Test Development**
1. **Write Clear Tests**: Use descriptive test names and assertions
2. **Test Edge Cases**: Include error conditions and boundary cases
3. **Mock External Services**: Use mocks for reliable testing
4. **Document Expectations**: Clear comments on test objectives

### **Debugging Failed Tests**
1. **Check Logs**: Review agent logs for error details
2. **Verify Configuration**: Ensure all environment variables are set
3. **Test Isolation**: Run individual tests to isolate issues
4. **Update Dependencies**: Ensure all packages are current

## 🎯 Advanced Testing

### **Custom Test Scenarios**
```python
# Create custom test scenarios
def test_custom_scenario():
    """Test specific use case"""
    agent = create_agent()
    # Your custom test logic here
    pass
```

### **Performance Testing**
```python
import time

def test_agent_performance():
    """Test agent response time"""
    agent = create_agent()
    start_time = time.time()
    response = agent.chat("Quick question")
    response_time = time.time() - start_time
    assert response_time < 10  # Should respond within 10 seconds
```

### **Stress Testing**
```python
def test_agent_stress():
    """Test agent under load"""
    agent = create_agent()
    for i in range(100):
        response = agent.chat(f"Question {i}")
        assert response is not None
```

## 🎉 Benefits of Direct Testing

### **Reliable Testing**
- **Direct Integration**: Tests actual agent code without UI dependencies
- **Fast Execution**: No browser startup or UI rendering delays
- **Consistent Results**: Eliminates UI timing and rendering issues

### **Comprehensive Coverage**
- **Unit Testing**: Test individual components in isolation
- **Integration Testing**: Test complete agent workflows
- **Error Handling**: Test edge cases and error conditions

### **Easy Debugging**
- **Direct Access**: Full access to agent internals and logs
- **Stack Traces**: Clear error reporting and debugging information
- **Isolated Testing**: Test specific functionality without external dependencies

---

## 🧪 Getting Started with Agent Testing

Ready to test your Strands SDK agents with comprehensive Python tests?

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Run all tests
python -m pytest tests/ -v

# 4. Review results
# Check console output for detailed results
```

**Happy Testing! 🧪✨**