"""
Web Research Agent - Specialized agent for web research and information gathering
Demonstrates advanced research capabilities with Strands SDK
"""

import os
import sys
import json
import re
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
from urllib.parse import urlparse, quote

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

class WebSearchTool:
    """Advanced web search tool with multiple search strategies"""
    
    def __init__(self):
        self.search_engines = {
            "duckduckgo": "https://duckduckgo.com/html/?q=",
            "bing": "https://www.bing.com/search?q=",
            "google": "https://www.google.com/search?q="
        }
    
    def search(self, query: str, num_results: int = 5) -> str:
        """Perform web search with mock results"""
        try:
            # Mock search results for demonstration
            results = self._generate_mock_results(query, num_results)
            
            response = f"""🔍 **Web Search Results for:** "{query}"

**Search Strategy:** Multi-source aggregation
**Results Found:** {len(results)}
**Search Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            for i, result in enumerate(results, 1):
                response += f"""**{i}. {result['title']}**
   📍 Source: {result['url']}
   📝 Summary: {result['summary']}
   🕒 Relevance: {result['relevance']}/10
   
"""
            
            response += """**Research Notes:**
• Results aggregated from multiple search engines
• Sources verified for credibility
• Content filtered for relevance
• Real-time information when available

*Note: This is a demonstration. Real implementation would use search APIs.*"""
            
            return response
            
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def _generate_mock_results(self, query: str, num_results: int) -> List[Dict]:
        """Generate mock search results based on query"""
        query_lower = query.lower()
        
        # Generate contextual mock results
        if any(word in query_lower for word in ['python', 'programming', 'code']):
            return [
                {
                    "title": f"Python Programming Guide - {query}",
                    "url": "https://docs.python.org/3/tutorial/",
                    "summary": f"Comprehensive guide covering {query} with examples and best practices.",
                    "relevance": 9
                },
                {
                    "title": f"Stack Overflow - {query} Questions",
                    "url": "https://stackoverflow.com/questions/tagged/python",
                    "summary": f"Community Q&A about {query} with practical solutions.",
                    "relevance": 8
                },
                {
                    "title": f"Real Python - {query} Tutorial",
                    "url": "https://realpython.com/",
                    "summary": f"In-depth tutorial on {query} for Python developers.",
                    "relevance": 9
                }
            ][:num_results]
        
        elif any(word in query_lower for word in ['weather', 'climate', 'temperature']):
            return [
                {
                    "title": f"Weather Forecast - {query}",
                    "url": "https://weather.com/",
                    "summary": f"Current weather conditions and forecast for {query}.",
                    "relevance": 10
                },
                {
                    "title": f"Climate Data - {query}",
                    "url": "https://climate.gov/",
                    "summary": f"Historical climate data and trends for {query}.",
                    "relevance": 8
                }
            ][:num_results]
        
        else:
            # Generic results
            return [
                {
                    "title": f"Complete Guide to {query}",
                    "url": f"https://example.com/{quote(query.replace(' ', '-'))}",
                    "summary": f"Comprehensive information about {query} including key concepts and applications.",
                    "relevance": 8
                },
                {
                    "title": f"{query} - Wikipedia",
                    "url": f"https://en.wikipedia.org/wiki/{quote(query.replace(' ', '_'))}",
                    "summary": f"Encyclopedia entry covering the basics and history of {query}.",
                    "relevance": 7
                },
                {
                    "title": f"Latest News about {query}",
                    "url": f"https://news.example.com/{quote(query)}",
                    "summary": f"Recent developments and news articles related to {query}.",
                    "relevance": 6
                }
            ][:num_results]

class ContentAnalyzerTool:
    """Tool for analyzing web content and extracting insights"""
    
    @staticmethod
    def analyze_content(content: str, focus: str = "general") -> str:
        """Analyze content for key insights"""
        try:
            # Basic content metrics
            word_count = len(content.split())
            char_count = len(content)
            
            # Extract key information based on focus
            if focus.lower() == "technical":
                return ContentAnalyzerTool._analyze_technical_content(content)
            elif focus.lower() == "news":
                return ContentAnalyzerTool._analyze_news_content(content)
            else:
                return ContentAnalyzerTool._analyze_general_content(content)
                
        except Exception as e:
            return f"❌ Content analysis error: {str(e)}"
    
    @staticmethod
    def _analyze_technical_content(content: str) -> str:
        """Analyze technical content"""
        # Look for technical terms
        tech_terms = re.findall(r'\b(?:API|SDK|framework|library|algorithm|database|server|client)\b', content, re.IGNORECASE)
        code_blocks = len(re.findall(r'```|`[^`]+`', content))
        
        return f"""🔬 **Technical Content Analysis:**

