"""
Agent Runner Module for Streamlit UI
Handles loading and executing different Strands SDK agents
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional
import traceback

# Add parent directory to path for agent imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import actual agent implementations
try:
    from basic_agent.simple_agent import create_simple_agent
    from basic_agent.agent_with_tools import create_agent_with_tools
    from basic_agent.custom_tool_agent import create_custom_tool_agent
    from advanced_agent.web_research_agent import create_web_research_agent
    from advanced_agent.file_manager_agent import create_file_manager_agent
    from advanced_agent.multi_agent_system import create_multi_agent_system
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import agent implementations: {e}")
    AGENTS_AVAILABLE = False

class AgentRunner:
    """Handles loading and running different Strands SDK agents"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.loaded_agents = {}
        
    def run_agent(self, agent_type: str, model_config: Dict[str, Any], user_input: str = "") -> str:
        """Run the specified agent with given configuration"""
        try:
            if not AGENTS_AVAILABLE:
                return self._fallback_response(agent_type, model_config, user_input)
            
            # Get or create agent instance
            agent_key = f"{agent_type}_{id(model_config)}"
            
            if agent_key not in self.loaded_agents:
                agent = self._create_agent(agent_type, model_config)
                if agent:
                    self.loaded_agents[agent_key] = agent
                else:
                    return f"❌ Failed to create {agent_type}"
            
            agent = self.loaded_agents[agent_key]
            
            # Use the agent's chat method
            if hasattr(agent, 'chat') and user_input:
                return agent.chat(user_input)
            else:
                # Return agent status or welcome message
                if hasattr(agent, 'get_status'):
                    status = agent.get_status()
                    return f"""**{agent_type} Ready**

Agent initialized and ready to assist!

**Configuration:**
• Provider: {model_config.get('provider', 'Unknown')}
• Model: {model_config.get('model', 'Unknown')}
• Temperature: {model_config.get('temperature', 0.7)}

**Status:** {status.get('status', 'Ready')}

Start chatting to interact with this agent!"""
                else:
                    return f"**{agent_type}** is ready! Start chatting to interact."
                
        except Exception as e:
            error_trace = traceback.format_exc()
            return f"""**Error Running {agent_type}:**

Error: {str(e)}

**Debug Information:**
```
{error_trace}
```

**Troubleshooting Tips:**
1. Check if all required dependencies are installed
2. Verify your API keys are correctly configured
3. Ensure the agent files exist in the expected locations
4. Check your internet connection for web-based agents
"""
    
    def _create_agent(self, agent_type: str, model_config: Dict[str, Any]):
        """Create an agent instance based on type"""
        try:
            if agent_type == "Simple Agent":
                return create_simple_agent(model_config)
            elif agent_type == "Agent with Tools":
                return create_agent_with_tools(model_config)
            elif agent_type == "Custom Tool Agent":
                return create_custom_tool_agent(model_config)
            elif agent_type == "Web Research Agent":
                return create_web_research_agent(model_config)
            elif agent_type == "File Manager Agent":
                return create_file_manager_agent(model_config)
            elif agent_type == "Multi Agent System":
                return create_multi_agent_system(model_config)
            else:
                return None
        except Exception as e:
            print(f"Error creating {agent_type}: {str(e)}")
            return None
    
    def _fallback_response(self, agent_type: str, model_config: Dict[str, Any], user_input: str) -> str:
        """Fallback response when agents are not available"""
        # Static fallback responses for each agent type
        if agent_type == "Simple Agent":
            return self._simple_agent_fallback(model_config, user_input)
        elif agent_type == "Agent with Tools":
            return self._tools_agent_fallback(model_config, user_input)
        elif agent_type == "Custom Tool Agent":
            return self._custom_tools_fallback(model_config, user_input)
        elif agent_type == "Web Research Agent":
            return self._research_agent_fallback(model_config, user_input)
        elif agent_type == "File Manager Agent":
            return self._file_manager_fallback(model_config, user_input)
        elif agent_type == "Multi Agent System":
            return self._multi_agent_fallback(model_config, user_input)
        else:
            return f"Unknown agent type: {agent_type}"
    
    def _simple_agent_fallback(self, model_config: Dict[str, Any], user_input: str) -> str:
        """Fallback for Simple Agent"""
        if user_input:
            return f"""**Simple Agent Response:**

Hello! I received your message: "{user_input}"

I'm a basic conversational agent powered by {model_config.get('provider', 'Unknown')} using the {model_config.get('model', 'default')} model.

I can help you with general questions and conversations. What would you like to talk about?

*Note: This is a fallback response. Install agent dependencies for full functionality.*

*Configuration:*
- Provider: {model_config.get('provider')}
- Model: {model_config.get('model')}
- Temperature: {model_config.get('temperature', 0.7)}"""
        else:
            return f"""**Simple Agent Ready**

I'm a basic conversational agent ready to chat!

*Configuration:*
- Provider: {model_config.get('provider')}
- Model: {model_config.get('model')}
- Temperature: {model_config.get('temperature', 0.7)}"""
    
    def _tools_agent_fallback(self, model_config: Dict[str, Any], user_input: str) -> str:
        """Fallback for Agent with Tools"""
        if user_input:
            tools_mentioned = []
            user_lower = user_input.lower()
            
            if any(word in user_lower for word in ['calculate', 'math', 'compute']):
                tools_mentioned.append("🧮 Calculator")
            if any(word in user_lower for word in ['search', 'find', 'lookup']):
                tools_mentioned.append("🔍 Web Search")
            if any(word in user_lower for word in ['weather', 'temperature']):
                tools_mentioned.append("🌤️ Weather")
            
            response = f"""**Agent with Tools Response:**

I received your query: "{user_input}"

"""
            if tools_mentioned:
                response += f"I would use these tools: {', '.join(tools_mentioned)}\n\n"
            
            response += f"""I have access to various tools including:
• 🧮 Calculator for mathematical operations
• 🔍 Web search for current information  
• 🌤️ Weather data for location queries
• 📁 File operations for document handling

*Note: This is a demonstration response. Install full agent for actual tool usage.*

*Configuration:*
- Provider: {model_config.get('provider')}
- Model: {model_config.get('model')}
- Temperature: {model_config.get('temperature', 0.7)}"""
            
            return response
        else:
            return "**Agent with Tools Ready** - I have access to Calculator, Web Search, Weather, and File tools!"
    
    def _custom_tools_fallback(self, model_config: Dict[str, Any], user_input: str) -> str:
        """Fallback for Custom Tool Agent"""
        return f"""**Custom Tool Agent Response:**

Query: "{user_input}"

I'm equipped with specialized custom tools:
📊 **Text Analyzer** - Analyze text metrics and extract keywords
📈 **Data Processor** - Process CSV data and generate statistics
💻 **Code Analyzer** - Analyze code structure and complexity  
🔐 **Hash Generator** - Generate security hashes

*This is a demonstration. Install full agent for actual custom tool functionality.*

*Configuration:*
- Provider: {model_config.get('provider')}
- Model: {model_config.get('model')}
- Temperature: {model_config.get('temperature', 0.7)}"""
    
    def _research_agent_fallback(self, model_config: Dict[str, Any], user_input: str) -> str:
        """Fallback for Web Research Agent"""
        return f"""**Web Research Agent Response:**

Research Query: "{user_input}"

I specialize in comprehensive web research including:
🔍 **Multi-source Search** - Aggregate information from various sources
📊 **Content Analysis** - Analyze and synthesize findings
📈 **Trend Analysis** - Identify patterns and developments
⚖️ **Comparative Research** - Compare different topics or solutions

*This is a demonstration. Install full agent for actual web research capabilities.*

*Configuration:*
- Provider: {model_config.get('provider')}
- Model: {model_config.get('model')}
- Temperature: {model_config.get('temperature', 0.3)}"""
    
    def _file_manager_fallback(self, model_config: Dict[str, Any], user_input: str) -> str:
        """Fallback for File Manager Agent"""
        return f"""**File Manager Agent Response:**

File Operation Request: "{user_input}"

I can help with file operations including:
📁 **Directory Listing** - Show files and folders
📄 **File Reading** - Display file contents
ℹ️ **File Information** - Show file details and metadata
🔍 **File Search** - Find files by name or content

*This is a demonstration. Install full agent for actual file operations.*

*Current Directory:* {os.getcwd()}
*Configuration:*
- Provider: {model_config.get('provider')}
- Model: {model_config.get('model')}
- Temperature: {model_config.get('temperature', 0.5)}"""

    def _multi_agent_fallback(self, model_config: Dict[str, Any], user_input: str) -> str:
        """Fallback for Multi Agent System"""
        return f"""**Multi Agent System Response:**

Task Request: "{user_input}"

I coordinate multiple specialized agents working together:
🤖 **Research Agent** - Gathers information from web sources
📊 **Analysis Agent** - Processes and analyzes data
📝 **Writing Agent** - Creates structured reports and summaries
🔧 **Tool Agent** - Handles calculations and technical tasks

*This is a demonstration. Install full agent system for collaborative AI workflows.*

*Simulated Agent Coordination:*
1. Task received and analyzed
2. Appropriate agents would be selected
3. Agents collaborate to complete the task
4. Results are synthesized and presented

*Configuration:*
- Provider: {model_config.get('provider')}
- Model: {model_config.get('model')}
- Temperature: {model_config.get('temperature', 0.7)}"""

def get_model_config(provider: str, model: str, temperature: float, max_tokens: int, **kwargs) -> Dict[str, Any]:
    """Create model configuration dictionary"""
    config = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # Add provider-specific configurations
    if provider == "OpenAI" and "api_key" in kwargs:
        config["api_key"] = kwargs["api_key"]
    elif provider == "Anthropic" and "api_key" in kwargs:
        config["api_key"] = kwargs["api_key"]
    
    return config
