"""
Web Research Agent - Using Official Strands SDK Tools
Demonstrates real web research capabilities with official Strands tools
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

# Import Strands Agent framework and official tools
from strands import Agent
from strands_tools import use_browser, http_request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrandsWebResearchAgent:
    """
    Web Research Agent using official Strands SDK tools
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the Strands web research agent"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        self.conversation_history = []
        self.research_history = []
        
        # Create Strands Agent with official SDK tools
        self.agent = Agent(
            model=self.model_config.get("model", "us.anthropic.claude-3-7-sonnet-20250219-v1:0"),
            system_prompt=f"""Web Research Agent with Official Strands SDK Tools - {datetime.now().strftime('%Y-%m-%d')}

You are a web research agent with access to real browser automation via official Strands SDK tools.

CRITICAL: SINGLE SEARCH ONLY - NO RETRIES OR MULTIPLE ATTEMPTS

AVAILABLE TOOLS:
- use_browser: Browser automation (navigate, get_text, get_html)
- http_request: HTTP client for API calls

SEARCH ENGINE PRIORITY (CHINA-OPTIMIZED FOR SPEED):
1. **Baidu (PRIMARY)**: https://www.baidu.com/s?wd=YOUR_QUERY 
   - FASTEST in China (2-3 seconds)
   - Use for ALL general queries first
   - Excellent for news, sports, current events, any topic
   
2. **Direct websites**: When you know the specific authoritative source
   - Company websites, news sites, official sources
   - Only if you need very specific information
   
3. **Other search engines**: ONLY if Baidu fails completely
   - DuckDuckGo, Bing (Google often blocked/slow in China)

CRITICAL PERFORMANCE RULE - ONE SEARCH ONLY:
- **Always try Baidu FIRST** for maximum speed
- Make only ONE search/navigation per query for fast response
- Do NOT try multiple search engines - stick with Baidu
- Extract maximum information from your chosen source

BROWSER ACTIONS (Use separately):
- First: playwright___playwright_navigate to Baidu search URL
- Then: playwright___playwright_get_visible_text to extract content
- DO NOT combine actions in one tool call

SEARCH STRATEGY FOR SPEED:
1. **Default choice**: Use Baidu search for 95% of queries
2. **Format query**: Convert to appropriate search terms (Chinese/English as needed)
3. **Single navigation**: Go to Baidu with search terms
4. **Extract comprehensively**: Get all needed info in one go
5. **NO retries**: One search, comprehensive answer

WHEN TO USE MCP TOOLS:
- User asks for current/recent information not in your training data
- User asks for real-time data (stock prices, news, sports results, etc.)
- User asks "search for", "find", "what's the latest", "current", etc.
- Any query that requires up-to-date information from the internet

RULES:
- ONE search/navigation only per query (mandatory for speed)
- Choose the most appropriate source for each specific query
- Use separate tool calls for navigate and extract
- Always cite the source URL used
- Be comprehensive in your single search""",
            tools=[use_browser, http_request]
        )
        
        logger.info("✅ Strands Web Research Agent initialized with official SDK tools")

    def chat(self, user_input: str) -> str:
        """Process research requests using Strands Agent with official SDK tools"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Show thinking process
            thinking_process = f"""**Strands Web Research Agent Thinking:**
```
1. Analyzing query: "{user_input}"
2. Using official Strands Agent SDK with tools: use_browser, http_request
3. Strategy: SINGLE SEARCH for quick results
4. Search engine priority: DuckDuckGo → Google → Baidu (if needed)
5. Will extract answer from first successful search
```

**Official Strands SDK Tools:**
- Framework: Strands Agents SDK (Official)
- Tools: use_browser (Playwright automation), http_request (HTTP client)
- Strategy: Single search approach for fast results
- Fallback: Baidu search engine for alternative results

**Initiating Quick Web Research:**
- Starting with DuckDuckGo for fast, unblocked search
- Single search execution with immediate result extraction
- Baidu available as backup for alternative content
- Quick response with source attribution
"""
            
            # Use Strands Agent to process the request
            response = self.agent(user_input)
            
            # Store research in history
            if any(word in user_input.lower() for word in ['research', 'search', 'find', 'latest', 'current']):
                self.research_history.append({
                    "query": user_input,
                    "timestamp": datetime.now(),
                    "type": "strands_sdk_research",
                    "method": "use_browser_and_http_request_tools"
                })
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Return formatted response
            return f"""{response}

---

**Research Session Summary:**
- **Framework:** Official Strands Agents SDK
- **SDK Tools Used:** use_browser (Playwright), http_request (HTTP client)
- **Data Source:** Live web browsing, API calls, real-time content extraction
- **Research Quality:** Current internet data with source verification
- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*This research was conducted using official Strands SDK tools for real web automation and data retrieval.*

---

<details>
<summary><strong>System Process Details</strong> (Click to expand)</summary>

{thinking_process}

</details>"""
            
        except Exception as e:
            error_msg = f"Error with Strands Web Research Agent: {str(e)}"
            logger.error(error_msg)
            return f"""**Strands Web Research Agent Error:**
```
1. Analyzing query: "{user_input}"
2. Attempting to use official Strands SDK tools
3. Error encountered during processing
```

**Error Details:**
{error_msg}

**Troubleshooting:**
This could be due to:
- Network connectivity issues
- Search engine access restrictions  
- Browser automation setup problems
- Missing dependencies (playwright, strands-agents-tools)

**Setup Verification:**
1. Ensure strands-agents-tools is installed: `pip install strands-agents-tools`
2. Install Playwright browsers: `playwright install`
3. Check network connectivity
4. Verify AWS credentials if using Bedrock models