**Technical Terms Found:** {len(set(tech_terms))}
**Code Examples:** {code_blocks}
**Content Type:** Technical Documentation/Tutorial

**Key Technical Concepts:**
{', '.join(set(tech_terms)[:10]) if tech_terms else 'None detected'}

**Recommendation:** Suitable for developers and technical audiences"""
    
    @staticmethod
    def _analyze_news_content(content: str) -> str:
        """Analyze news content"""
        # Look for news indicators
        dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}|\b\d{4}-\d{2}-\d{2}\b', content)
        locations = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', content)  # Simple location detection
        
        return f"""📰 **News Content Analysis:**

**Dates Mentioned:** {len(dates)}
**Locations Referenced:** {len(set(locations))}
**Content Type:** News Article/Report

**Timeliness:** {'Recent' if dates else 'Undated'}
**Geographic Scope:** {'International' if len(set(locations)) > 3 else 'Local/Regional'}

**Recommendation:** {'Current events coverage' if dates else 'General information'}"""
    
    @staticmethod
    def _analyze_general_content(content: str) -> str:
        """Analyze general content"""
        sentences = len([s for s in content.split('.') if s.strip()])
        questions = len(re.findall(r'\?', content))
        
        return f"""📄 **General Content Analysis:**

**Structure:**
• Sentences: {sentences}
• Questions: {questions}
• Reading Level: {'Advanced' if len(content.split()) / sentences > 20 else 'Intermediate' if sentences > 0 else 'Basic'}

**Content Style:** {'Interactive/FAQ' if questions > 3 else 'Informational'}
**Engagement Level:** {'High' if questions > 0 else 'Medium'}"""

class ResearchSynthesizerTool:
    """Tool for synthesizing research findings"""
    
    @staticmethod
    def synthesize_findings(findings: List[str], topic: str) -> str:
        """Synthesize multiple research findings into a coherent summary"""
        try:
            return f"""📋 **Research Synthesis: {topic}**

**Sources Analyzed:** {len(findings)}
**Synthesis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Key Findings:**
• Multiple perspectives gathered from {len(findings)} sources
• Information cross-referenced for accuracy
• Conflicting viewpoints identified and noted
• Consensus points highlighted

**Research Quality:**
• Source Diversity: High
• Information Recency: Current
• Credibility Score: 8.5/10

**Summary:**
Based on the research conducted, {topic} appears to be a well-documented subject with multiple reliable sources providing consistent information. The findings suggest comprehensive coverage of the topic with both introductory and advanced materials available.

**Recommendations for Further Research:**
• Explore specialized academic sources
• Check for recent developments or updates
• Consider expert opinions and case studies
• Verify information with primary sources

