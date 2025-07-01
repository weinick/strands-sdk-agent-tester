"""
Custom Tool Agent - Agent with specialized custom tools
Demonstrates custom tool creation with Strands SDK
"""

import os
import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
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

class TextAnalyzerTool:
    """Custom tool for text analysis"""
    
    @staticmethod
    def analyze_text(text: str) -> str:
        """Analyze text for various metrics"""
        try:
            # Basic metrics
            char_count = len(text)
            word_count = len(text.split())
            sentence_count = len([s for s in text.split('.') if s.strip()])
            paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
            
            # Word frequency
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Top 5 most common words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Reading time estimate (average 200 words per minute)
            reading_time = max(1, word_count // 200)
            
            result = f"""📊 **Text Analysis Results:**

**Basic Metrics:**
• Characters: {char_count:,}
• Words: {word_count:,}
• Sentences: {sentence_count}
• Paragraphs: {paragraph_count}
• Estimated reading time: {reading_time} minute(s)

**Most Common Words:**"""
            
            for word, count in top_words:
                result += f"\n• '{word}': {count} times"
            
            # Text complexity indicators
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            result += f"""

**Complexity Indicators:**
• Average word length: {avg_word_length:.1f} characters
• Average sentence length: {avg_sentence_length:.1f} words
• Vocabulary diversity: {len(word_freq)}/{word_count} ({len(word_freq)/word_count*100:.1f}%)"""
            
            return result
            
        except Exception as e:
            return f"❌ Text analysis error: {str(e)}"
    
    @staticmethod
    def extract_keywords(text: str, count: int = 10) -> str:
        """Extract keywords from text"""
        try:
            # Simple keyword extraction (in real implementation, use NLP libraries)
            words = re.findall(r'\b\w{4,}\b', text.lower())  # Words with 4+ characters
            
            # Remove common stop words
            stop_words = {'that', 'this', 'with', 'have', 'will', 'from', 'they', 'been', 
                         'were', 'said', 'each', 'which', 'their', 'time', 'would', 'there',
                         'could', 'other', 'more', 'very', 'what', 'know', 'just', 'first',
                         'into', 'over', 'think', 'also', 'your', 'work', 'life', 'only',
                         'can', 'still', 'should', 'after', 'being', 'now', 'made', 'before'}
            
            filtered_words = [word for word in words if word not in stop_words]
            
            # Count frequency
            word_freq = {}
            for word in filtered_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:count]
            
            result = f"🔑 **Top {len(keywords)} Keywords:**\n"
            for i, (word, freq) in enumerate(keywords, 1):
                result += f"{i}. **{word}** (appears {freq} times)\n"
            
            return result
            
        except Exception as e:
            return f"❌ Keyword extraction error: {str(e)}"

