# 🎭 Strands SDK Agent Playwright Testing Suite

Comprehensive browser-based testing framework for all 6 Strands SDK agents using Playwright. This suite provides realistic UI testing by actually interacting with the Streamlit web interface through automated browser actions.

## 🚀 Quick Start

### **Setup Playwright**
```bash
# Install Playwright and dependencies
pip install -r tests/requirements_playwright.txt

# Install browser binaries
playwright install chromium

# Or use the automated setup
python tests/run_playwright_tests.py --install
```

### **Run Tests**
```bash
# Test all agents with realistic conversations
python tests/test_individual_agents.py --all

# Test specific agent
python tests/test_individual_agents.py --agent "Simple Agent"

# Run comprehensive UI tests
python tests/test_streamlit_ui.py

# Check setup
python tests/run_playwright_tests.py --check
```

## 🎯 Test Overview

### **What Gets Tested**

| Agent | Conversation Flow | Key Interactions |
|-------|------------------|------------------|
| **Simple Agent** | Introduction & capabilities | Basic conversation, self-description |
| **Agent with Tools** | Tool demonstration | Math calculations, web search |
| **Custom Tool Agent** | Custom capabilities | Text analysis, hash generation |
| **Web Research Agent** | Research scenarios | Information gathering, trend analysis |
| **File Manager Agent** | File operations | Directory listing, project structure |
| **Multi Agent System** | Coordination demo | Agent collaboration, system overview |

### **Test Types**

1. **🤖 Individual Agent Tests** - Focused conversation flows
2. **🎭 Comprehensive UI Tests** - Full interface testing
3. **👤 User Persona Tests** - Realistic user scenarios
4. **🔄 Browser Automation** - Actual UI interactions

## 📋 Test Files

### **Main Test Files**
- `test_streamlit_ui.py` - Comprehensive Playwright UI tests
- `test_individual_agents.py` - Individual agent conversation tests
- `run_playwright_tests.py` - Test runner and setup utility

### **Generated Reports**
- `playwright_ui_results.json` - Comprehensive test results
- `all_agents_playwright_results.json` - Individual agent results
- `{agent_name}_test_result.json` - Specific agent results

## 🎭 How Playwright Testing Works

### **Browser Automation**
```python
# Real browser interactions
await page.goto("http://localhost:8501")
await page.locator("select").select_option(label="Simple Agent")
await page.locator("textarea").fill("Hello, how are you?")
await page.locator("button").click()
```

### **Response Validation**
```python
# Check for actual UI responses
chat_messages = page.locator("div[data-testid='stChatMessage']")
response_text = await last_message.inner_text()
success = len(response_text.strip()) > 20
```

### **Realistic Conversations**
Each agent is tested with multi-turn conversations:

```python
# Example: Custom Tool Agent conversation
[
    "Hello! I'm interested in your custom capabilities.",
    "Can you analyze this text: 'AI is revolutionizing technology'?",
    "Generate a secure hash for the password 'mySecurePass123'",
    "What other custom tools do you have available?",
    "This is exactly what I needed for my project!"
]
```

## 📊 Test Results and Metrics

### **Success Criteria**
- **Response Quality**: Substantial responses (>20 characters)
- **Conversation Flow**: Multi-turn dialogue success
- **UI Interaction**: Proper form submission and response display
- **Agent Selection**: Correct agent switching in UI

### **Performance Metrics**
- **Success Rate**: Percentage of successful interactions
- **Response Time**: Time to receive agent responses
- **UI Responsiveness**: Browser interaction timing
- **Conversation Completion**: Full dialogue success

### **Grading Scale**
- **✅ PASS (70%+)**: Agent working well through UI
- **⚠️ PARTIAL (40-69%)**: Some issues, needs attention
- **❌ FAIL (<40%)**: Significant problems, requires fixes

## 🛠️ Troubleshooting

### **Common Issues**

**Playwright Not Installed:**
```bash
pip install playwright
playwright install chromium
```

**Streamlit Connection Issues:**
```bash
# Check if Streamlit is running
curl http://localhost:8501/healthz

# Manual Streamlit start
cd ui && streamlit run streamlit_ui.py --port 8501
```

**Browser Launch Failures:**
```bash
# Install system dependencies (Linux)
playwright install-deps

# Use different browser
# Edit test files to use firefox or webkit instead of chromium
```

### **Debug Mode**
```python
# Run with visible browser for debugging
browser = await p.chromium.launch(headless=False, slow_mo=1000)
```

## 🎯 Test Scenarios

### **Basic Agent Scenarios**
- **Simple Agent**: Greeting, capability inquiry, self-description
- **Agent with Tools**: Math calculations, web search, tool listing
- **Custom Tool Agent**: Text analysis, hash generation, tool inquiry

### **Advanced Agent Scenarios**
- **Web Research Agent**: AI research, climate solutions, tech trends
- **File Manager Agent**: Directory listing, project structure, file operations
- **Multi Agent System**: Task coordination, agent collaboration, system inquiry

### **User Persona Testing**
- **Developer**: Technical questions, tool-focused interactions
- **Researcher**: Information gathering, analysis requests
- **Business User**: Productivity-focused, practical applications
- **Student**: Learning-oriented, explanation requests

## 📈 Best Practices

### **Running Tests**
1. **Start with Setup Check**: `python tests/run_playwright_tests.py --check`
2. **Test Individual Agents**: Use `--agent` flag for focused testing
3. **Run Full Suite**: Use `--all` for comprehensive testing
4. **Monitor Results**: Check JSON reports for detailed analysis

### **Interpreting Results**
1. **Focus on Success Rates**: Aim for >70% success rate
2. **Check Conversation Flow**: Ensure multi-turn dialogues work
3. **Monitor UI Responsiveness**: Watch for timeout issues
4. **Review Error Messages**: Address specific failure points

### **Maintenance**
1. **Update Conversations**: Add new scenarios as agents evolve
2. **Adjust Timeouts**: Tune wait times based on performance
3. **Monitor Browser Compatibility**: Test with different browsers
4. **Update Selectors**: Maintain UI element selectors as Streamlit updates

## 🚀 Example Usage

### **Test All Agents**
```bash
python tests/test_individual_agents.py --all
```

### **Test Specific Agent**
```bash
python tests/test_individual_agents.py --agent "Web Research Agent"
```

### **List Available Agents**
```bash
python tests/test_individual_agents.py --list
```

### **Run Comprehensive Tests**
```bash
python tests/test_streamlit_ui.py
```

## 🎉 Benefits of Playwright Testing

### **Realistic Testing**
- **Actual Browser**: Tests real user interactions
- **UI Validation**: Ensures interface works correctly
- **End-to-End**: Complete user journey testing

### **Comprehensive Coverage**
- **All Agents**: Tests every agent through UI
- **Multiple Scenarios**: Various conversation patterns
- **User Personas**: Different user types and needs

### **Reliable Results**
- **Browser Automation**: Consistent, repeatable tests
- **Visual Validation**: Actual UI element interaction
- **Real Performance**: Measures actual response times

---

## 🎭 Getting Started with Playwright Testing

Ready to test your Strands SDK agents with realistic browser automation?

```bash
# 1. Install Playwright
pip install -r tests/requirements_playwright.txt
playwright install chromium

# 2. Test all agents
python tests/test_individual_agents.py --all

# 3. Review results
cat tests/all_agents_playwright_results.json
```

**Happy Testing with Playwright! 🎭✨**