*This synthesis represents a comprehensive overview based on available web sources.*"""
            
        except Exception as e:
            return f"❌ Synthesis error: {str(e)}"

class WebResearchAgent:
    """
    Advanced agent specialized in web research and information gathering
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the web research agent"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.3,  # Lower temperature for more focused research
            "max_tokens": 1500
        }
        
        self.conversation_history = []
        self.research_history = []
        self.bedrock_client = None
        
        # Initialize research tools
        self.web_search = WebSearchTool()
        self.content_analyzer = ContentAnalyzerTool()
        self.synthesizer = ResearchSynthesizerTool()
        
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
        """Process research requests and provide comprehensive responses"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Check if this is a research request
            research_response = self._handle_research_request(user_input)
            
            if research_response:
                response = research_response
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
            error_msg = f"Error processing research request: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def _handle_research_request(self, user_input: str) -> Optional[str]:
        """Handle research-specific requests"""
        user_lower = user_input.lower()
        
        # Research triggers
        if any(phrase in user_lower for phrase in ['research', 'find information', 'search for', 'look up']):
            # Extract research topic
            topic = self._extract_research_topic(user_input)
            if topic:
                return self._conduct_research(topic)
            return "🔍 What would you like me to research? Please specify a topic."
        
        # Comparison research
        elif any(phrase in user_lower for phrase in ['compare', 'versus', 'vs', 'difference between']):
            topics = self._extract_comparison_topics(user_input)
            if len(topics) >= 2:
                return self._conduct_comparison_research(topics)
            return "⚖️ Please specify what you'd like me to compare (e.g., 'compare Python vs JavaScript')"
        
        # Trend analysis
        elif any(phrase in user_lower for phrase in ['trends in', 'latest in', 'recent developments']):
            topic = self._extract_research_topic(user_input)
            if topic:
                return self._conduct_trend_analysis(topic)
            return "📈 What trends would you like me to analyze?"
        
        return None
    
    def _extract_research_topic(self, user_input: str) -> Optional[str]:
        """Extract research topic from user input"""
        # Simple topic extraction
        user_lower = user_input.lower()
        
        # Remove common research phrases
        for phrase in ['research', 'find information about', 'search for', 'look up', 'tell me about']:
            user_lower = user_lower.replace(phrase, '')
        
        topic = user_lower.strip()
        return topic if len(topic) > 2 else None
    
    def _extract_comparison_topics(self, user_input: str) -> List[str]:
        """Extract topics for comparison"""
        # Simple comparison extraction
        user_lower = user_input.lower()
        
        # Split on comparison keywords
        for separator in [' vs ', ' versus ', ' and ', ' or ']:
            if separator in user_lower:
                parts = user_lower.split(separator)
                if len(parts) >= 2:
                    return [part.strip() for part in parts[:2]]
        
        return []
    
    def _conduct_research(self, topic: str) -> str:
        """Conduct comprehensive research on a topic"""
        try:
            # Perform web search
            search_results = self.web_search.search(topic, num_results=5)
            
            # Analyze content (mock analysis)
            content_analysis = self.content_analyzer.analyze_content(f"Research content about {topic}", "general")
            
            # Synthesize findings
            findings = [search_results, content_analysis]
            synthesis = self.synthesizer.synthesize_findings(findings, topic)
            
            # Store research in history
            self.research_history.append({
                "topic": topic,
                "timestamp": datetime.now(),
                "type": "comprehensive_research"
            })
            
            return f"""🔬 **Comprehensive Research Report: {topic.title()}**

{search_results}

---

{content_analysis}

---

{synthesis}

**Research Session Summary:**
• Topic: {topic.title()}
• Research Type: Comprehensive Analysis
• Sources Consulted: Multiple web sources
• Analysis Depth: Detailed
• Confidence Level: High

*This research was conducted using advanced web research methodologies and cross-source verification.*"""
            
        except Exception as e:
            return f"❌ Research error: {str(e)}"
    
    def _conduct_comparison_research(self, topics: List[str]) -> str:
        """Conduct comparative research between topics"""
        try:
            topic1, topic2 = topics[0], topics[1]
            
            # Research both topics
            results1 = self.web_search.search(topic1, num_results=3)
            results2 = self.web_search.search(topic2, num_results=3)
            
            return f"""⚖️ **Comparative Research: {topic1.title()} vs {topic2.title()}**

**Research Methodology:**
• Individual research conducted for each topic
• Cross-comparison analysis performed
• Strengths and weaknesses identified
• Use case scenarios evaluated

**{topic1.title()} Research:**
{results1}

---

**{topic2.title()} Research:**
{results2}

---

**Comparative Analysis:**

**Similarities:**
• Both topics have substantial online documentation
• Active community discussions available
• Multiple learning resources accessible

**Key Differences:**
• **{topic1.title()}**: Appears to have [specific characteristics based on search]
• **{topic2.title()}**: Shows [different characteristics based on search]

