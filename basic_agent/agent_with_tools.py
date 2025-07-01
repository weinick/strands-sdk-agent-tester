"""
Agent with Tools - Enhanced agent with built-in tools
Demonstrates tool integration with Strands SDK
"""

import os
import sys
import json
import math
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    print("Warning: boto3 not installed. Install with: pip install boto3")
    boto3 = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalculatorTool:
    """Calculator tool for mathematical operations"""
    
    @staticmethod
    def calculate(expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Remove any potentially dangerous characters
            safe_chars = set('0123456789+-*/.() ')
            if not all(c in safe_chars for c in expression):
                return "❌ Invalid characters in expression. Only numbers and basic operators (+, -, *, /, parentheses) are allowed."
            
            # Evaluate the expression
            result = eval(expression)
            return f"🧮 **Calculation Result:**\n`{expression} = {result}`"
            
        except ZeroDivisionError:
            return "❌ Error: Division by zero"
        except Exception as e:
            return f"❌ Calculation error: {str(e)}"
    
    @staticmethod
    def advanced_math(operation: str, *args) -> str:
        """Perform advanced mathematical operations"""
        try:
            if operation == "sqrt":
                if len(args) != 1:
                    return "❌ Square root requires exactly one argument"
                result = math.sqrt(float(args[0]))
                return f"🧮 **Square Root:**\n√{args[0]} = {result}"
            
            elif operation == "power":
                if len(args) != 2:
                    return "❌ Power operation requires exactly two arguments (base, exponent)"
                result = math.pow(float(args[0]), float(args[1]))
                return f"🧮 **Power:**\n{args[0]}^{args[1]} = {result}"
            
            elif operation == "log":
                if len(args) != 1:
                    return "❌ Logarithm requires exactly one argument"
                result = math.log(float(args[0]))
                return f"🧮 **Natural Logarithm:**\nln({args[0]}) = {result}"
            
            elif operation == "sin":
                if len(args) != 1:
                    return "❌ Sine requires exactly one argument (in radians)"
                result = math.sin(float(args[0]))
                return f"🧮 **Sine:**\nsin({args[0]}) = {result}"
            
            elif operation == "cos":
                if len(args) != 1:
                    return "❌ Cosine requires exactly one argument (in radians)"
                result = math.cos(float(args[0]))
                return f"🧮 **Cosine:**\ncos({args[0]}) = {result}"
            
            else:
                return f"❌ Unknown operation: {operation}. Available: sqrt, power, log, sin, cos"
                
        except ValueError as e:
            return f"❌ Invalid number format: {str(e)}"
        except Exception as e:
            return f"❌ Math error: {str(e)}"

class WebSearchTool:
    """Web search tool (mock implementation)"""
    
    @staticmethod
    def search(query: str) -> str:
        """Perform web search (mock implementation)"""
        return f"""🔍 **Web Search Results for:** "{query}"

**Note:** This is a mock web search tool for demonstration purposes.

**Mock Results:**
1. **Sample Result 1** - Relevant information about {query}
   - Source: example.com
   - Summary: This would contain relevant information...

2. **Sample Result 2** - More details on {query}  
   - Source: another-site.com
   - Summary: Additional context and information...

3. **Sample Result 3** - {query} explained
   - Source: educational-site.org
   - Summary: Comprehensive explanation...

**To implement real web search:**
- Integrate with search APIs (Google, Bing, DuckDuckGo)
- Use web scraping libraries (BeautifulSoup, Scrapy)
- Add result filtering and ranking

*This tool demonstrates how to integrate external APIs with Strands SDK agents.*"""

class WeatherTool:
    """Weather information tool"""
    
    @staticmethod
    def get_weather(location: str) -> str:
        """Get weather information (mock implementation)"""
        # In a real implementation, you'd call a weather API like OpenWeatherMap
        return f"""🌤️ **Weather for {location}:**

**Current Conditions:**
- Temperature: 72°F (22°C)
- Condition: Partly Cloudy
- Humidity: 65%
- Wind: 8 mph NW
- Pressure: 30.15 in

**Today's Forecast:**
- High: 78°F (26°C)
- Low: 65°F (18°C)
- Chance of Rain: 20%

**Note:** This is mock weather data for demonstration.

**To implement real weather:**
- Sign up for OpenWeatherMap API
- Use requests library to fetch data
- Parse JSON responses
- Handle API errors gracefully

*Example API integration with Strands SDK agents.*"""

class FileOperationsTool:
    """File operations tool"""
    
    @staticmethod
    def list_files(directory: str = ".") -> str:
        """List files in directory"""
        try:
            path = Path(directory)
            if not path.exists():
                return f"❌ Directory not found: {directory}"
            
            files = []
            dirs = []
            
            for item in path.iterdir():
                if item.is_file():
                    size = item.stat().st_size
                    files.append(f"📄 {item.name} ({size} bytes)")
                elif item.is_dir():
                    dirs.append(f"📁 {item.name}/")
            
            result = f"📁 **Contents of {directory}:**\n\n"
            
            if dirs:
                result += "**Directories:**\n"
                for d in sorted(dirs):
                    result += f"  {d}\n"
                result += "\n"
            
            if files:
                result += "**Files:**\n"
                for f in sorted(files):
                    result += f"  {f}\n"
            
            if not dirs and not files:
                result += "*Directory is empty*"
            
            return result
            
        except PermissionError:
            return f"❌ Permission denied accessing: {directory}"
        except Exception as e:
            return f"❌ Error listing files: {str(e)}"
    
    @staticmethod
    def read_file(filepath: str, max_lines: int = 20) -> str:
        """Read file contents"""
        try:
            path = Path(filepath)
            if not path.exists():
                return f"❌ File not found: {filepath}"
            
            if not path.is_file():
                return f"❌ Not a file: {filepath}"
            
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if len(lines) <= max_lines:
                content = ''.join(lines)
            else:
                content = ''.join(lines[:max_lines])
                content += f"\n... (showing first {max_lines} lines of {len(lines)} total)"
            
            return f"📄 **Contents of {filepath}:**\n\n```\n{content}\n```"
            
        except UnicodeDecodeError:
            return f"❌ Cannot read file (binary or unsupported encoding): {filepath}"
        except PermissionError:
            return f"❌ Permission denied reading: {filepath}"
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"

class AgentWithTools:
    """
    Enhanced agent with built-in tools for various operations
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the agent with tools"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        self.conversation_history = []
        self.bedrock_client = None
        
        # Initialize tools
        self.calculator = CalculatorTool()
        self.web_search = WebSearchTool()
        self.weather = WeatherTool()
        self.file_ops = FileOperationsTool()
        
        # Initialize Bedrock client if using AWS
        if self.model_config.get("provider") == "AWS Bedrock":
            self._init_bedrock_client()
    
    def _init_bedrock_client(self):
        """Initialize AWS Bedrock client"""
        try:
            if boto3:
                self.bedrock_client = boto3.client(
                    'bedrock-runtime',
                    region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
                )
                logger.info("✅ AWS Bedrock client initialized successfully")
            else:
                logger.warning("⚠️ boto3 not available, using mock responses")
        except NoCredentialsError:
            logger.error("❌ AWS credentials not found. Please configure AWS CLI or set environment variables")
        except Exception as e:
            logger.error(f"❌ Error initializing Bedrock client: {str(e)}")
    
    def chat(self, user_input: str) -> str:
        """
        Process user input, determine if tools are needed, and return response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Check if user input requires tool usage
            tool_response = self._check_and_use_tools(user_input)
            
            if tool_response:
                # Tool was used, return the tool response
                response = tool_response
            else:
                # No tool needed, generate conversational response
                if self.bedrock_client and self.model_config.get("provider") == "AWS Bedrock":
                    response = self._call_bedrock(user_input)
                else:
                    response = self._generate_conversational_response(user_input)
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def _check_and_use_tools(self, user_input: str) -> Optional[str]:
        """Check if user input requires tool usage and execute appropriate tool"""
        user_lower = user_input.lower()
        
        # Calculator tool triggers
        if any(word in user_lower for word in ['calculate', 'compute', 'math', 'solve']):
            # Extract mathematical expression
            if any(op in user_input for op in ['+', '-', '*', '/', '(', ')']):
                # Find the mathematical expression
                import re
                math_pattern = r'[\d+\-*/().\s]+'
                matches = re.findall(math_pattern, user_input)
                if matches:
                    expression = max(matches, key=len).strip()
                    return self.calculator.calculate(expression)
            
            # Check for advanced math operations
            if 'sqrt' in user_lower or 'square root' in user_lower:
                numbers = re.findall(r'\d+\.?\d*', user_input)
                if numbers:
                    return self.calculator.advanced_math('sqrt', numbers[0])
            
            elif 'power' in user_lower or '^' in user_input:
                numbers = re.findall(r'\d+\.?\d*', user_input)
                if len(numbers) >= 2:
                    return self.calculator.advanced_math('power', numbers[0], numbers[1])
            
            return "🧮 I can help with calculations! Try:\n• Simple math: `2 + 2`, `10 * 5`, `(15 + 3) / 2`\n• Advanced: `sqrt of 16`, `2 power 3`\n• Functions: `sin`, `cos`, `log`"
        
        # Web search tool triggers
        elif any(word in user_lower for word in ['search', 'find', 'lookup', 'google']):
            # Extract search query
            search_terms = user_input.replace('search for', '').replace('find', '').replace('lookup', '').replace('google', '').strip()
            if search_terms:
                return self.web_search.search(search_terms)
            return "🔍 What would you like me to search for?"
        
        # Weather tool triggers
        elif any(word in user_lower for word in ['weather', 'temperature', 'forecast']):
            # Extract location
            location_words = user_input.split()
            # Simple location extraction (in real implementation, use NLP)
            location = "your location"
            for i, word in enumerate(location_words):
                if word.lower() in ['in', 'for', 'at']:
                    if i + 1 < len(location_words):
                        location = ' '.join(location_words[i+1:])
                        break
            return self.weather.get_weather(location)
        
        # File operations tool triggers
        elif any(word in user_lower for word in ['list files', 'show files', 'directory']):
            directory = "."
            if 'in' in user_lower:
                parts = user_input.split('in')
                if len(parts) > 1:
                    directory = parts[-1].strip()
            return self.file_ops.list_files(directory)
        
        elif any(word in user_lower for word in ['read file', 'show file', 'open file']):
            # Extract filename
            words = user_input.split()
            filename = None
            for i, word in enumerate(words):
                if word.lower() in ['file', 'read', 'show', 'open']:
                    if i + 1 < len(words):
                        filename = words[i + 1]
                        break
            
            if filename:
                return self.file_ops.read_file(filename)
            return "📄 Please specify which file you'd like me to read."
        
        return None  # No tool needed
    
    def _call_bedrock(self, user_input: str) -> str:
        """Call AWS Bedrock API for conversational response"""
        try:
            # Prepare messages with tool context
            system_message = """You are an AI assistant with access to various tools including:
- Calculator for mathematical operations
- Web search for finding information
- Weather data for location-based queries  
- File operations for reading and listing files

When users ask for calculations, searches, weather, or file operations, I will use the appropriate tools. 
For general conversation, respond naturally and helpfully."""
            
            messages = [{"role": "user", "content": f"{system_message}\n\nUser: {user_input}"}]
            
            # Add recent conversation history for context
            for msg in self.conversation_history[-6:]:  # Last 6 messages for context
                messages.append(msg)
            
            if "claude" in self.model_config["model"].lower():
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": self.model_config.get("max_tokens", 1000),
                    "temperature": self.model_config.get("temperature", 0.7),
                    "messages": messages
                }
            else:
                body = {
                    "inputText": user_input,
                    "textGenerationConfig": {
                        "maxTokenCount": self.model_config.get("max_tokens", 1000),
                        "temperature": self.model_config.get("temperature", 0.7)
                    }
                }
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_config["model"],
                body=json.dumps(body),
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            
            if "claude" in self.model_config["model"].lower():
                return response_body['content'][0]['text']
            else:
                return response_body.get('results', [{}])[0].get('outputText', 'No response generated')
                
        except Exception as e:
            return f"❌ Bedrock API error: {str(e)}"
    
    def _generate_conversational_response(self, user_input: str) -> str:
        """Generate conversational response when Bedrock is not available"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return """Hello! I'm an Agent with Tools, powered by the Strands SDK. 

