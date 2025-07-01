#!/usr/bin/env python3
"""
Multi-Agent System Example - Strands Agents SDK

This example demonstrates how to create a multi-agent system where different
agents specialize in different tasks and can collaborate to solve complex problems.

Prerequisites:
- AWS credentials configured (for default Bedrock model provider)
- Claude 3.7 Sonnet model access enabled in AWS Bedrock (us-west-2 region)
"""

import os
import logging
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
from strands import Agent, tool

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


# Specialized tools for different agents
@tool
def calculate_math(expression: str) -> Dict[str, Any]:
    """Perform mathematical calculations safely.
    
    Evaluates mathematical expressions using safe evaluation.
    Supports basic arithmetic, powers, and common math functions.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Dictionary containing calculation result and metadata
    """
    import math
    
    # Safe evaluation context with math functions
    safe_dict = {
        "__builtins__": {},
        "abs": abs, "round": round, "min": min, "max": max,
        "sum": sum, "pow": pow,
        "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "log": math.log, "log10": math.log10, "exp": math.exp,
        "pi": math.pi, "e": math.e
    }
    
    try:
        result = eval(expression, safe_dict)
        return {
            "success": True,
            "expression": expression,
            "result": result,
            "type": type(result).__name__
        }
    except Exception as e:
        return {
            "success": False,
            "expression": expression,
            "error": str(e)
        }


@tool
def analyze_text_content(text: str) -> Dict[str, Any]:
    """Analyze text content for various metrics and insights.
    
    Provides comprehensive text analysis including readability,
    sentiment indicators, and structural analysis.
    
    Args:
        text: Text content to analyze
        
    Returns:
        Dictionary containing text analysis results
    """
    words = text.split()
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # Basic metrics
    word_count = len(words)
    sentence_count = len(sentences)
    paragraph_count = len(paragraphs)
    char_count = len(text)
    
    # Average metrics
    avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
    avg_chars_per_word = char_count / word_count if word_count > 0 else 0
    
    # Word frequency analysis
    word_freq = {}
    for word in words:
        clean_word = word.lower().strip('.,!?;:"()[]{}')
        if clean_word and len(clean_word) > 2:  # Ignore very short words
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    # Most common words
    most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Simple sentiment indicators (basic keyword matching)
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'joy']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'disappointed']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    sentiment_score = positive_count - negative_count
    if sentiment_score > 0:
        sentiment = "positive"
    elif sentiment_score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "character_count": char_count,
        "avg_words_per_sentence": round(avg_words_per_sentence, 2),
        "avg_chars_per_word": round(avg_chars_per_word, 2),
        "most_common_words": most_common,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "readability_estimate": "easy" if avg_words_per_sentence < 15 else "moderate" if avg_words_per_sentence < 25 else "difficult"
    }


@tool
def format_data(data: Any, format_type: str = "json") -> Dict[str, Any]:
    """Format data in various formats for presentation.
    
    Converts data to different formats for better readability and presentation.
    
    Args:
        data: Data to format (can be dict, list, or string)
        format_type: Format type (json, table, list, summary)
        
    Returns:
        Dictionary containing formatted data and metadata
    """
    try:
        if format_type.lower() == "json":
            if isinstance(data, str):
                # Try to parse as JSON first
                try:
                    parsed_data = json.loads(data)
                    formatted = json.dumps(parsed_data, indent=2, sort_keys=True)
                except json.JSONDecodeError:
                    formatted = json.dumps({"text": data}, indent=2)
            else:
                formatted = json.dumps(data, indent=2, sort_keys=True, default=str)
            
            return {
                "success": True,
                "format": "json",
                "formatted_data": formatted,
                "original_type": type(data).__name__
            }
        
        elif format_type.lower() == "table":
            if isinstance(data, list) and data and isinstance(data[0], dict):
                # Format as table for list of dictionaries
                headers = list(data[0].keys())
                table = "| " + " | ".join(headers) + " |\n"
                table += "| " + " | ".join(["-" * len(h) for h in headers]) + " |\n"
                
                for row in data:
                    values = [str(row.get(h, "")) for h in headers]
                    table += "| " + " | ".join(values) + " |\n"
                
                formatted = table
            else:
                formatted = str(data)
            
            return {
                "success": True,
                "format": "table",
                "formatted_data": formatted,
                "original_type": type(data).__name__
            }
        
        elif format_type.lower() == "list":
            if isinstance(data, (list, tuple)):
                formatted = "\n".join([f"• {item}" for item in data])
            elif isinstance(data, dict):
                formatted = "\n".join([f"• {k}: {v}" for k, v in data.items()])
            else:
                formatted = f"• {data}"
            
            return {
                "success": True,
                "format": "list",
                "formatted_data": formatted,
                "original_type": type(data).__name__
            }
        
        else:
            return {
                "success": False,
                "error": f"Unsupported format type: {format_type}",
                "supported_formats": ["json", "table", "list"]
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "format": format_type
        }


