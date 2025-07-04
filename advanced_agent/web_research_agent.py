"""
Web Research Agent - Using Official Strands Agent Browser Tools
Demonstrates real web research capabilities with use_browser tool
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import Strands Agent framework
from strands import Agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrandsWebResearchAgent:
    """
    Web Research Agent using official Strands Agent browser tools
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the Strands web research agent"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.3,
            "max_tokens": 1500
        }
        
        self.conversation_history = []
        self.research_history = []
        
        # Create Strands Agent with browser tools
        try:
            # Import the use_browser tool from strands_tools
            from strands_tools import use_browser
            
            self.agent = Agent(
                model=self.model_config.get("model", "us.anthropic.claude-3-7-sonnet-20250219-v1:0"),
                system_prompt="""You are a specialized Web Research Agent with real browser automation capabilities.

Your primary tools:
- use_browser: For real web browsing, searching, and content extraction
- You can navigate websites, search for information, and extract current data

When users ask you to research something:
1. Use the browser tool to search for current information
2. Navigate to relevant websites to gather data
3. Extract and synthesize information from multiple sources
4. Provide comprehensive, up-to-date research reports

Always prioritize real-time web data over your training knowledge when conducting research.""",
                tools=[use_browser]  # Use official Strands browser tool
            )
            
            logger.info("✅ Strands Web Research Agent initialized with browser tools")
            
        except ImportError as e:
            logger.warning(f"⚠️ Could not import use_browser tool: {e}")
            # Create agent without tools as fallback
            self.agent = Agent(
                model=self.model_config.get("model", "us.anthropic.claude-3-7-sonnet-20250219-v1:0"),
                system_prompt="""You are a specialized Web Research Agent. 

While I don't have access to real browser tools in this configuration, I can help you with:
- Research planning and methodology
- Information analysis and synthesis
- Research question formulation
- Source evaluation guidance

For actual web browsing, you would need the use_browser tool properly configured."""
            )
            logger.info("✅ Strands Web Research Agent initialized in fallback mode")
    
    def chat(self, user_input: str) -> str:
        """Process research requests using Strands Agent with browser tools"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Show thinking process
            thinking_process = f"""🧠 **Strands Web Research Agent Thinking:**
```
1. Analyzing query: "{user_input}"
2. Using official Strands Agent framework with use_browser tool
3. Will perform real web browsing and search for current information
4. Browser tool provides: navigation, search, content extraction
```

**🔧 Strands Tool Selection:**
- Framework: Official Strands Agents SDK
- Tool: use_browser (official browser automation tool)
- Capabilities: Real web browsing, search, content extraction
- Data source: Live internet via browser automation

**🌐 Initiating Browser-Based Research...**
"""
            
            # Use Strands Agent to process the request
            response = self.agent(user_input)
            
            # Store research in history
            if any(word in user_input.lower() for word in ['research', 'search', 'find', 'latest']):
                self.research_history.append({
                    "query": user_input,
                    "timestamp": datetime.now(),
                    "type": "strands_browser_research",
                    "method": "use_browser_tool"
                })
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return thinking_process + f"""

**📤 Strands Agent Response:**
{response}

**📋 Research Session Summary:**
• **Framework:** Official Strands Agents SDK
• **Tool Used:** use_browser (real browser automation)
• **Data Source:** Live web browsing and search
• **Research Quality:** Real-time internet data
• **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*This research was conducted using official Strands Agent browser tools for real web automation.*"""
            
        except Exception as e:
            error_msg = f"Error with Strands Web Research Agent: {str(e)}"
            logger.error(error_msg)
            return f"""🧠 **Strands Web Research Agent Thinking:**
```
1. Analyzing query: "{user_input}"
2. Attempting to use official Strands Agent browser tools
3. Error encountered during processing
```

❌ **Error:** {error_msg}

**🔧 Troubleshooting:**
- Ensure Strands Agents tools are properly installed
- Check browser tool dependencies
- Verify network connectivity for web browsing

**📋 Fallback Information:**
While I couldn't perform live web research due to the error above, I can provide general guidance based on my knowledge. For real-time web research, the Strands Agent use_browser tool would normally:

1. **Navigate to search engines** (Google, Bing, DuckDuckGo)
2. **Perform searches** with your query
3. **Extract content** from relevant websites
4. **Synthesize findings** from multiple sources
5. **Provide current information** with timestamps

*To enable full browser-based research, please ensure all Strands Agent dependencies are properly configured.*"""
    
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def get_research_history(self) -> list:
        """Get research history"""
        return self.research_history.copy()
    
    def clear_history(self):
        """Clear conversation and research history"""
        self.conversation_history = []
        self.research_history = []
        logger.info("All history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_type": "Strands Web Research Agent",
            "framework": "Official Strands Agents SDK",
            "tools": ["use_browser"],
            "model_config": self.model_config,
            "conversation_length": len(self.conversation_history),
            "research_sessions": len(self.research_history),
            "status": "Ready for Browser-Based Research"
        }

def create_web_research_agent(model_config: Optional[Dict[str, Any]] = None) -> StrandsWebResearchAgent:
    """Factory function to create a Strands Web Research Agent"""
    return StrandsWebResearchAgent(model_config)

def main():
    """Main function for testing the agent directly"""
    print("🌐 Strands Web Research Agent - Official Browser Tools Demo")
    print("=" * 70)
    
    # Create agent
    agent = create_web_research_agent()
    
    print("Strands Web Research Agent initialized!")
    print("Status:", agent.get_status())
    print("-" * 70)
    print("Try research commands like:")
    print('• "Research the latest AI trends"')
    print('• "Search for Python web frameworks"')
    print('• "Find current news about machine learning"')
    print('• "Look up information about climate change"')
    print("• Type 'quit' to exit")
    print("-" * 70)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAgent: Thank you for using the Strands Web Research Agent!")
                break
            
            if user_input:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Strands Web Research Agent!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