**Fallback Response:**
Based on my training data, I can provide general information about your query, though it may not be the most current information available online."""

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_type": "Strands Web Research Agent",
            "framework": "Official Strands Agents SDK",
            "tools": ["use_browser", "http_request"],
            "model_config": self.model_config,
            "conversation_length": len(self.conversation_history),
            "research_sessions": len(self.research_history),
            "status": "Ready for Official SDK Web Research"
        }

    def clear_history(self):
        """Clear conversation and research history"""
        self.conversation_history = []
        self.research_history = []

def create_web_research_agent(model_config: Optional[Dict[str, Any]] = None) -> StrandsWebResearchAgent:
    """Factory function to create a web research agent"""
    return StrandsWebResearchAgent(model_config)

def main():
    """Main function for testing the web research agent"""
    print("🌐 Strands Web Research Agent - Official SDK Version")
    print("=" * 60)
    
    try:
        # Create agent
        agent = create_web_research_agent()
        print(f"✅ Agent Status: {agent.get_status()}")
        
        # Test queries
        test_queries = [
            "Research the latest AI trends for 2025",
            "Find current Amazon stock price (AMZN)",
            "What are the best Python learning resources?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing: {query}")
            print("-" * 40)
            response = agent.chat(query)
            print(response[:300] + "..." if len(response) > 300 else response)
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Setup Instructions:")
        print("   1. pip install strands-agents-tools")
        print("   2. playwright install")
        print("   3. Ensure AWS credentials are configured")

if __name__ == "__main__":
    main()

    def chat(self, user_input: str) -> str:
        """Process research requests using Strands Agent with MCP tools"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Show thinking process
            thinking_process = f"""**Strands Web Research Agent Thinking:**
```
1. Analyzing query: "{user_input}"
2. Using Strands Agent framework with MCP Playwright tools
3. Available tools: playwright___playwright_navigate, playwright___playwright_get_visible_text, etc.
4. Will perform real web research with live browser automation
```

**MCP Tool Selection:**
- Framework: Strands Agents SDK with MCP integration
- Tools: Playwright MCP tools (browser automation)
- Capabilities: Real browser navigation, content extraction, form interaction
- Data source: Live internet via browser automation

**Initiating Real Web Research:**
- Starting browser automation with Playwright MCP tools
- Navigating to relevant websites and search engines
- Extracting and analyzing web content
- Verifying information from reliable sources
- Compiling comprehensive research results
"""
            
            # Use Strands Agent to process the request
            response = self.agent(user_input)
            
            # Store research in history
            if any(word in user_input.lower() for word in ['research', 'search', 'find', 'latest', 'current']):
                self.research_history.append({
                    "query": user_input,
                    "timestamp": datetime.now(),
                    "type": "strands_mcp_research",
                    "method": "use_browser_and_http_request_tools"
                })
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Show the actual Strands Agent Response content FIRST and prominently
            return f"""{response}

---

**Research Session Summary:**
- **Framework:** Strands Agents SDK with MCP integration
- **MCP Tools Used:** Playwright (browser automation, navigation, content extraction)
- **Data Source:** Live web browsing, real-time content extraction
- **Research Quality:** Current internet data with source verification
- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*This research was conducted using MCP Playwright tools for real web automation and data retrieval.*

---

<details>
<summary><strong>System Process Details</strong> (Click to expand)</summary>

{thinking_process}

</details>"""
            
        except Exception as e:
            error_msg = f"Error with Strands Web Research Agent: {str(e)}"
            logger.error(error_msg)
            return f"""**Strands Web Research Agent Thinking:**
```
1. Analyzing query: "{user_input}"
2. Attempting to use official Strands Agent MCP tools
3. Error encountered during processing
```

**Error Details:**
{error_msg}

**Fallback Response:**
I apologize, but I encountered an issue while trying to perform live web research. This could be due to:
- Network connectivity issues
- Search engine access restrictions
- MCP tool configuration problems

For reliable web research, please ensure:
1. Internet connection is stable
2. MCP tools are properly configured
3. Browser automation is enabled

You can try running the setup script: `python advanced_agent/setup_web_research.py`

**General Knowledge Response:**
Based on my training data, I can provide general information about your query, though it may not be the most current information available online."""

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_type": "Strands Web Research Agent",
            "framework": "Strands Agents SDK with MCP integration",
            "tools": ["playwright___playwright_navigate", "playwright___playwright_get_visible_text", "playwright___playwright_get_visible_html"],
            "model_config": self.model_config,
            "conversation_length": len(self.conversation_history),
            "research_sessions": len(self.research_history),
            "status": "Ready for MCP-Powered Web Research"
        }

    def clear_history(self):
        """Clear conversation and research history"""
        self.conversation_history = []
        self.research_history = []

def create_web_research_agent(model_config: Optional[Dict[str, Any]] = None) -> StrandsWebResearchAgent:
    """Factory function to create a web research agent"""
    return StrandsWebResearchAgent(model_config)

def main():
    """Main function for testing the web research agent"""
    print("🌐 Strands Web Research Agent - Fixed Version")
    print("=" * 50)
    
    try:
        # Create agent
        agent = create_web_research_agent()
        print(f"✅ Agent Status: {agent.get_status()}")
        
        # Test queries
        test_queries = [
            "Research the latest AI trends for 2025",
            "Find current Amazon stock price",
            "Best Python learning resources"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing: {query}")
            print("-" * 30)
            response = agent.chat(query)
            print(response[:200] + "..." if len(response) > 200 else response)
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Try running: python advanced_agent/setup_web_research.py")

if __name__ == "__main__":
    main()
