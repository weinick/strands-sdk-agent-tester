# 🤖 Strands SDK Agent Tester

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

A comprehensive sample project demonstrating how to build AI agents using the Strands Agents SDK from Amazon. Features an interactive Streamlit web interface for testing and interacting with 6 different AI agents.

## ✨ Features

- **🎯 6 AI Agents**: 3 basic + 3 advanced agents with different capabilities
- **🖥️ Interactive UI**: Beautiful Streamlit web interface for easy testing
- **🔧 Multi-Model Support**: Works with AWS Bedrock, OpenAI, and Anthropic
- **🛠️ Built-in Tools**: Pre-built tools for calculations, web search, file operations
- **🎨 Custom Tools**: Easy creation of custom tools using Python decorators
- **🤝 Multi-Agent Systems**: Support for complex agent interactions
- **📊 Live Monitoring**: Real-time agent status and session statistics
- **💾 Export Capability**: Download chat logs for analysis
- **🧪 Comprehensive Testing**: Full test suite for all agents

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- AWS account with Bedrock access (for default model provider)
- AWS CLI configured with appropriate credentials

### Installation

1. **Clone this repository:**
```bash
git clone https://github.com/weinick/strands-sdk-agent-tester.git
cd strands-sdk-agent-tester
```

2. **Create and activate a Python virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Configure AWS credentials (for Bedrock):**
```bash
aws configure
```

6. **Enable Claude model access in AWS Bedrock console** (Claude 3.7 Sonnet recommended)

### Running the Application

#### Using the Streamlit UI (Recommended)
```bash
# Launch the interactive web interface
python start_ui.py
```

The UI will open in your browser at `http://localhost:8501` and provides:
- Interactive chat interface for all agents
- Real-time configuration switching
- Session monitoring and chat export
- User-friendly testing environment

## Project Structure

```
StrandsSDK/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── start_ui.py                 # Simple UI launcher
├── basic_agent/                # Basic agent examples
│   ├── simple_agent.py         # Minimal agent example
│   ├── agent_with_tools.py     # Agent with built-in tools
│   └── custom_tool_agent.py    # Agent with custom tools
├── advanced_agent/             # Advanced agent examples
│   ├── web_research_agent.py   # Web research agent
│   ├── file_manager_agent.py   # File management agent
│   └── multi_agent_system.py   # Multi-agent collaboration
├── ui/                         # Streamlit UI components
│   ├── README.md               # UI documentation
│   ├── streamlit_ui.py         # Main UI interface
│   ├── agent_runner.py         # Agent execution handler
│   ├── run_ui.py               # UI startup script
│   ├── launch_ui.py            # Alternative launcher
│   └── requirements_ui.txt     # UI-specific dependencies
├── tests/                      # Test files
│   ├── test_agents.py          # Agent functionality tests
│   ├── test_basic_agents.py    # Tests for basic agents
│   └── test_advanced_agents.py # Tests for advanced agents
└── docs/                       # Documentation
    ├── setup.md                # Setup instructions
    ├── examples.md             # Usage examples
    └── deployment.md           # Deployment guide
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- AWS account with Bedrock access (for default model provider)
- AWS CLI configured with appropriate credentials

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd StrandsSDK
```

2. Create and activate a Python virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Configure AWS credentials (for Bedrock):
```bash
aws configure
```

5. Enable Claude model access in AWS Bedrock console (Claude 3.7 Sonnet recommended)

### Running Examples

#### Using the Streamlit UI (Recommended)
```bash
# Launch the interactive web interface
python start_ui.py
```

The UI will open in your browser at `http://localhost:8501` and provides:
- Interactive chat interface for all agents
- Real-time configuration switching
- Session monitoring and chat export
- User-friendly testing environment

#### Command Line Examples

#### Basic Agents
```bash
# Simple conversational agent
python basic_agent/simple_agent.py

# Agent with built-in tools (calculator, web search, etc.)
python basic_agent/agent_with_tools.py

# Agent with custom tools and functions
python basic_agent/custom_tool_agent.py
```

#### Advanced Agents
```bash
# Web research and information gathering
python advanced_agent/web_research_agent.py

# File operations and management
python advanced_agent/file_manager_agent.py

# Multi-agent collaborative system
python advanced_agent/multi_agent_system.py
```

#### Testing Agents
```bash
# Comprehensive UI testing (all agents through Streamlit interface)
python tests/run_all_ui_tests.py

# Quick functionality test
python tests/run_all_ui_tests.py --quick

# Test specific agent types
python tests/test_ui_basic_agents.py      # Simple, Tools, Custom Tool agents
python tests/test_ui_advanced_agents.py   # Research, File Manager, Multi-Agent
python tests/test_user_scenarios.py       # Realistic user interactions
python tests/test_ui_performance.py       # Performance and load testing

# Traditional agent tests (direct testing)
python tests/test_agents.py

# Run specific test suites
python -m pytest tests/test_basic_agents.py
python -m pytest tests/test_advanced_agents.py
```

## 🧪 Comprehensive Testing

This project includes an extensive testing suite that simulates real user interactions through the Streamlit UI:

### **Test Categories**
- **🤖 Basic Agent Tests** - Core functionality testing
- **🔬 Advanced Agent Tests** - Complex feature validation  
- **👤 User Scenario Tests** - Realistic user interaction simulation
- **⚡ Performance Tests** - Response time and load testing
- **🎯 Comprehensive Tests** - Full end-to-end validation

### **Quick Testing**
```bash
# Run all tests with comprehensive reporting
python tests/run_all_ui_tests.py

# Quick test for development
python tests/run_all_ui_tests.py --quick

# Check test environment
python tests/run_all_ui_tests.py --check
```

### **Test Results**
All tests generate detailed reports including:
- Success rates and performance metrics
- User experience simulation results
- Response time analysis and load testing
- Comprehensive HTML and JSON reports

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Documentation

- [Setup Guide](docs/setup.md) - Detailed setup instructions
- [Examples Guide](docs/examples.md) - Comprehensive usage examples
- [Deployment Guide](docs/deployment.md) - Production deployment patterns

## Resources

- [Official Strands Agents Documentation](https://strandsagents.com/)
- [Strands Agents GitHub](https://github.com/strands-agents)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Support

For questions and support:
- Check the [official documentation](https://strandsagents.com/)
- Open an issue in this repository
- Join the Strands Agents community discussions