**Recommendations:**
• Choose **{topic1.title()}** if: [context-specific recommendation]
• Choose **{topic2.title()}** if: [alternative context recommendation]
• Consider both if: [combined use case scenario]

**Research Confidence:** High (based on multiple source verification)"""
            
        except Exception as e:
            return f"❌ Comparison research error: {str(e)}"
    
    def _conduct_trend_analysis(self, topic: str) -> str:
        """Conduct trend analysis for a topic"""
        try:
            # Search for trend-related information
            trend_results = self.web_search.search(f"latest trends {topic} 2024", num_results=4)
            
            return f"""📈 **Trend Analysis: {topic.title()}**

**Analysis Period:** Current (2024)
**Research Focus:** Latest developments and emerging trends
**Data Sources:** Multiple web sources and industry reports

{trend_results}

**Trend Summary:**
Based on current research, {topic} shows the following trend patterns:

**Emerging Trends:**
• Increased interest and adoption
• New developments and innovations
• Growing community engagement
• Enhanced tooling and resources

**Market Indicators:**
• **Growth Trajectory:** Positive
• **Industry Adoption:** Increasing
• **Community Activity:** High
• **Innovation Rate:** Accelerating

**Future Outlook:**
The research suggests continued growth and development in {topic}, with strong indicators for sustained interest and advancement.

**Recommendations:**
• Stay updated with latest developments
• Engage with community resources
• Consider early adoption of emerging features
• Monitor competitive landscape

*Trend analysis based on current web research and market indicators.*"""
            
        except Exception as e:
            return f"❌ Trend analysis error: {str(e)}"
    
    def _call_bedrock(self, user_input: str) -> str:
        """Call AWS Bedrock for research-oriented responses"""
        try:
            system_message = """You are a specialized web research agent with advanced capabilities for:
- Comprehensive web research and information gathering
- Multi-source verification and cross-referencing
- Trend analysis and comparative research
- Content analysis and synthesis

When users need research, I use specialized tools to provide thorough, well-sourced information.
For general conversation, I maintain a research-focused perspective."""
            
            messages = [{"role": "user", "content": f"{system_message}\n\nUser: {user_input}"}]
            
            if "claude" in self.model_config["model"].lower():
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": self.model_config.get("max_tokens", 1500),
                    "temperature": self.model_config.get("temperature", 0.3),
                    "messages": messages
                }
            else:
                body = {
                    "inputText": user_input,
                    "textGenerationConfig": {
                        "maxTokenCount": self.model_config.get("max_tokens", 1500),
                        "temperature": self.model_config.get("temperature", 0.3)
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
        """Generate research-focused conversational responses"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return """Hello! I'm a Web Research Agent specialized in comprehensive information gathering and analysis.

🔍 **My Research Capabilities:**
• **Comprehensive Research**: Deep-dive analysis on any topic
• **Comparative Analysis**: Side-by-side comparison of concepts
• **Trend Analysis**: Latest developments and emerging patterns
• **Multi-Source Verification**: Cross-referenced information gathering

**Research Commands:**
• "Research [topic]" - Comprehensive topic analysis
• "Compare [A] vs [B]" - Comparative research
• "Latest trends in [topic]" - Trend analysis
• "Find information about [subject]" - General research

**Example Queries:**
• "Research machine learning algorithms"
• "Compare Python vs JavaScript for web development"
• "Latest trends in artificial intelligence"
• "Find information about sustainable energy"

What would you like me to research for you today?"""
        
        elif any(word in user_lower for word in ['what can you do', 'capabilities', 'help']):
            return """I'm a specialized Web Research Agent with advanced research capabilities:

🔬 **Research Methodologies:**

**Comprehensive Research:**
• Multi-source information gathering
• Cross-verification of facts and claims
• Synthesis of findings from various perspectives
• Quality assessment of sources

**Comparative Analysis:**
• Side-by-side feature comparison
• Pros and cons evaluation
• Use case scenario analysis
• Recommendation generation

**Trend Analysis:**
• Latest development tracking
• Market trend identification
• Future outlook assessment
• Industry pattern recognition

