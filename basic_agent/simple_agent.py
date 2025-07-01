"""
Simple Agent - Basic conversational agent using Strands SDK
Demonstrates minimal agent setup with AWS Bedrock
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    print("Warning: boto3 not installed. Install with: pip install boto3")
    boto3 = None

import json
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAgent:
    """
    A simple conversational agent using AWS Bedrock
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the simple agent"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        self.conversation_history = []
        self.bedrock_client = None
        
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
        Process user input and return agent response
        
        Args:
            user_input: User's message
            
        Returns:
            Agent's response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Generate response
            if self.bedrock_client and self.model_config.get("provider") == "AWS Bedrock":
                response = self._call_bedrock(user_input)
            else:
                response = self._generate_mock_response(user_input)
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant", 
                "content": response
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def _call_bedrock(self, user_input: str) -> str:
        """Call AWS Bedrock API"""
        try:
            # Prepare the prompt with conversation history
            messages = []
            for msg in self.conversation_history[-10:]:  # Keep last 10 messages for context
                messages.append(msg)
            
            # Prepare request body based on model
            if "claude" in self.model_config["model"].lower():
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": self.model_config.get("max_tokens", 1000),
                    "temperature": self.model_config.get("temperature", 0.7),
                    "messages": messages
                }
            else:
                # Generic format for other models
                body = {
                    "inputText": user_input,
                    "textGenerationConfig": {
                        "maxTokenCount": self.model_config.get("max_tokens", 1000),
                        "temperature": self.model_config.get("temperature", 0.7)
                    }
                }
            
            # Make the API call
            response = self.bedrock_client.invoke_model(
                modelId=self.model_config["model"],
                body=json.dumps(body),
                contentType="application/json"
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            if "claude" in self.model_config["model"].lower():
                return response_body['content'][0]['text']
            else:
                return response_body.get('results', [{}])[0].get('outputText', 'No response generated')
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ValidationException':
                return "❌ Model validation error. Please check if the Claude model is enabled in your AWS Bedrock console."
            elif error_code == 'AccessDeniedException':
                return "❌ Access denied. Please check your AWS permissions for Bedrock."
            else:
                return f"❌ AWS Bedrock error ({error_code}): {str(e)}"
        except Exception as e:
            return f"❌ Bedrock API error: {str(e)}"
    
    def _generate_mock_response(self, user_input: str) -> str:
        """Generate mock response when Bedrock is not available"""
        user_lower = user_input.lower()
        
        # Simple keyword-based responses
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return """Hello! I'm a Simple Agent built with the Strands SDK. 

I'm designed to have natural conversations and can help you with:
• General questions and discussions
• Basic information requests  
• Casual conversation
• Testing the Strands SDK functionality

How can I assist you today?"""
        
        elif any(word in user_lower for word in ['how are you', 'how do you do', 'what\'s up']):
            return """I'm doing well, thank you for asking! 

As a Simple Agent, I'm functioning properly and ready to help. I'm built using the Strands SDK and designed to be a friendly conversational companion.

Is there anything specific you'd like to talk about or any way I can help you?"""
        
        elif any(word in user_lower for word in ['what can you do', 'capabilities', 'help', 'abilities']):
            return """As a Simple Agent, I have several capabilities:

**Conversational Skills:**
• Natural language understanding and generation
• Context-aware responses based on our conversation
• Friendly and helpful personality

**Technical Features:**
• Built with Strands SDK framework
• AWS Bedrock integration (when configured)
• Conversation history tracking
• Error handling and graceful fallbacks

**What I Can Help With:**
• Answer questions on various topics
• Engage in casual conversation
• Provide information and explanations
• Test and demonstrate Strands SDK functionality

**Limitations:**
• I don't have access to real-time information
• I can't perform calculations (try the Agent with Tools for that!)
• I can't browse the web or access external APIs

What would you like to explore together?"""
        
        elif any(word in user_lower for word in ['goodbye', 'bye', 'see you', 'farewell']):
            return """Goodbye! It was great chatting with you. 

Thank you for testing the Simple Agent. Feel free to come back anytime to continue our conversation or try out the other agents available in the Strands SDK!

Have a wonderful day! 👋"""
        
        elif any(word in user_lower for word in ['strands', 'sdk', 'framework']):
            return """Great question about the Strands SDK! 

The Strands Agents SDK is Amazon's framework for building AI agents. Here's what makes it special:

**Key Features:**
• **Model-agnostic**: Works with AWS Bedrock, OpenAI, Anthropic, and more
• **Code-first approach**: Simple Python-based agent development
• **Built-in tools**: Pre-built tools for common tasks
• **Custom tools**: Easy creation of specialized tools
• **Multi-agent systems**: Support for agent collaboration
• **Production-ready**: Includes deployment patterns

**Why I'm a good example:**
I demonstrate the basic conversational capabilities you can build with just a few lines of code using the Strands SDK. More complex agents can include tools, web search, file operations, and much more!

Would you like to know more about any specific aspect?"""
        
        elif any(word in user_lower for word in ['weather', 'temperature', 'forecast']):
            return """I don't have access to real-time weather data, but I can suggest how to get that information!

**For weather information, try:**
• The **Web Research Agent** - can search for current weather
• The **Agent with Tools** - has weather API capabilities
• Or ask me to help you think through weather-related questions

If you're building a weather-capable agent with Strands SDK, you'd typically integrate with weather APIs like OpenWeatherMap or AWS weather services.

Is there something specific about weather you'd like to discuss?"""
        
        elif any(word in user_lower for word in ['calculate', 'math', 'compute', 'number']):
            return """I'm a Simple Agent, so I don't have calculation capabilities built in.

**For mathematical operations, try:**
• **Agent with Tools** - has a built-in calculator
• **Custom Tool Agent** - can be configured with specialized math tools

**What I can help with instead:**
• Explain mathematical concepts
• Discuss problem-solving approaches
• Help you think through mathematical questions conceptually

If you're interested in building calculation capabilities into Strands SDK agents, I'd be happy to discuss the architectural approaches!

What kind of mathematical help were you looking for?"""
        
        else:
            return f"""Thank you for your message: "{user_input}"

As a Simple Agent, I aim to be helpful and conversational. While I may not have specialized tools or real-time data access, I can:

• Engage in meaningful conversation
• Provide general information and explanations  
• Help you explore ideas and concepts
• Demonstrate basic Strands SDK functionality

**Some things you might try asking me:**
• Questions about the Strands SDK
• General topics you're curious about
• How I work as an AI agent
• Casual conversation topics

**For more advanced capabilities, try:**
• **Agent with Tools** - for calculations, web search, etc.
• **Web Research Agent** - for current information
• **File Manager Agent** - for file operations

What would you like to explore together?

*Current Configuration:*
- Provider: {self.model_config.get('provider', 'Mock')}
- Model: {self.model_config.get('model', 'Simple Demo')}
- Temperature: {self.model_config.get('temperature', 0.7)}"""
    
    def get_conversation_history(self) -> list:
        """Get the conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "agent_type": "Simple Agent",
            "model_config": self.model_config,
            "conversation_length": len(self.conversation_history),
            "bedrock_available": self.bedrock_client is not None,
            "status": "Ready"
        }

def create_simple_agent(model_config: Optional[Dict[str, Any]] = None) -> SimpleAgent:
    """Factory function to create a Simple Agent"""
    return SimpleAgent(model_config)

def main():
    """Main function for testing the agent directly"""
    print("🤖 Simple Agent - Strands SDK Demo")
    print("=" * 40)
    
    # Create agent
    agent = create_simple_agent()
    
    print("Agent initialized! Type 'quit' to exit.")
    print("Status:", agent.get_status())
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAgent: Goodbye! Thanks for testing the Simple Agent!")
                break
            
            if user_input:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thanks for testing the Simple Agent!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