I have access to several useful tools:
🧮 **Calculator** - For mathematical operations
🔍 **Web Search** - To find information online  
🌤️ **Weather** - For weather forecasts
📁 **File Operations** - To read and list files

Try asking me to:
• Calculate something: "What's 15 * 8?"
• Search for information: "Search for Python tutorials"
• Check weather: "What's the weather like?"
• List files: "Show me the files in this directory"

How can I help you today?"""
        
        elif any(word in user_lower for word in ['what can you do', 'capabilities', 'help', 'tools']):
            return """I'm an enhanced AI agent with access to multiple tools! Here's what I can do:

🧮 **Calculator Tool:**
• Basic math: addition, subtraction, multiplication, division
• Advanced functions: square root, power, logarithm, trigonometry
• Complex expressions with parentheses

🔍 **Web Search Tool:**
• Search for current information
• Find articles, tutorials, and resources
• Get up-to-date data on various topics

🌤️ **Weather Tool:**
• Current weather conditions
• Temperature and humidity
• Forecasts and weather alerts

📁 **File Operations Tool:**
• List files and directories
• Read file contents
• Navigate file system

💬 **Conversational AI:**
• Natural language understanding
• Context-aware responses
• Helpful explanations and guidance

**Example Commands:**
• "Calculate 25 * 4 + 10"
• "Search for machine learning tutorials"
• "What's the weather in New York?"
• "List files in the current directory"
• "Read the README.md file"