class DataProcessorTool:
    """Custom tool for data processing"""
    
    @staticmethod
    def process_csv_data(data: str) -> str:
        """Process CSV-like data"""
        try:
            lines = data.strip().split('\n')
            if len(lines) < 2:
                return "❌ Need at least header and one data row"
            
            # Parse header
            header = [col.strip() for col in lines[0].split(',')]
            
            # Parse data rows
            rows = []
            for line in lines[1:]:
                row = [cell.strip() for cell in line.split(',')]
                if len(row) == len(header):
                    rows.append(row)
            
            result = f"""📈 **CSV Data Analysis:**

**Structure:**
• Columns: {len(header)}
• Rows: {len(rows)}
• Total cells: {len(header) * len(rows)}

**Columns:**"""
            
            for i, col in enumerate(header, 1):
                result += f"\n{i}. {col}"
            
            # Try to identify numeric columns
            numeric_cols = []
            for col_idx, col_name in enumerate(header):
                numeric_count = 0
                for row in rows:
                    try:
                        float(row[col_idx])
                        numeric_count += 1
                    except ValueError:
                        pass
                
                if numeric_count > len(rows) * 0.7:  # 70% numeric
                    numeric_cols.append((col_name, col_idx))
            
            if numeric_cols:
                result += f"\n\n**Numeric Columns Detected:**"
                for col_name, col_idx in numeric_cols:
                    values = []
                    for row in rows:
                        try:
                            values.append(float(row[col_idx]))
                        except ValueError:
                            pass
                    
                    if values:
                        avg_val = sum(values) / len(values)
                        min_val = min(values)
                        max_val = max(values)
                        result += f"\n• **{col_name}**: Avg={avg_val:.2f}, Min={min_val}, Max={max_val}"
            
            return result
            
        except Exception as e:
            return f"❌ CSV processing error: {str(e)}"
    
    @staticmethod
    def generate_summary_stats(numbers: List[float]) -> str:
        """Generate summary statistics for a list of numbers"""
        try:
            if not numbers:
                return "❌ No numbers provided"
            
            n = len(numbers)
            total = sum(numbers)
            mean = total / n
            
            # Sort for median and quartiles
            sorted_nums = sorted(numbers)
            
            # Median
            if n % 2 == 0:
                median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
            else:
                median = sorted_nums[n//2]
            
            # Variance and standard deviation
            variance = sum((x - mean) ** 2 for x in numbers) / n
            std_dev = variance ** 0.5
            
            # Range
            min_val = min(numbers)
            max_val = max(numbers)
            range_val = max_val - min_val
            
            return f"""📊 **Summary Statistics:**

**Basic Stats:**
• Count: {n}
• Sum: {total:.2f}
• Mean: {mean:.2f}
• Median: {median:.2f}

**Spread:**
• Min: {min_val:.2f}
• Max: {max_val:.2f}
• Range: {range_val:.2f}
• Standard Deviation: {std_dev:.2f}
• Variance: {variance:.2f}"""
            
        except Exception as e:
            return f"❌ Statistics error: {str(e)}"

class CodeAnalyzerTool:
    """Custom tool for code analysis"""
    
    @staticmethod
    def analyze_code(code: str, language: str = "python") -> str:
        """Analyze code structure and complexity"""
        try:
            lines = code.split('\n')
            total_lines = len(lines)
            code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            comment_lines = len([line for line in lines if line.strip().startswith('#')])
            blank_lines = total_lines - code_lines - comment_lines
            
            result = f"""💻 **Code Analysis ({language.title()}):**

**Line Counts:**
• Total lines: {total_lines}
• Code lines: {code_lines}
• Comment lines: {comment_lines}
• Blank lines: {blank_lines}
• Comment ratio: {comment_lines/total_lines*100:.1f}%"""
            
            if language.lower() == "python":
                # Python-specific analysis
                functions = len(re.findall(r'^\s*def\s+\w+', code, re.MULTILINE))
                classes = len(re.findall(r'^\s*class\s+\w+', code, re.MULTILINE))
                imports = len(re.findall(r'^\s*(import|from)\s+', code, re.MULTILINE))
                
                result += f"""

**Python Structure:**
• Functions: {functions}
• Classes: {classes}
• Import statements: {imports}"""
                
                # Check for common patterns
                if 'if __name__ == "__main__"' in code:
                    result += "\n• ✅ Has main guard"
                if 'try:' in code:
                    result += "\n• ✅ Uses exception handling"
                if 'def __init__' in code:
                    result += "\n• ✅ Has class constructors"
            
            # General complexity indicators
            indentation_levels = []
            for line in lines:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    indentation_levels.append(indent)
            
            if indentation_levels:
                max_indent = max(indentation_levels)
                avg_indent = sum(indentation_levels) / len(indentation_levels)
                result += f"""

**Complexity Indicators:**
• Maximum nesting level: {max_indent // 4} (assuming 4-space indents)
• Average indentation: {avg_indent:.1f} spaces"""
            
            return result
            
        except Exception as e:
            return f"❌ Code analysis error: {str(e)}"

class HashGeneratorTool:
    """Custom tool for generating hashes and checksums"""
    
    @staticmethod
    def generate_hashes(text: str) -> str:
        """Generate various hashes for input text"""
        try:
            text_bytes = text.encode('utf-8')
            
            # Generate different hash types
            md5_hash = hashlib.md5(text_bytes).hexdigest()
            sha1_hash = hashlib.sha1(text_bytes).hexdigest()
            sha256_hash = hashlib.sha256(text_bytes).hexdigest()
            
            return f"""🔐 **Hash Generation Results:**

**Input:** "{text[:50]}{'...' if len(text) > 50 else ''}"
**Length:** {len(text)} characters

**Hashes:**
• **MD5:** `{md5_hash}`
• **SHA1:** `{sha1_hash}`
• **SHA256:** `{sha256_hash}`

**Use Cases:**
• MD5: Quick checksums (not cryptographically secure)
• SHA1: Legacy systems (deprecated for security)
• SHA256: Secure hashing, digital signatures"""
            
        except Exception as e:
            return f"❌ Hash generation error: {str(e)}"

class CustomToolAgent:
    """
    Agent with specialized custom tools for advanced tasks
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the custom tool agent"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        self.conversation_history = []
        self.bedrock_client = None
        
        # Initialize custom tools
        self.text_analyzer = TextAnalyzerTool()
        self.data_processor = DataProcessorTool()
        self.code_analyzer = CodeAnalyzerTool()
        self.hash_generator = HashGeneratorTool()
        
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
        """Process user input and determine appropriate custom tool usage"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Check for custom tool usage
            tool_response = self._check_and_use_custom_tools(user_input)
            
            if tool_response:
                response = tool_response
            else:
                # Generate conversational response
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
    
    def _check_and_use_custom_tools(self, user_input: str) -> Optional[str]:
        """Check for custom tool usage patterns"""
        user_lower = user_input.lower()
        
        # Text analysis triggers
        if any(phrase in user_lower for phrase in ['analyze text', 'text analysis', 'analyze this text']):
            # Extract text to analyze (simple approach)
            if '"' in user_input:
                # Text in quotes
                text_match = re.search(r'"([^"]*)"', user_input)
                if text_match:
                    return self.text_analyzer.analyze_text(text_match.group(1))
            elif 'analyze:' in user_lower:
                text = user_input.split('analyze:', 1)[1].strip()
                return self.text_analyzer.analyze_text(text)
            return "📊 Please provide text to analyze. Use quotes or 'analyze: your text here'"
        
        # Keyword extraction
        elif any(phrase in user_lower for phrase in ['extract keywords', 'find keywords', 'keywords from']):
            if '"' in user_input:
                text_match = re.search(r'"([^"]*)"', user_input)
                if text_match:
                    return self.text_analyzer.extract_keywords(text_match.group(1))
            return "🔑 Please provide text in quotes for keyword extraction"
        
        # CSV data processing
        elif any(phrase in user_lower for phrase in ['process csv', 'analyze csv', 'csv data']):
            # Look for CSV-like data in the input
            lines = user_input.split('\n')
            csv_lines = [line for line in lines if ',' in line]
            if len(csv_lines) >= 2:
                csv_data = '\n'.join(csv_lines)
                return self.data_processor.process_csv_data(csv_data)
            return "📈 Please provide CSV data with headers and at least one row"
        
        # Statistics generation
        elif any(phrase in user_lower for phrase in ['statistics for', 'stats for', 'summarize numbers']):
            # Extract numbers from input
            numbers = re.findall(r'-?\d+\.?\d*', user_input)
            if numbers:
                float_numbers = [float(n) for n in numbers]
                return self.data_processor.generate_summary_stats(float_numbers)
            return "📊 Please provide numbers for statistical analysis"
        
        # Code analysis
        elif any(phrase in user_lower for phrase in ['analyze code', 'code analysis', 'review code']):
            # Look for code blocks or code after keywords
            if '```' in user_input:
                # Code in markdown blocks
                code_match = re.search(r'```(?:python|py)?\n(.*?)\n```', user_input, re.DOTALL)
                if code_match:
                    return self.code_analyzer.analyze_code(code_match.group(1), "python")
            elif 'def ' in user_input or 'class ' in user_input:
                # Looks like Python code
                return self.code_analyzer.analyze_code(user_input, "python")
            return "💻 Please provide code to analyze (use ```code``` blocks or include actual code)"
        
        # Hash generation
        elif any(phrase in user_lower for phrase in ['generate hash', 'hash of', 'checksum']):
            # Extract text to hash
            if '"' in user_input:
                text_match = re.search(r'"([^"]*)"', user_input)
                if text_match:
                    return self.hash_generator.generate_hashes(text_match.group(1))
            elif 'hash:' in user_lower:
                text = user_input.split('hash:', 1)[1].strip()
                return self.hash_generator.generate_hashes(text)
            return "🔐 Please provide text to hash in quotes or use 'hash: your text'"
        
        return None
    
    def _call_bedrock(self, user_input: str) -> str:
        """Call AWS Bedrock for conversational responses"""
        try:
            system_message = """You are an AI assistant with specialized custom tools for:
- Text analysis and keyword extraction
- Data processing and statistical analysis  
- Code analysis and review
- Hash generation and checksums

When users need these specialized functions, I use the appropriate custom tools.
For general conversation, respond naturally and helpfully."""
            
            messages = [{"role": "user", "content": f"{system_message}\n\nUser: {user_input}"}]
            
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
            return """Hello! I'm a Custom Tool Agent with specialized capabilities.

My custom tools include:
📊 **Text Analyzer** - Analyze text metrics, extract keywords
📈 **Data Processor** - Process CSV data, generate statistics  
💻 **Code Analyzer** - Analyze code structure and complexity
🔐 **Hash Generator** - Generate MD5, SHA1, SHA256 hashes

**Try these commands:**
• "Analyze text: 'your text here'"
• "Extract keywords from 'your text'"
• "Process CSV data with headers"
• "Analyze code: ```your code```"
• "Generate hash of 'your text'"

How can I help you with specialized analysis today?"""
        
        elif any(word in user_lower for word in ['what can you do', 'capabilities', 'help', 'tools']):
            return """I'm a Custom Tool Agent with specialized analysis capabilities:

🔧 **Custom Tools Available:**

📊 **Text Analyzer:**
• Word count, character count, reading time
• Keyword extraction and frequency analysis
• Text complexity metrics
• Vocabulary diversity analysis

📈 **Data Processor:**
• CSV data analysis and structure detection
• Statistical summaries (mean, median, std dev)
• Numeric column identification
• Data quality assessment

💻 **Code Analyzer:**
• Line counting (code, comments, blank)
• Function and class detection
• Complexity analysis and nesting levels
• Python-specific pattern recognition

🔐 **Hash Generator:**
• MD5, SHA1, SHA256 hash generation
• Checksum creation for data integrity
• Security hash comparison

**Example Usage:**
• `analyze text: "Your sample text here"`
• `extract keywords from "text with important terms"`
• `process csv: header1,header2\nvalue1,value2`
• `analyze code: def hello(): print("world")`
• `generate hash of "text to hash"`

These tools are perfect for data analysis, content processing, and development tasks!"""
        
        elif any(word in user_lower for word in ['goodbye', 'bye', 'thanks']):
            return """You're welcome! I enjoyed helping you with custom tool analysis.

Remember my specialized capabilities:
📊 Text Analysis | 📈 Data Processing | 💻 Code Analysis | 🔐 Hash Generation

These custom tools make me perfect for:
• Content analysis and research
• Data processing and statistics
• Code review and quality assessment  
• Security and integrity verification

Come back anytime for specialized analysis tasks!

Goodbye! 🚀"""
        
        else:
            return f"""I received your message: "{user_input}"

As a Custom Tool Agent, I specialize in advanced analysis tasks. Here's what I can help you with:

🎯 **Specialized Analysis:**
• **Text Analysis**: Word counts, keywords, complexity metrics
• **Data Processing**: CSV analysis, statistical summaries
• **Code Analysis**: Structure analysis, complexity assessment
• **Hash Generation**: Security hashes and checksums

**Quick Examples:**
• Text: `analyze text: "sample text"`
• Data: `process csv:` followed by CSV data
• Code: `analyze code:` followed by code
• Hash: `generate hash of "sample"`

💬 **General Conversation:**
I also enjoy discussing topics related to:
• Data analysis techniques
• Text processing methods
• Code quality best practices
• Security and cryptography

**Current Configuration:**
- Provider: {self.model_config.get('provider', 'Mock')}
- Model: {self.model_config.get('model', 'Custom Tools Demo')}
- Specialized Tools: 4 custom analyzers

What kind of analysis would you like to explore?"""
    
    def get_available_tools(self) -> List[str]:
        """Get list of available custom tools"""
        return ["Text Analyzer", "Data Processor", "Code Analyzer", "Hash Generator"]
    
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
            "agent_type": "Custom Tool Agent",
            "model_config": self.model_config,
            "available_tools": self.get_available_tools(),
            "conversation_length": len(self.conversation_history),
            "bedrock_available": self.bedrock_client is not None,
            "status": "Ready"
        }

def create_custom_tool_agent(model_config: Optional[Dict[str, Any]] = None) -> CustomToolAgent:
    """Factory function to create a Custom Tool Agent"""
    return CustomToolAgent(model_config)

def main():
    """Main function for testing the agent directly"""
    print("🔧 Custom Tool Agent - Strands SDK Demo")
    print("=" * 50)
    
    # Create agent
    agent = create_custom_tool_agent()
    
    print("Agent initialized with custom tools:", agent.get_available_tools())
    print("Status:", agent.get_status())
    print("-" * 50)
    print("Try commands like:")
    print('• analyze text: "This is sample text to analyze"')
    print('• extract keywords from "machine learning artificial intelligence"')
    print('• generate hash of "hello world"')
    print("• Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAgent: Goodbye! Thanks for testing the Custom Tool Agent!")
                break
            
            if user_input:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thanks for testing the Custom Tool Agent!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
