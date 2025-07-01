#!/usr/bin/env python3
"""
Real User Scenario Testing for Strands SDK Agents
Simulates realistic user interactions and workflows
"""

import sys
import time
import json
import random
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class UserScenarioTester:
    """Simulates real user scenarios with the Streamlit UI"""
    
    def __init__(self):
        self.project_root = project_root
        self.user_personas = self._create_user_personas()
        self.scenarios = self._create_user_scenarios()
    
    def _create_user_personas(self) -> Dict[str, Dict]:
        """Create different user personas for testing"""
        return {
            "Developer": {
                "description": "Software developer exploring AI agents",
                "interests": ["programming", "automation", "tools", "efficiency"],
                "typical_questions": [
                    "Can you help me with code?",
                    "What programming tools do you have?",
                    "How can I automate my workflow?"
                ]
            },
            "Researcher": {
                "description": "Academic researcher needing information",
                "interests": ["research", "data", "analysis", "information"],
                "typical_questions": [
                    "Find information about recent studies",
                    "Help me analyze this data",
                    "What are the latest developments in AI?"
                ]
            },
            "Business User": {
                "description": "Business professional seeking efficiency",
                "interests": ["productivity", "reports", "analysis", "automation"],
                "typical_questions": [
                    "Help me create a report",
                    "Analyze these business metrics",
                    "What tools can improve productivity?"
                ]
            },
            "Student": {
                "description": "Student learning about AI and technology",
                "interests": ["learning", "education", "examples", "explanations"],
                "typical_questions": [
                    "Explain how this works",
                    "Give me examples",
                    "Help me understand AI agents"
                ]
            },
            "Curious Explorer": {
                "description": "General user exploring AI capabilities",
                "interests": ["exploration", "capabilities", "fun", "creativity"],
                "typical_questions": [
                    "What can you do?",
                    "Show me something interesting",
                    "How do AI agents work?"
                ]
            }
        }
    
    def _create_user_scenarios(self) -> Dict[str, List[Dict]]:
        """Create realistic user scenarios for each agent"""
        return {
            "Simple Agent": [
                {
                    "scenario": "First Time User",
                    "persona": "Curious Explorer",
                    "conversation": [
                        "Hello, I'm new here. What is this?",
                        "What can you help me with?",
                        "Are you a real AI?",
                        "Thank you for the explanation!"
                    ]
                },
                {
                    "scenario": "Quick Question",
                    "persona": "Student",
                    "conversation": [
                        "Hi, I have a quick question",
                        "Can you explain what an AI agent is?",
                        "That's helpful, thanks!"
                    ]
                }
            ],
            
            "Agent with Tools": [
                {
                    "scenario": "Math Help",
                    "persona": "Student",
                    "conversation": [
                        "I need help with some calculations",
                        "What's 15% of 240?",
                        "Can you calculate the square root of 169?",
                        "What's 2 to the power of 10?"
                    ]
                },
                {
                    "scenario": "Research Assistant",
                    "persona": "Researcher",
                    "conversation": [
                        "I need to find some information",
                        "Search for recent AI developments",
                        "What's the weather like for my research trip to Boston?",
                        "Thanks for the help!"
                    ]
                }
            ],
            
            "Custom Tool Agent": [
                {
                    "scenario": "Text Analysis",
                    "persona": "Developer",
                    "conversation": [
                        "I need to analyze some text",
                        "Analyze this: 'Machine learning is transforming industries'",
                        "Can you generate a hash for security purposes?",
                        "What other custom tools do you have?"
                    ]
                },
                {
                    "scenario": "Data Processing",
                    "persona": "Business User",
                    "conversation": [
                        "I have some data to process",
                        "Can you help with text analysis?",
                        "Process this customer feedback: 'Great service, very satisfied'",
                        "This is very useful for my work!"
                    ]
                }
            ],
            
            "Web Research Agent": [
                {
                    "scenario": "Academic Research",
                    "persona": "Researcher",
                    "conversation": [
                        "I'm working on a research project",
                        "Find information about sustainable energy solutions",
                        "What are the latest trends in renewable energy?",
                        "Can you research climate change mitigation strategies?"
                    ]
                },
                {
                    "scenario": "Market Research",
                    "persona": "Business User",
                    "conversation": [
                        "I need market research help",
                        "Research the current state of AI in healthcare",
                        "What are competitors doing in this space?",
                        "Find trends in digital transformation"
                    ]
                }
            ],
            
            "File Manager Agent": [
                {
                    "scenario": "Project Organization",
                    "persona": "Developer",
                    "conversation": [
                        "I need help organizing my project files",
                        "Show me the current project structure",
                        "What files are in the docs directory?",
                        "Can you help me understand the file organization?"
                    ]
                },
                {
                    "scenario": "File Operations",
                    "persona": "Business User",
                    "conversation": [
                        "I need to manage some files",
                        "List the files in the current directory",
                        "What file operations can you perform?",
                        "This will help with my document management"
                    ]
                }
            ],
            
            "Multi Agent System": [
                {
                    "scenario": "Complex Task",
                    "persona": "Researcher",
                    "conversation": [
                        "I have a complex task that needs multiple capabilities",
                        "I need both calculations and research for my project",
                        "Can different agents work together on this?",
                        "Show me how agent collaboration works"
                    ]
                },
                {
                    "scenario": "Workflow Automation",
                    "persona": "Developer",
                    "conversation": [
                        "I want to automate a complex workflow",
                        "How can multiple agents coordinate?",
                        "What agents are available in the system?",
                        "This could revolutionize my development process!"
                    ]
                }
            ]
        }
    
    def simulate_user_session(self, agent_name: str, scenario: Dict) -> Dict[str, Any]:
        """Simulate a complete user session with an agent"""
        print(f"\n👤 Simulating User Session")
        print(f"   Agent: {agent_name}")
        print(f"   Scenario: {scenario['scenario']}")
        print(f"   Persona: {scenario['persona']}")
        print("-" * 50)
        
        try:
            from ui.agent_runner import AgentRunner
            
            agent_runner = AgentRunner(str(self.project_root))
            model_config = {
                "provider": "bedrock",
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            session_result = {
                "agent_name": agent_name,
                "scenario": scenario['scenario'],
                "persona": scenario['persona'],
                "conversation": [],
                "success": True,
                "total_exchanges": len(scenario['conversation']),
                "successful_exchanges": 0,
                "session_quality_score": 0.0
            }
            
            persona_info = self.user_personas[scenario['persona']]
            print(f"👤 User Profile: {persona_info['description']}")
            
            for i, user_message in enumerate(scenario['conversation'], 1):
                print(f"\n💬 Exchange {i}/{len(scenario['conversation'])}")
                print(f"   User: {user_message}")
                
                try:
                    # Add some realistic delay
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    response = agent_runner.run_agent(agent_name, model_config, user_message)
                    
                    # Evaluate response quality
                    quality_score = self._evaluate_response_quality(
                        user_message, response, persona_info
                    )
                    
                    exchange_result = {
                        "exchange_number": i,
                        "user_message": user_message,
                        "agent_response": response,
                        "response_length": len(response),
                        "quality_score": quality_score,
                        "success": quality_score >= 0.5
                    }
                    
                    session_result["conversation"].append(exchange_result)
                    
                    if exchange_result["success"]:
                        session_result["successful_exchanges"] += 1
                    
                    print(f"   Agent: {response[:100]}...")
                    print(f"   Quality: {quality_score:.1f}/1.0 {'✅' if quality_score >= 0.5 else '❌'}")
                    
                except Exception as e:
                    exchange_result = {
                        "exchange_number": i,
                        "user_message": user_message,
                        "error": str(e),
                        "success": False,
                        "quality_score": 0.0
                    }
                    session_result["conversation"].append(exchange_result)
                    session_result["success"] = False
                    print(f"   ❌ Error: {e}")
            
            # Calculate overall session quality
            if session_result["conversation"]:
                avg_quality = sum(ex.get("quality_score", 0) for ex in session_result["conversation"]) / len(session_result["conversation"])
                session_result["session_quality_score"] = avg_quality
            
            success_rate = session_result["successful_exchanges"] / session_result["total_exchanges"]
            
            print(f"\n📊 Session Summary:")
            print(f"   Successful Exchanges: {session_result['successful_exchanges']}/{session_result['total_exchanges']}")
            print(f"   Success Rate: {success_rate:.1%}")
            print(f"   Quality Score: {session_result['session_quality_score']:.2f}/1.0")
            
            return session_result
            
        except Exception as e:
            print(f"❌ Session setup error: {e}")
            return {
                "agent_name": agent_name,
                "scenario": scenario['scenario'],
                "error": str(e),
                "success": False
            }
    
    def _evaluate_response_quality(self, user_message: str, response: str, persona_info: Dict) -> float:
        """Evaluate the quality of an agent response"""
        score = 0.0
        
        # Basic response quality checks
        if len(response) > 20:
            score += 0.2  # Has substantial content
        
        if len(response) > 100:
            score += 0.2  # Detailed response
        
        # Check for persona-relevant keywords
        user_interests = persona_info.get("interests", [])
        response_lower = response.lower()
        user_message_lower = user_message.lower()
        
        # Relevance to user interests
        relevant_keywords = sum(1 for interest in user_interests if interest in response_lower)
        if relevant_keywords > 0:
            score += 0.2
        
        # Response appropriateness
        if any(word in response_lower for word in ["help", "assist", "can", "will", "happy"]):
            score += 0.2  # Helpful tone
        
        # Context awareness
        if any(word in user_message_lower for word in ["thank", "thanks"]) and any(word in response_lower for word in ["welcome", "pleasure", "glad"]):
            score += 0.2  # Appropriate response to thanks
        
        return min(score, 1.0)  # Cap at 1.0

def run_user_scenario_tests():
    """Run comprehensive user scenario tests"""
    print("🎭 USER SCENARIO TESTING SUITE")
    print("=" * 60)
    print("Simulating realistic user interactions with all agents")
    print("Testing different user personas and conversation flows")
    print("=" * 60)
    
    tester = UserScenarioTester()
    all_results = {}
    
    # Run scenarios for each agent
    for agent_name, scenarios in tester.scenarios.items():
        print(f"\n🤖 Testing {agent_name}")
        print("=" * 40)
        
        agent_results = []
        
        for scenario in scenarios:
            session_result = tester.simulate_user_session(agent_name, scenario)
            agent_results.append(session_result)
        
        all_results[agent_name] = agent_results
    
    # Generate comprehensive report
    print("\n" + "=" * 80)
    print("🎭 USER SCENARIO TEST RESULTS")
    print("=" * 80)
    
    total_sessions = 0
    successful_sessions = 0
    total_quality_score = 0.0
    
    for agent_name, sessions in all_results.items():
        agent_successful = sum(1 for s in sessions if s.get("success", False))
        agent_total = len(sessions)
        agent_avg_quality = sum(s.get("session_quality_score", 0) for s in sessions) / agent_total if agent_total > 0 else 0
        
        total_sessions += agent_total
        successful_sessions += agent_successful
        total_quality_score += agent_avg_quality * agent_total
        
        success_rate = agent_successful / agent_total if agent_total > 0 else 0
        
        status = "🎉 EXCELLENT" if success_rate >= 0.8 and agent_avg_quality >= 0.7 else \
                "✅ GOOD" if success_rate >= 0.6 and agent_avg_quality >= 0.5 else \
                "⚠️ FAIR" if success_rate >= 0.4 else "❌ POOR"
        
        print(f"{status} {agent_name}:")
        print(f"   Sessions: {agent_successful}/{agent_total} successful ({success_rate:.1%})")
        print(f"   Quality: {agent_avg_quality:.2f}/1.0")
        
        # Show scenario details
        for session in sessions:
            scenario_status = "✅" if session.get("success", False) else "❌"
            quality = session.get("session_quality_score", 0)
            print(f"     {scenario_status} {session.get('scenario', 'Unknown')}: {quality:.2f}")
    
    overall_success_rate = successful_sessions / total_sessions if total_sessions > 0 else 0
    overall_quality = total_quality_score / total_sessions if total_sessions > 0 else 0
    
    print(f"\n🎯 OVERALL USER EXPERIENCE:")
    print(f"   Total Sessions: {total_sessions}")
    print(f"   Success Rate: {overall_success_rate:.1%}")
    print(f"   Average Quality: {overall_quality:.2f}/1.0")
    
    if overall_success_rate >= 0.8 and overall_quality >= 0.7:
        print("🎉 OUTSTANDING! Users will have an excellent experience")
    elif overall_success_rate >= 0.6 and overall_quality >= 0.5:
        print("✅ GOOD! Users will have a positive experience")
    elif overall_success_rate >= 0.4:
        print("⚠️ FAIR! User experience needs improvement")
    else:
        print("❌ POOR! Significant improvements needed for user satisfaction")
    
    # Save detailed results
    results_file = project_root / "tests" / "user_scenario_results.json"
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    return all_results

if __name__ == "__main__":
    run_user_scenario_tests()
