# 🧪 Strands SDK Agent Testing Suite

Comprehensive testing framework for all 6 Strands SDK agents through the Streamlit UI interface. This suite simulates real user interactions and validates agent responses across multiple scenarios.

## 📋 Test Overview

### **Test Categories**

1. **🤖 Basic Agent Tests** - Tests fundamental agent capabilities
2. **🔬 Advanced Agent Tests** - Tests complex agent features  
3. **👤 User Scenario Tests** - Simulates realistic user interactions
4. **⚡ Performance Tests** - Measures response times and load handling
5. **🎯 Comprehensive Tests** - Full end-to-end testing

### **Agents Tested**

| Agent | Type | Capabilities Tested |
|-------|------|-------------------|
| Simple Agent | Basic | Conversational abilities, basic responses |
| Agent with Tools | Basic | Built-in tools (calculator, search, weather) |
| Custom Tool Agent | Basic | Custom tools (text analysis, hashing) |
| Web Research Agent | Advanced | Research capabilities, information gathering |
| File Manager Agent | Advanced | File operations, directory management |
| Multi Agent System | Advanced | Agent coordination, collaboration |

## 🚀 Quick Start

### **Run All Tests (Recommended)**
```bash
# Comprehensive testing of all agents
python tests/run_all_ui_tests.py

# Quick test (basic functionality only)
python tests/run_all_ui_tests.py --quick

# Check test environment
python tests/run_all_ui_tests.py --check
```

### **Run Specific Test Suites**
```bash
# Test basic agents only
python tests/test_ui_basic_agents.py

# Test advanced agents only  
python tests/test_ui_advanced_agents.py

# Test user scenarios
python tests/test_user_scenarios.py

# Performance testing
python tests/test_ui_performance.py
```

### **Individual Agent Testing**
```bash
# Test specific agent with scenarios
python tests/test_ui_agents.py --agent "Simple Agent"

# List available agents
python tests/test_ui_agents.py --list
```

## 📊 Test Types Explained

### **1. Basic Agent Tests (`test_ui_basic_agents.py`)**

Tests the three basic agents with focused test cases:

- **Simple Agent**: Conversational capabilities, greetings, self-description
- **Agent with Tools**: Math calculations, web search simulation, tool usage
- **Custom Tool Agent**: Text analysis, hash generation, custom capabilities

**Example Test Cases:**
```python
# Simple Agent
"Hello, how are you today?"
"What can you help me with?"
"Tell me about yourself"

# Agent with Tools  
"Calculate 25 * 17 + 83"
"What's the square root of 256?"
"Search for information about Python programming"

# Custom Tool Agent
"Analyze this text: 'The quick brown fox jumps over the lazy dog'"
"Generate a hash for the password 'test123'"
"What custom tools do you have?"
```

### **2. Advanced Agent Tests (`test_ui_advanced_agents.py`)**

Tests the three advanced agents with complex scenarios:

- **Web Research Agent**: Research capabilities, information gathering
- **File Manager Agent**: File operations, directory management
- **Multi Agent System**: Agent coordination, collaboration

**Example Test Cases:**
```python
# Web Research Agent
"Research the latest developments in artificial intelligence"
"Find information about climate change solutions"
"Compare Python vs JavaScript for beginners"

# File Manager Agent
"List the files in the current directory"
"Show me the project structure"
"What's in the docs folder?"

# Multi Agent System
"I need help with both calculations and research"
"Can you coordinate multiple agents to solve a problem?"
"What agents are available in the system?"
```

### **3. User Scenario Tests (`test_user_scenarios.py`)**

Simulates realistic user interactions with different personas:

**User Personas:**
- **Developer**: Software developer exploring AI agents
- **Researcher**: Academic researcher needing information
- **Business User**: Professional seeking efficiency
- **Student**: Learning about AI and technology
- **Curious Explorer**: General user exploring capabilities

**Scenario Examples:**
```python
# Developer Scenario with Custom Tool Agent
[
    "I need to analyze some text",
    "Analyze this: 'Machine learning is transforming industries'", 
    "Can you generate a hash for security purposes?",
    "What other custom tools do you have?"
]

# Researcher Scenario with Web Research Agent
[
    "I'm working on a research project",
    "Find information about sustainable energy solutions",
    "What are the latest trends in renewable energy?",
    "Can you research climate change mitigation strategies?"
]
```

### **4. Performance Tests (`test_ui_performance.py`)**

Measures system performance and stability:

- **Response Time Testing**: Measures average response times
- **Concurrent User Testing**: Tests multiple simultaneous users
- **Load Testing**: Evaluates system under stress
- **Performance Grading**: Assigns performance grades (A+ to F)