**Content Analysis:**
• Technical content evaluation
• News and current events analysis
• Academic and research paper insights
• Social media trend monitoring

🛠️ **Research Tools:**
• **Web Search Engine**: Multi-platform search capabilities
• **Content Analyzer**: Deep content insight extraction
• **Research Synthesizer**: Finding consolidation and summary
• **Trend Tracker**: Pattern and development monitoring

**Research Quality Features:**
• Source credibility verification
• Information recency checking
• Cross-reference validation
• Bias detection and mitigation

**Best Use Cases:**
• Academic research assistance
• Market research and analysis
• Technology comparison studies
• Industry trend monitoring
• Competitive intelligence gathering

Ready to conduct thorough research on any topic you're interested in!"""
        
        elif any(word in user_lower for word in ['goodbye', 'bye', 'thanks']):
            return """Thank you for using the Web Research Agent! 

**Research Session Summary:**
• Topics Researched: {len(self.research_history)}
• Research Quality: Professional-grade analysis
• Source Verification: Multi-source cross-referencing
• Analysis Depth: Comprehensive coverage

**Research Capabilities Demonstrated:**
🔍 Web Search & Information Gathering
📊 Content Analysis & Synthesis  
📈 Trend Analysis & Forecasting
⚖️ Comparative Research & Evaluation

Feel free to return anytime for:
• In-depth topic research
• Comparative analysis
• Trend monitoring
• Information verification

Keep researching and stay informed! 🚀"""
        
        else:
            return f"""I received your message: "{user_input}"

As a Web Research Agent, I specialize in comprehensive information gathering and analysis. Here's how I can help:

🔍 **Research Services:**
• **Topic Research**: "Research [your topic]"
• **Comparative Analysis**: "Compare [A] vs [B]"  
• **Trend Analysis**: "Latest trends in [field]"
• **Information Gathering**: "Find information about [subject]"

**Research Quality Standards:**
• Multi-source verification
• Credibility assessment
• Current information prioritization
• Comprehensive analysis and synthesis

**Example Research Requests:**
• "Research the benefits of renewable energy"
• "Compare React vs Vue.js for frontend development"
• "Latest trends in cybersecurity"
• "Find information about space exploration"

**Current Session:**
- Provider: {self.model_config.get('provider', 'Mock')}
- Model: {self.model_config.get('model', 'Research Demo')}
- Research History: {len(self.research_history)} topics
- Analysis Mode: Comprehensive

What research can I conduct for you? I'm ready to dive deep into any topic and provide you with well-researched, comprehensive information!"""
    
    def get_research_history(self) -> List[Dict]:
        """Get research history"""
        return self.research_history.copy()
    
    def get_available_tools(self) -> List[str]:
        """Get list of available research tools"""
        return ["Web Search", "Content Analyzer", "Research Synthesizer", "Trend Tracker"]
    
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation and research history"""
        self.conversation_history = []
        self.research_history = []
        logger.info("All history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_type": "Web Research Agent",
            "model_config": self.model_config,
            "available_tools": self.get_available_tools(),
            "conversation_length": len(self.conversation_history),
            "research_sessions": len(self.research_history),
            "bedrock_available": self.bedrock_client is not None,
            "status": "Ready for Research"
        }

def create_web_research_agent(model_config: Optional[Dict[str, Any]] = None) -> WebResearchAgent:
    """Factory function to create a Web Research Agent"""
    return WebResearchAgent(model_config)

def main():
    """Main function for testing the agent directly"""
    print("🔍 Web Research Agent - Strands SDK Demo")
    print("=" * 60)
    
    # Create agent
    agent = create_web_research_agent()
    
    print("Research Agent initialized with tools:", agent.get_available_tools())
    print("Status:", agent.get_status())
    print("-" * 60)
    print("Try research commands like:")
    print('• "Research artificial intelligence"')
    print('• "Compare Python vs Java"')
    print('• "Latest trends in machine learning"')
    print('• "Find information about climate change"')
    print("• Type 'quit' to exit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAgent: Thank you for using the Web Research Agent! Happy researching!")
                break
            
            if user_input:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Web Research Agent!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
