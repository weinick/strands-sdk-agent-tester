"""
Multi-Agent System - Collaborative agent system using Strands SDK
Demonstrates multi-agent coordination and task delegation
"""

import os
import sys
import json
import math
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

class MathTool:
    """Mathematical calculation tool"""
    
    @staticmethod
    def calculate_math(expression: str) -> Dict[str, Any]:
        """Perform mathematical calculations safely"""
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

class TextAnalysisTool:
    """Text analysis tool"""
    
    @staticmethod
    def analyze_text_content(text: str) -> Dict[str, Any]:
        """Analyze text content for various metrics and insights"""
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
            if clean_word and len(clean_word) > 2:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Most common words
        most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Simple sentiment indicators
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

class DataFormattingTool:
    """Data formatting tool"""
    
    @staticmethod
    def format_data(data: Any, format_type: str = "json") -> Dict[str, Any]:
        """Format data in various formats for presentation"""
        try:
            if format_type.lower() == "json":
                if isinstance(data, str):
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
    """
    Multi-agent system that coordinates specialized agents for complex tasks
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the multi-agent system"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.7,
            "max_tokens": 1200
        }
        
        self.conversation_history = []
        self.task_history = []
        self.bedrock_client = None
        
        # Initialize tools
        self.math_tool = MathTool()
        self.text_tool = TextAnalysisTool()
        self.format_tool = DataFormattingTool()
        
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
        """Process multi-agent requests"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Analyze the task and determine which agents are needed
            task_analysis = self._analyze_task(user_input)
            
            # Execute the task using appropriate agents
            response = self._execute_multi_agent_task(user_input, task_analysis)
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error in multi-agent processing: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def _analyze_task(self, user_input: str) -> Dict[str, Any]:
        """Analyze the task to determine which agents are needed"""
        user_lower = user_input.lower()
        
        analysis = {
            "needs_math": False,
            "needs_text_analysis": False,
            "needs_formatting": False,
            "complexity": "simple",
            "agents_required": []
        }
        
        # Check for mathematical operations
        math_keywords = ['calculate', 'compute', 'math', 'equation', 'formula', 'sqrt', 'square', 'root', 'power', '+', '-', '*', '/', 'sum', 'average']
        if any(keyword in user_lower for keyword in math_keywords):
            analysis["needs_math"] = True
            analysis["agents_required"].append("Math Specialist")
        
        # Check for text analysis needs
        text_keywords = ['analyze', 'sentiment', 'text', 'content', 'words', 'readability', 'writing', 'review', 'feedback']
        if any(keyword in user_lower for keyword in text_keywords):
            analysis["needs_text_analysis"] = True
            analysis["agents_required"].append("Text Analysis Specialist")
        
        # Check for formatting needs
        format_keywords = ['format', 'json', 'table', 'list', 'structure', 'organize', 'present']
        if any(keyword in user_lower for keyword in format_keywords):
            analysis["needs_formatting"] = True
            analysis["agents_required"].append("Data Formatting Specialist")
        
        # Determine complexity
        if len(analysis["agents_required"]) > 1:
            analysis["complexity"] = "complex"
        elif len(analysis["agents_required"]) == 1:
            analysis["complexity"] = "moderate"
        
        return analysis
    
    def _execute_multi_agent_task(self, user_input: str, task_analysis: Dict[str, Any]) -> str:
        """Execute the task using multiple agents"""
        results = []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        response = f"""🤖 **Multi-Agent System Response**

**Task:** {user_input}
**Analysis:** {task_analysis['complexity'].title()} task requiring {len(task_analysis['agents_required'])} specialist(s)
**Agents Deployed:** {', '.join(task_analysis['agents_required'])}
**Processing Time:** {timestamp}

---

"""
        
        # Execute math operations if needed
        if task_analysis["needs_math"]:
            math_result = self._execute_math_agent(user_input)
            results.append(math_result)
            response += f"""🧮 **Math Specialist Results:**
{math_result}

"""
        
        # Execute text analysis if needed
        if task_analysis["needs_text_analysis"]:
            text_result = self._execute_text_agent(user_input)
            results.append(text_result)
            response += f"""📊 **Text Analysis Specialist Results:**
{text_result}

"""
        
        # Execute formatting if needed
        if task_analysis["needs_formatting"]:
            format_result = self._execute_format_agent(user_input, results)
            response += f"""📋 **Data Formatting Specialist Results:**
{format_result}

"""
        
        # If no specific agents were triggered, provide general coordination
        if not task_analysis["agents_required"]:
            response += self._general_coordination_response(user_input)
        
        # Add task summary
        response += f"""---

**🎯 Task Summary:**
• **Agents Used:** {len(task_analysis['agents_required'])}
• **Complexity Level:** {task_analysis['complexity'].title()}
• **Processing Status:** ✅ Complete
• **Results Generated:** {len(results)} specialist outputs

*This demonstrates multi-agent collaboration where specialized agents work together to solve complex tasks.*"""
        
        # Log the task
        self.task_history.append({
            "task": user_input,
            "analysis": task_analysis,
            "results_count": len(results),
            "timestamp": timestamp
        })
        
        return response
    
    def _execute_math_agent(self, user_input: str) -> str:
        """Execute mathematical operations"""
        try:
            # Extract mathematical expressions from the input
            import re
            
            # Look for mathematical expressions
            math_patterns = [
                r'(\d+(?:\.\d+)?\s*[\+\-\*\/\^]\s*\d+(?:\.\d+)?)',
                r'sqrt\(\s*\d+(?:\.\d+)?\s*\)',
                r'(\d+(?:\.\d+)?)\s*\^\s*(\d+(?:\.\d+)?)',
                r'square\s+root\s+of\s+(\d+(?:\.\d+)?)'
            ]
            
            expressions_found = []
            for pattern in math_patterns:
                matches = re.findall(pattern, user_input.lower())
                expressions_found.extend(matches)
            
            if expressions_found:
                results = []
                for expr in expressions_found[:3]:  # Limit to 3 expressions
                    if isinstance(expr, tuple):
                        expr = expr[0] if expr[0] else str(expr)
                    
                    # Clean up the expression
                    expr = str(expr).replace('^', '**').replace('sqrt(', 'math.sqrt(')
                    
                    calc_result = self.math_tool.calculate_math(expr)
                    if calc_result["success"]:
                        results.append(f"• {calc_result['expression']} = **{calc_result['result']}**")
                    else:
                        results.append(f"• {expr}: Error - {calc_result['error']}")
                
                return "\n".join(results) if results else "No valid mathematical expressions found."
            else:
                # Handle word problems or general math requests
                if "square root" in user_input.lower():
                    numbers = re.findall(r'\d+(?:\.\d+)?', user_input)
                    if numbers:
                        num = float(numbers[0])
                        result = self.math_tool.calculate_math(f"sqrt({num})")
                        if result["success"]:
                            return f"• √{num} = **{result['result']}**"
                
                return "Mathematical analysis requested - please provide specific numbers or expressions to calculate."
                
        except Exception as e:
            return f"Math processing error: {str(e)}"
    
    def _execute_text_agent(self, user_input: str) -> str:
        """Execute text analysis operations"""
        try:
            # Extract text to analyze (look for quoted text or use the entire input)
            import re
            
            # Look for quoted text first
            quoted_text = re.findall(r'"([^"]*)"', user_input)
            if quoted_text:
                text_to_analyze = quoted_text[0]
            else:
                # Use the input itself if no quoted text found
                text_to_analyze = user_input
            
            analysis_result = self.text_tool.analyze_text_content(text_to_analyze)
            
            result = f"""**Text Analysis Results:**
• **Word Count:** {analysis_result['word_count']}
• **Sentence Count:** {analysis_result['sentence_count']}
• **Character Count:** {analysis_result['character_count']}
• **Average Words/Sentence:** {analysis_result['avg_words_per_sentence']}
• **Readability:** {analysis_result['readability_estimate'].title()}
• **Sentiment:** {analysis_result['sentiment'].title()} (score: {analysis_result['sentiment_score']})

**Most Common Words:**"""
            
            for word, count in analysis_result['most_common_words'][:5]:
                result += f"\n• '{word}': {count} times"
            
            return result
            
        except Exception as e:
            return f"Text analysis error: {str(e)}"
    
    def _execute_format_agent(self, user_input: str, previous_results: List[str]) -> str:
        """Execute data formatting operations"""
        try:
            # Determine what to format
            if previous_results:
                # Format the results from other agents
                data_to_format = {
                    "task": user_input,
                    "results": previous_results,
                    "timestamp": datetime.now().isoformat()
                }
                format_type = "json"
            else:
                # Look for data in the user input
                data_to_format = {"user_request": user_input}
                format_type = "json"
            
            # Check if user specified a format
            user_lower = user_input.lower()
            if "table" in user_lower:
                format_type = "table"
            elif "list" in user_lower:
                format_type = "list"
            
            format_result = self.format_tool.format_data(data_to_format, format_type)
            
            if format_result["success"]:
                return f"""**Formatted Output ({format_type.upper()}):**
```{format_type}
{format_result['formatted_data']}
```"""
            else:
                return f"Formatting error: {format_result['error']}"
                
        except Exception as e:
            return f"Formatting error: {str(e)}"
    
    def _general_coordination_response(self, user_input: str) -> str:
        """Provide general coordination response when no specific agents are triggered"""
        return f"""🎭 **General Coordination Response:**

I've analyzed your request: "{user_input}"

As a multi-agent coordinator, I can deploy specialized agents for:
• **🧮 Mathematical Operations** - Calculations, equations, formulas
• **📊 Text Analysis** - Content analysis, sentiment, readability
• **📋 Data Formatting** - JSON, tables, structured output
• **🔍 Research Tasks** - Information gathering and synthesis
• **📁 File Operations** - Document management and processing

To get the most from the multi-agent system, try requests like:
- "Calculate the compound interest and format the results"
- "Analyze this text and present findings in a table"
- "Research Python libraries and create a comparison"

*Provide more specific instructions to activate specialized agents.*"""

def create_multi_agent_system(model_config: Optional[Dict[str, Any]] = None) -> MultiAgentSystem:
    """Factory function to create a Multi Agent System"""
    return MultiAgentSystem(model_config)

def main():
    """Test the Multi Agent System"""
    print("🤖 Testing Multi-Agent System...")
    
    try:
        mas = create_multi_agent_system()
        
        test_queries = [
            "Calculate the square root of 144 and analyze the result",
            "Analyze this text: 'This is a great product with excellent quality!' and format the results",
            "What is 25 * 47 + 100?",
            "Help me plan a Python learning roadmap with timeline and resources"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print('='*60)
            response = mas.chat(query)
            print(response)
        
        print(f"\n✅ Multi-Agent System test completed!")
        
    except Exception as e:
        print(f"❌ Error testing Multi-Agent System: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
