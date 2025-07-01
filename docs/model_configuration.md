# Model Configuration Guide

## 🤖 Available Claude Models

### **Claude 3.7 Sonnet (Latest & Recommended)**
- **Model ID**: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`
- **Release**: February 2025 - Anthropic's most intelligent model
- **Type**: Hybrid reasoning model (first of its kind)
- **Best for**: All tasks, especially complex reasoning, coding, analysis
- **Performance**: Highest capability, advanced reasoning
- **Use cases**: Default for all agents, production workloads

### **Claude 3.5 Sonnet v2**
- **Model ID**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Best for**: General purpose, balanced performance
- **Performance**: High capability, good speed
- **Use cases**: Alternative to Claude 3.7

### **Claude 3 Sonnet**
- **Model ID**: `anthropic.claude-3-sonnet-20240229-v1:0`
- **Best for**: Complex analysis, research tasks
- **Performance**: High capability, moderate speed
- **Use cases**: Research and analytical tasks

### **Claude 3 Haiku**
- **Model ID**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Best for**: Fast responses, simple tasks
- **Performance**: Good capability, fastest speed
- **Use cases**: Quick interactions, cost-effective operations

### **Claude v2.1 (Legacy)**
- **Model ID**: `anthropic.claude-v2:1`
- **Best for**: Compatibility with older implementations
- **Performance**: Good capability, legacy support
- **Use cases**: Fallback option

## 🎯 Agent-Specific Model Configurations

### **Default Model Assignments:**

| Agent Type | Default Model | Temperature | Max Tokens | Reasoning |
|------------|---------------|-------------|------------|-----------|
| Simple Agent | Claude 3.7 Sonnet | 0.7 | 1000 | Best overall performance |
| Agent with Tools | Claude 3.7 Sonnet | 0.7 | 1000 | Advanced tool integration |
| Custom Tool Agent | Claude 3.7 Sonnet | 0.7 | 1000 | Complex reasoning for tools |
| Web Research Agent | Claude 3.7 Sonnet | 0.3 | 1500 | Hybrid reasoning for research |
| File Manager Agent | Claude 3.7 Sonnet | 0.5 | 1200 | Balanced file operations |

### **Temperature Settings:**
- **0.1-0.3**: Focused, deterministic responses (research, analysis)
- **0.4-0.6**: Balanced creativity and consistency (file operations)
- **0.7-0.9**: Creative, varied responses (general conversation)

### **Token Limits:**
- **1000**: Standard conversations
- **1200**: File operations with content display
- **1500**: Research with detailed analysis
- **2000+**: Complex multi-step operations

## 🔧 Configuration in Streamlit UI

### **Model Selection:**
1. Open the Streamlit UI
2. Use the sidebar "Model Provider" dropdown
3. Select "AWS Bedrock"
4. Choose your preferred Claude model
5. Adjust temperature and max tokens as needed

### **Available Options:**
- **Claude 3.5 Sonnet v2** (Default, Recommended)
- **Claude 3 Sonnet** (High capability)
- **Claude 3 Haiku** (Fast, cost-effective)
- **Claude v2.1** (Legacy compatibility)

## 🚀 AWS Bedrock Setup

### **Enable Models in AWS Console:**
1. Go to AWS Bedrock Console
2. Navigate to "Model access"
3. Request access for Claude models:
   - ✅ **Claude 3.5 Sonnet v2** (Recommended)
   - ✅ **Claude 3 Sonnet**
   - ✅ **Claude 3 Haiku**
   - ✅ **Claude v2.1**

### **Required Permissions:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-v2:1"
            ]
        }
    ]
}
```

## 💡 Best Practices

### **Model Selection Guidelines:**
- **Development/Testing**: Claude 3 Haiku (fast, cost-effective)
- **Production**: Claude 3.5 Sonnet v2 (best performance)
- **Research Tasks**: Claude 3.5 Sonnet v2 with low temperature
- **Creative Tasks**: Claude 3.5 Sonnet v2 with higher temperature

### **Performance Optimization:**
- Use appropriate token limits to avoid unnecessary costs
- Adjust temperature based on task requirements
- Monitor usage and costs in AWS console
- Consider caching for repeated queries

### **Error Handling:**
- All agents include fallback responses when models are unavailable
- Graceful degradation to mock responses for testing
- Clear error messages for configuration issues

## 🔍 Troubleshooting

### **Common Issues:**
1. **Model not available**: Check AWS Bedrock model access
2. **Permission denied**: Verify IAM permissions
3. **Rate limiting**: Implement retry logic with exponential backoff
4. **High costs**: Monitor usage and optimize token limits

### **Testing Model Access:**
```bash
# Test model availability
python test_agents.py

# Test specific agent
python basic_agent/simple_agent.py
```

## 📊 Model Comparison

| Feature | Claude 3.7 Sonnet | Claude 3.5 Sonnet v2 | Claude 3 Sonnet | Claude 3 Haiku | Claude v2.1 |
|---------|-------------------|----------------------|-----------------|----------------|-------------|
| Capability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Reasoning | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Code Generation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Analysis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Tool Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Hybrid Reasoning | ⭐⭐⭐⭐⭐ | ❌ | ❌ | ❌ | ❌ |

**Recommendation**: Use Claude 3.7 Sonnet as the default for the most advanced AI capabilities, including hybrid reasoning that can switch between fast responses and deep analytical thinking.