class MultiAgentSystem:
    """Multi-agent system that coordinates specialized agents."""
    
    def __init__(self):
        """Initialize the multi-agent system with specialized agents."""
        
        # Math Specialist Agent
        self.math_agent = Agent(
            tools=[calculate_math],
            system_prompt="""You are a mathematics specialist agent. Your expertise is in:
            - Performing accurate mathematical calculations
            - Solving equations and mathematical problems
            - Explaining mathematical concepts
            - Working with numbers, formulas, and mathematical expressions
            
            When given mathematical tasks, use your calculate_math tool to provide precise results.
            Always show your work and explain the mathematical reasoning."""
        )
        
        # Text Analysis Specialist Agent
        self.text_agent = Agent(
            tools=[analyze_text_content],
            system_prompt="""You are a text analysis specialist agent. Your expertise is in:
            - Analyzing text content for various metrics
            - Providing insights about readability and structure
            - Identifying patterns in text
            - Offering writing and content improvement suggestions
            
            When given text analysis tasks, use your analyze_text_content tool to provide comprehensive insights.
            Always explain what the metrics mean and provide actionable recommendations."""
        )
        
        # Data Formatting Specialist Agent
        self.format_agent = Agent(
            tools=[format_data],
            system_prompt="""You are a data formatting specialist agent. Your expertise is in:
            - Converting data between different formats
            - Making data more readable and presentable
            - Structuring information for better understanding
            - Creating well-formatted outputs
            
            When given formatting tasks, use your format_data tool to present information clearly.
            Always choose the most appropriate format for the given data and context."""
        )
        
        # Coordinator Agent (uses other agents as tools)
        self.coordinator = Agent(
            system_prompt="""You are a coordinator agent that manages a team of specialist agents:
            
            1. Math Agent: Handles mathematical calculations and problems
            2. Text Agent: Analyzes text content and provides writing insights
            3. Format Agent: Formats data and makes it more presentable
            
            When users request complex tasks that involve multiple specialties:
            1. Break down the task into components
            2. Identify which specialist agents are needed
            3. Coordinate the work between agents
            4. Synthesize the results into a comprehensive response
            
            You don't have direct access to the specialist tools, but you can describe what each agent would do
            and coordinate their efforts conceptually."""
        )
    
    def process_with_specialist(self, task: str, agent_type: str) -> Dict[str, Any]:
        """Process a task with a specific specialist agent.
        
        Args:
            task: Task description
            agent_type: Type of agent ('math', 'text', 'format')
            
        Returns:
            Dictionary containing agent response and metadata
        """
        try:
            if agent_type == 'math':
                response = self.math_agent(task)
                agent_name = "Math Specialist"
            elif agent_type == 'text':
                response = self.text_agent(task)
                agent_name = "Text Analysis Specialist"
            elif agent_type == 'format':
                response = self.format_agent(task)
                agent_name = "Data Formatting Specialist"
            else:
                return {
                    "success": False,
                    "error": f"Unknown agent type: {agent_type}",
                    "available_types": ["math", "text", "format"]
                }
            
            return {
                "success": True,
                "agent": agent_name,
                "response": str(response),
                "metrics": {
                    "stop_reason": response.stop_reason,
                    "processing_time": response.metrics.total_time_seconds,
                    "tool_calls": response.metrics.tool_calls
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": agent_type
            }
    
    def coordinate_complex_task(self, task: str) -> Dict[str, Any]:
        """Coordinate a complex task that may require multiple agents.
        
        Args:
            task: Complex task description
            
        Returns:
            Dictionary containing coordination results
        """
        try:
            # Use coordinator to plan the approach
            coordination_response = self.coordinator(f"""
            I need to coordinate the following complex task: {task}
            
            Please analyze this task and:
            1. Identify which specialist agents would be needed
            2. Break down the task into components for each agent
            3. Suggest the order of operations
            4. Explain how the results should be combined
            """)
            
            return {
                "success": True,
                "task": task,
                "coordination_plan": str(coordination_response),
                "coordinator_metrics": {
                    "stop_reason": coordination_response.stop_reason,
                    "processing_time": coordination_response.metrics.total_time_seconds
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": task
            }


def main():
    """Demonstrate multi-agent system capabilities."""
    
    print("🤖 Creating multi-agent system...")
    
    try:
        # Initialize multi-agent system
        mas = MultiAgentSystem()
        
        print("✅ Multi-agent system created successfully!")
        print("🎯 Available specialist agents:")
        print("   - Math Specialist: Mathematical calculations and problem solving")
        print("   - Text Analysis Specialist: Text content analysis and insights")
        print("   - Data Formatting Specialist: Data formatting and presentation")
        print("   - Coordinator: Task coordination and planning")
        
        print("\n" + "="*70)
        print("🔬 Testing individual specialist agents")
        print("="*70)
        
        # Test individual specialists
        specialist_tests = [
            ("math", "Calculate the compound interest for $1000 invested at 5% annual rate for 3 years using the formula A = P(1 + r)^t"),
            ("text", "Analyze this product review: 'This product is absolutely amazing! I love how easy it is to use and the quality is fantastic. Highly recommended for anyone looking for a reliable solution.'"),
            ("format", "Format this data as a JSON: Name: John Doe, Age: 30, City: New York, Hobbies: reading, swimming, cooking")
        ]
        
        for agent_type, task in specialist_tests:
            print(f"\n🎯 {agent_type.upper()} Agent Task: {task}")
            print("-" * 60)
            
            result = mas.process_with_specialist(task, agent_type)
            
            if result["success"]:
                print(f"🤖 {result['agent']}: {result['response']}")
                print(f"\n📊 Agent metrics:")
                print(f"   - Processing time: {result['metrics']['processing_time']:.2f}s")
                print(f"   - Tool calls: {result['metrics']['tool_calls']}")
            else:
                print(f"❌ Error: {result['error']}")
        
        print("\n" + "="*70)
        print("🎭 Testing complex task coordination")
        print("="*70)
        
        # Test complex task coordination
        complex_tasks = [
            "I need to analyze a business report that contains financial data and text. The report shows revenue of $150,000 with 15% growth, and includes customer feedback. I want to calculate the previous year's revenue, analyze the sentiment of the feedback, and format everything in a professional presentation format.",
            "Help me process survey data: 50 responses with average satisfaction score of 4.2/5, and this comment: 'The service was good but could be improved in terms of speed and efficiency.' I need mathematical analysis of the scores and text analysis of the comment, then format the results clearly.",
        ]
        
        for i, task in enumerate(complex_tasks, 1):
            print(f"\n🎯 Complex Task {i}: {task}")
            print("-" * 60)
            
            coordination_result = mas.coordinate_complex_task(task)
            
            if coordination_result["success"]:
                print(f"🎭 Coordinator Plan: {coordination_result['coordination_plan']}")
                print(f"\n📊 Coordination metrics:")
                print(f"   - Planning time: {coordination_result['coordinator_metrics']['processing_time']:.2f}s")
            else:
                print(f"❌ Coordination error: {coordination_result['error']}")
        
        print("\n" + "="*70)
        print("🔧 Direct tool demonstrations")
        print("="*70)
        
        # Direct tool usage examples
        print("\n📞 Direct math calculation:")
        math_result = mas.math_agent.tool.calculate_math(expression="sqrt(144) + 10^2")
        print(f"   Result: {math_result}")
        
        print("\n📞 Direct text analysis:")
        text_result = mas.text_agent.tool.analyze_text_content(
            text="Artificial intelligence is revolutionizing the way we work. It's amazing how quickly technology advances!"
        )
        print(f"   Analysis: {text_result}")
        
        print("\n📞 Direct data formatting:")
        format_result = mas.format_agent.tool.format_data(
            data={"name": "Alice", "score": 95, "grade": "A"}, 
            format_type="json"
        )
        print(f"   Formatted: {format_result}")
        
    except Exception as e:
        logger.error(f"Error in multi-agent system: {e}")
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. AWS credentials configured")
        print("   2. Claude 3.7 Sonnet model access enabled in AWS Bedrock")
        return 1
    
    print("\n✨ Multi-agent system example completed!")
    return 0


def create_multi_agent_system(model_config: Dict[str, Any] = None) -> MultiAgentSystem:
    """Factory function to create a Multi Agent System"""
    return MultiAgentSystem(model_config)


if __name__ == "__main__":
    exit(main())