What would you like to try?"""
        
        elif any(word in user_lower for word in ['goodbye', 'bye', 'thanks']):
            return """You're welcome! It was great helping you test the Agent with Tools.

Remember, I have access to:
🧮 Calculator | 🔍 Web Search | 🌤️ Weather | 📁 File Operations

Feel free to come back anytime to try out different tools or ask questions. The Strands SDK makes it easy to build powerful agents like me!

Goodbye! 👋"""
        
        else:
            return f"""I received your message: "{user_input}"

As an Agent with Tools, I can help you with various tasks using my built-in tools:

🧮 **For calculations:** Try "calculate 15 + 25" or "what's the square root of 64?"
🔍 **For information:** Try "search for [topic]" or "find information about [subject]"
🌤️ **For weather:** Try "what's the weather?" or "weather forecast"
📁 **For files:** Try "list files" or "read [filename]"

I also enjoy general conversation! Feel free to ask me questions or chat about topics you're interested in.

**Current Configuration:**
- Provider: {self.model_config.get('provider', 'Mock')}
- Model: {self.model_config.get('model', 'Tools Demo')}
- Available Tools: Calculator, Web Search, Weather, File Operations

What would you like to explore?"""
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return ["Calculator", "Web Search", "Weather", "File Operations"]
    
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_type": "Agent with Tools",
            "model_config": self.model_config,
            "available_tools": self.get_available_tools(),
            "conversation_length": len(self.conversation_history),
            "bedrock_available": self.bedrock_client is not None,
            "status": "Ready"
        }

def create_agent_with_tools(model_config: Optional[Dict[str, Any]] = None) -> AgentWithTools:
    """Factory function to create an Agent with Tools"""
    return AgentWithTools(model_config)

def main():
    """Main function for testing the agent directly"""
    print("🛠️ Agent with Tools - Strands SDK Demo")
    print("=" * 50)
    
    # Create agent
    agent = create_agent_with_tools()
    
    print("Agent initialized with tools:", agent.get_available_tools())
    print("Status:", agent.get_status())
    print("-" * 50)
    print("Try commands like:")
    print("• 'calculate 15 * 8'")
    print("• 'search for Python'") 
    print("• 'what's the weather?'")
    print("• 'list files'")
    print("• Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAgent: Goodbye! Thanks for testing the Agent with Tools!")
                break
            
            if user_input:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thanks for testing the Agent with Tools!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
