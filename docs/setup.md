# Setup Guide - Strands Agents SDK Sample Project

This guide will help you set up and run the Strands Agents SDK sample project.

## Prerequisites

### System Requirements
- **Python 3.10 or higher**
- **AWS Account** (for default Bedrock model provider)
- **Git** (for cloning and version control)

### AWS Setup (Required for Default Configuration)

1. **AWS Account**: Ensure you have an AWS account with appropriate permissions.

2. **AWS CLI Configuration**: Install and configure the AWS CLI:
   ```bash
   # Install AWS CLI (if not already installed)
   pip install awscli
   
   # Configure AWS credentials
   aws configure
   ```
   
   You'll need to provide:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (recommend: `us-west-2`)
   - Default output format (recommend: `json`)

3. **Enable Claude Model Access**: 
   - Go to the AWS Bedrock console
   - Navigate to "Model access" in the left sidebar
   - Request access to **Claude 3.7 Sonnet** model
   - Wait for approval (usually takes a few minutes)

## Installation

### 1. Clone or Download the Project
```bash
# If using git
git clone <your-repository-url>
cd StrandsSDK

# Or download and extract the project files
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# Optional: Install additional packages for web scraping
pip install beautifulsoup4 requests

# Optional: Install development dependencies
pip install pytest pytest-asyncio
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# At minimum, set:
# AWS_REGION=us-west-2
# AWS_PROFILE=default (or your AWS profile name)
```

## Verification

### Test AWS Configuration
```bash
# Test AWS credentials
aws sts get-caller-identity

# Test Bedrock access
aws bedrock list-foundation-models --region us-west-2
```

### Test Basic Installation
```bash
# Run simple agent example
python basic_agent/simple_agent.py
```

If successful, you should see the agent respond to basic questions.

## Alternative Model Providers

If you prefer not to use AWS Bedrock, you can configure alternative providers:

### Anthropic
```bash
# Install Anthropic SDK
pip install anthropic

# Set API key in .env
ANTHROPIC_API_KEY=your_api_key_here
```

### OpenAI
```bash
# Install OpenAI SDK
pip install openai

# Set API key in .env
OPENAI_API_KEY=your_api_key_here
```

### Ollama (Local Models)
```bash
# Install Ollama locally
# Visit: https://ollama.ai/

# Pull a model
ollama pull llama3

# Set host in .env
OLLAMA_HOST=http://localhost:11434
```

## Project Structure

```
StrandsSDK/
├── README.md                    # Project overview
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── basic_agent/                # Basic agent examples
│   ├── simple_agent.py         # Minimal agent example
│   ├── agent_with_tools.py     # Agent with built-in tools
│   └── custom_tool_agent.py    # Agent with custom tools
├── advanced_agent/             # Advanced agent examples
│   ├── web_research_agent.py   # Web research capabilities
│   ├── file_manager_agent.py   # File management operations
│   └── multi_agent_system.py   # Multi-agent collaboration
├── tests/                      # Test files
│   ├── test_basic_agents.py    # Tests for basic agents
│   └── test_advanced_agents.py # Tests for advanced agents
└── docs/                       # Documentation
    ├── setup.md                # This setup guide
    ├── examples.md             # Usage examples
    └── deployment.md           # Deployment guide
```

## Running Examples

### Basic Examples
```bash
# Simple agent (minimal setup)
python basic_agent/simple_agent.py

# Agent with built-in tools
python basic_agent/agent_with_tools.py

# Agent with custom tools
python basic_agent/custom_tool_agent.py
```

### Advanced Examples
```bash
# Web research agent
python advanced_agent/web_research_agent.py

# File manager agent
python advanced_agent/file_manager_agent.py

# Multi-agent system
python advanced_agent/multi_agent_system.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_basic_agents.py -v

# Run with coverage
pytest --cov=. tests/
```

## Troubleshooting

### Common Issues

1. **AWS Credentials Not Found**
   ```
   Error: Unable to locate credentials
   ```
   **Solution**: Run `aws configure` or set environment variables

2. **Model Access Denied**
   ```
   Error: Access denied to model
   ```
   **Solution**: Enable Claude model access in AWS Bedrock console

3. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'strands'
   ```
   **Solution**: Ensure virtual environment is activated and dependencies installed

4. **Permission Errors**
   ```
   PermissionError: [Errno 13] Permission denied
   ```
   **Solution**: Check file permissions and virtual environment activation

### Getting Help

1. **Check Logs**: Most examples include detailed logging
2. **AWS Documentation**: [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
3. **Strands Documentation**: [Official Strands Agents Documentation](https://strandsagents.com/)
4. **GitHub Issues**: Check the project's GitHub issues for common problems

## Next Steps

Once setup is complete:

1. **Explore Examples**: Start with `basic_agent/simple_agent.py`
2. **Read Documentation**: Check `docs/examples.md` for detailed usage
3. **Customize Tools**: Modify or create new tools for your use case
4. **Deploy**: See `docs/deployment.md` for production deployment options

## Security Considerations

- **API Keys**: Never commit API keys to version control
- **AWS Permissions**: Use least-privilege IAM policies
- **File Operations**: File manager examples are restricted to safe directories
- **Web Scraping**: Be respectful of robots.txt and rate limits
- **Input Validation**: Always validate user inputs in production

## Performance Tips

- **Model Selection**: Choose appropriate models for your use case
- **Parallel Tools**: Configure `max_parallel_tools` for better performance
- **Context Management**: Use conversation managers to control memory usage
- **Caching**: Consider caching frequently used results
- **Monitoring**: Use built-in metrics and observability features