**Performance Metrics:**
- Average response time
- Success rate
- Throughput (requests/second)
- Concurrent user handling
- System stability

## 📈 Test Results and Reporting

### **Generated Reports**

All tests generate detailed reports in JSON and human-readable formats:

| File | Description |
|------|-------------|
| `master_ui_test_report.json` | Complete test execution results |
| `UI_TEST_REPORT.md` | Human-readable summary report |
| `basic_agents_ui_results.json` | Basic agent test details |
| `advanced_agents_ui_results.json` | Advanced agent test details |
| `user_scenario_results.json` | User scenario test results |
| `performance_test_results.json` | Performance test metrics |

### **Success Criteria**

Tests use the following success criteria:

- **Response Quality**: Keyword matching, response length, relevance
- **Success Rate**: Percentage of successful interactions
- **Performance**: Response time thresholds, concurrent handling
- **User Experience**: Persona-appropriate responses, conversation flow

**Grading Scale:**
- **A+ (90-100%)**: Excellent performance, production-ready
- **A (80-89%)**: Very good performance, minor improvements
- **B (70-79%)**: Good performance, some optimization needed
- **C (60-69%)**: Fair performance, improvements recommended
- **D (50-59%)**: Poor performance, significant work needed
- **F (<50%)**: Failing, major issues to resolve

## 🔧 Test Configuration

### **Model Configuration**
```python
model_config = {
    "provider": "bedrock",
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "temperature": 0.7,
    "max_tokens": 1000  # 1500 for advanced agents
}
```

### **Test Parameters**
- **Response Time Iterations**: 3-5 per test
- **Concurrent Users**: 3 simultaneous users
- **Keyword Matching Threshold**: 30% for basic, 40% for advanced
- **Minimum Response Length**: 50 chars basic, 100 chars advanced

## 🛠️ Troubleshooting

### **Common Issues**

**Environment Setup:**
```bash
# Check test environment
python tests/run_all_ui_tests.py --check

# Install missing dependencies
pip install -r requirements.txt
pip install -r ui/requirements_ui.txt
```

**Model Access Issues:**
- Ensure AWS credentials are configured
- Verify Bedrock model access in AWS console
- Check .env file configuration

**Import Errors:**
- Verify all test files are in the tests/ directory
- Check Python path configuration
- Ensure ui/ directory structure is correct

### **Test Debugging**

**Verbose Output:**
```bash
# Run individual tests for debugging
python tests/test_ui_basic_agents.py
python tests/test_ui_advanced_agents.py

# Test specific agent
python tests/test_ui_agents.py --agent "Simple Agent"
```

**Log Analysis:**
- Check generated JSON reports for detailed error information
- Review response times and success rates
- Analyze keyword matching results

## 📚 Best Practices

### **Running Tests**

1. **Start with Environment Check**: Always run `--check` first
2. **Use Quick Tests for Development**: Use `--quick` during development
3. **Run Comprehensive Tests for Release**: Full testing before deployment
4. **Monitor Performance**: Regular performance testing to catch regressions

### **Interpreting Results**

1. **Focus on Success Rates**: Aim for >80% success rate
2. **Monitor Response Times**: Keep average <5 seconds
3. **Check User Scenarios**: Ensure realistic interactions work well
4. **Review Performance Grades**: Maintain A/B grades for production

### **Test Maintenance**

1. **Update Test Cases**: Add new scenarios as agents evolve
2. **Adjust Thresholds**: Tune success criteria based on requirements
3. **Monitor Trends**: Track performance over time
4. **Document Changes**: Update test documentation with changes

## 🎯 Test Coverage

### **Functional Coverage**
- ✅ All 6 agents tested
- ✅ Basic and advanced capabilities
- ✅ Tool integration and usage
- ✅ Error handling and edge cases

### **User Experience Coverage**
- ✅ Multiple user personas
- ✅ Realistic conversation flows
- ✅ Various interaction patterns
- ✅ Different complexity levels

### **Performance Coverage**
- ✅ Response time measurement
- ✅ Concurrent user handling
- ✅ Load testing scenarios
- ✅ System stability validation

---

## 🚀 Getting Started

Ready to test your Strands SDK agents? Start here:

```bash
# 1. Check your environment
python tests/run_all_ui_tests.py --check

# 2. Run a quick test
python tests/run_all_ui_tests.py --quick

# 3. Run comprehensive tests
python tests/run_all_ui_tests.py --comprehensive

# 4. Review results
cat tests/UI_TEST_REPORT.md
```

**Happy Testing! 🧪✨**
