# 🤖 Strands SDK Agent Tester UI

A beautiful, interactive Streamlit web interface for testing and interacting with your Strands SDK agents.

## ✨ Features

- **🎯 Multi-Agent Support**: Test different types of agents from a single interface
- **💬 Interactive Chat**: Real-time conversation with your agents
- **⚙️ Flexible Configuration**: Switch between different AI models and providers
- **📊 Live Monitoring**: Track agent status and session statistics
- **💾 Export Capability**: Download chat logs for analysis
- **🎨 Clean Interface**: User-friendly design optimized for testing

## 🚀 Quick Start

### Option 1: From Root Directory (Recommended)
```bash
# Make sure you're in the StrandsSDK directory
cd StrandsSDK

# Run the simple launcher
python start_ui.py
```

### Option 2: From UI Directory
```bash
# Navigate to the ui directory
cd ui
python run_ui.py
```

### Option 3: Alternative UI Launcher
```bash
# From the ui directory
python launch_ui.py
```

### Option 2: Manual Launch
```bash
# Install UI dependencies
pip install -r requirements_ui.txt

# Launch Streamlit
streamlit run streamlit_ui.py
```

The UI will automatically open in your default web browser at `http://localhost:8501`

## 🎮 How to Use

### 1. Select an Agent
Choose from the available agents in the sidebar:
- **Simple Agent**: Basic conversational agent
- **Agent with Tools**: Enhanced agent with built-in tools
- **Custom Tool Agent**: Agent with specialized custom tools
- **Web Research Agent**: Specialized for web research
- **File Manager Agent**: File operations and management

### 2. Configure Settings
Set up your preferred configuration:
- **Model Provider**: AWS Bedrock, OpenAI, or Anthropic
- **Model Selection**: Choose specific models for each provider
- **Temperature**: Control response creativity (0.0 - 1.0)
- **Max Tokens**: Set response length limits

### 3. Start Chatting
- Type your message in the chat input at the bottom
- Press Enter or click Send
- Watch your agent respond in real-time
- Continue the conversation naturally

### 4. Monitor and Export
- View agent status and session statistics in the right panel
- Clear chat history when needed
- Export conversation logs for analysis

## 🛠️ Agent Types Explained

### Simple Agent
- Basic conversational capabilities
- Good for testing fundamental chat functionality
- Minimal resource requirements

### Agent with Tools
- Enhanced with built-in tools:
  - 🧮 Calculator for math operations
  - 🔍 Web search for current information
  - 🌤️ Weather data access
  - 📁 File operations

### Custom Tool Agent
- Specialized tools for specific tasks
- Domain-specific analyzers
- Custom data processors
- Workflow automators

### Web Research Agent
- Multi-source web searching
- Real-time information gathering
- Source credibility assessment
- Comprehensive research summaries

### File Manager Agent
- Directory and file management
- Search and filter capabilities
- File analysis and organization
- Backup and cleanup operations

## ⚙️ Configuration Options

### Model Providers

#### AWS Bedrock
- **Models**: Claude 3.5 Sonnet v2, Claude 3 Sonnet, Claude 3 Haiku, Claude v2.1
- **Requirements**: AWS credentials configured
- **Setup**: `aws configure` or environment variables

#### OpenAI
- **Models**: GPT-4, GPT-3.5-turbo, etc.
- **Requirements**: OpenAI API key
- **Setup**: Enter API key in the sidebar

#### Anthropic
- **Models**: Claude 3 models
- **Requirements**: Anthropic API key
- **Setup**: Enter API key in the sidebar

### Parameters
- **Temperature**: Controls randomness (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Maximum response length (100-4000)

## 📁 File Structure

```
StrandsSDK/
├── start_ui.py              # Simple UI launcher (from root)
├── basic_agent/             # Basic agent implementations
├── advanced_agent/          # Advanced agent implementations
├── tests/                   # Test files
│   ├── test_agents.py       # Agent functionality tests
│   ├── test_basic_agents.py # Basic agent tests
│   └── test_advanced_agents.py # Advanced agent tests
└── ui/                      # UI Components (this directory)
    ├── README.md            # This file
    ├── streamlit_ui.py      # Main Streamlit application
    ├── agent_runner.py      # Agent execution logic
    ├── run_ui.py            # UI startup script
    ├── launch_ui.py         # Alternative launcher
    └── requirements_ui.txt  # UI-specific dependencies
```

## 🔧 Troubleshooting

### Common Issues

#### "Streamlit not found"
```bash
pip install streamlit
# or
pip install -r requirements_ui.txt
```

#### "Agent file not found"
- Ensure you're running from the StrandsSDK directory
- Check that agent files exist in their expected locations

#### "API key errors"
- Verify your API keys are correctly entered
- Check that your AWS credentials are configured
- Ensure you have the necessary permissions

#### "Import errors"
- Install main project dependencies: `pip install -r requirements.txt`
- Install UI dependencies: `pip install -r requirements_ui.txt`

### Debug Mode
To run with debug information:
```bash
streamlit run streamlit_ui.py --logger.level=debug
```

## 🎨 Customization

### Adding New Agents
1. Create your agent class in the appropriate directory
2. Add agent configuration to `AGENTS` dictionary in `streamlit_ui.py`
3. Implement agent logic in `agent_runner.py`

### Styling
- Modify CSS in the `st.markdown()` sections
- Customize colors, fonts, and layout
- Add new UI components as needed

### Features
- Add new model providers
- Implement additional monitoring metrics
- Create custom export formats

## 📊 Session Statistics

The UI tracks:
- Total messages exchanged
- User vs agent message counts
- Session duration
- Agent response times (future feature)

## 💡 Tips for Best Results

1. **Start Simple**: Begin with the Simple Agent to test basic functionality
2. **Experiment with Temperature**: Lower values for focused responses, higher for creativity
3. **Use Appropriate Agents**: Match the agent type to your use case
4. **Monitor Resources**: Some agents may require more computational resources
5. **Export Important Conversations**: Save valuable interactions for future reference

## 🤝 Contributing

To contribute to the UI:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

## 📝 License

This UI is part of the Strands SDK Sample Project and follows the same Apache License 2.0.

## 🆘 Support

For help with the UI:
- Check this README for common solutions
- Review the main project documentation
- Open an issue in the repository
- Join the Strands Agents community discussions

---

**Happy Testing! 🚀**
