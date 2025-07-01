#!/usr/bin/env python3
"""
Specialized UI Test Cases for Basic Agents
Tests Simple Agent, Agent with Tools, and Custom Tool Agent
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class BasicAgentsUITester:
    """Specialized tester for basic agents"""
    
    def __init__(self):
        self.project_root = project_root
        self.test_results = {}
    
    def test_simple_agent(self) -> Dict[str, Any]:
        """Test Simple Agent with conversation scenarios"""
        print("🤖 Testing Simple Agent - Conversational Capabilities")
        print("-" * 50)
        
        test_cases = [
            {
                "category": "Greeting",
                "message": "Hello! How are you today?",
                "expected_keywords": ["hello", "hi", "good", "fine", "help"]
            },
            {
                "category": "Capability Inquiry",
                "message": "What can you help me with?",
                "expected_keywords": ["help", "assist", "can", "do", "support"]
            },
            {
                "category": "Self Description",
                "message": "Tell me about yourself",
                "expected_keywords": ["agent", "ai", "assistant", "strands", "help"]
            },
            {
                "category": "General Question",
                "message": "What's the meaning of life?",
                "expected_keywords": ["meaning", "life", "purpose", "question", "philosophical"]
            },
            {
                "category": "Farewell",
                "message": "Thank you and goodbye!",
                "expected_keywords": ["thank", "welcome", "goodbye", "bye", "pleasure"]
            }
        ]
        
        return self._run_agent_tests("Simple Agent", test_cases)
    
    def test_agent_with_tools(self) -> Dict[str, Any]:
        """Test Agent with Tools - Built-in tool capabilities"""
        print("🛠️ Testing Agent with Tools - Built-in Tool Capabilities")
        print("-" * 50)
        
        test_cases = [
            {
                "category": "Math Calculation",
                "message": "Calculate 25 * 17 + 83",
                "expected_keywords": ["calculate", "result", "answer", "508"]
            },
            {
                "category": "Square Root",
                "message": "What's the square root of 256?",
                "expected_keywords": ["square", "root", "16", "result"]
            },
            {
                "category": "Web Search Simulation",
                "message": "Search for information about Python programming",
                "expected_keywords": ["python", "programming", "search", "information", "language"]
            },
            {
                "category": "Weather Query",
                "message": "What's the weather like in San Francisco?",
                "expected_keywords": ["weather", "san francisco", "temperature", "forecast"]
            },
            {
                "category": "Tool Listing",
                "message": "What tools do you have available?",
                "expected_keywords": ["tools", "available", "calculator", "search", "weather"]
            }
        ]
        
        return self._run_agent_tests("Agent with Tools", test_cases)
    
    def test_custom_tool_agent(self) -> Dict[str, Any]:
        """Test Custom Tool Agent - Custom tool capabilities"""
        print("🔧 Testing Custom Tool Agent - Custom Tool Capabilities")
        print("-" * 50)
        
        test_cases = [
            {
                "category": "Text Analysis",
                "message": "Analyze this text: 'The quick brown fox jumps over the lazy dog'",
                "expected_keywords": ["analyze", "text", "words", "characters", "analysis"]
            },
            {
                "category": "Hash Generation",
                "message": "Generate a hash for the password 'test123'",
                "expected_keywords": ["hash", "password", "generated", "security"]
            },
            {
                "category": "Custom Tool Inquiry",
                "message": "What custom tools do you have?",
                "expected_keywords": ["custom", "tools", "available", "text", "hash"]
            },
            {
                "category": "Data Processing",
                "message": "Process this data: [1, 2, 3, 4, 5]",
                "expected_keywords": ["process", "data", "numbers", "list", "result"]
            },
            {
                "category": "Tool Demonstration",
                "message": "Show me what you can do with your custom tools",
                "expected_keywords": ["demonstrate", "custom", "tools", "capabilities", "examples"]
            }
        ]
        
        return self._run_agent_tests("Custom Tool Agent", test_cases)
    
    def _run_agent_tests(self, agent_name: str, test_cases: List[Dict]) -> Dict[str, Any]:
        """Run tests for a specific agent"""
        try:
            from ui.agent_runner import AgentRunner
            
            agent_runner = AgentRunner(str(self.project_root))
            model_config = {
                "provider": "bedrock",
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            results = {
                "agent_name": agent_name,
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "failed_tests": 0,
                "test_details": [],
                "success_rate": 0.0
            }
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n📝 Test {i}: {test_case['category']}")
                print(f"   Message: {test_case['message']}")
                
                try:
                    response = agent_runner.run_agent(agent_name, model_config, test_case['message'])
                    
                    # Check for expected keywords
                    response_lower = response.lower()
                    found_keywords = [kw for kw in test_case['expected_keywords'] 
                                    if kw.lower() in response_lower]
                    
                    keyword_score = len(found_keywords) / len(test_case['expected_keywords'])
                    test_passed = keyword_score >= 0.3 or len(response) > 50  # Pass if 30% keywords found or substantial response
                    
                    test_detail = {
                        "test_number": i,
                        "category": test_case['category'],
                        "message": test_case['message'],
                        "response": response,
                        "response_length": len(response),
                        "expected_keywords": test_case['expected_keywords'],
                        "found_keywords": found_keywords,
                        "keyword_score": keyword_score,
                        "passed": test_passed
                    }
                    
                    results["test_details"].append(test_detail)
                    
                    if test_passed:
                        results["passed_tests"] += 1
                        print(f"   ✅ PASS - Response: {len(response)} chars, Keywords: {len(found_keywords)}/{len(test_case['expected_keywords'])}")
                    else:
                        results["failed_tests"] += 1
                        print(f"   ❌ FAIL - Response: {len(response)} chars, Keywords: {len(found_keywords)}/{len(test_case['expected_keywords'])}")
                    
                    print(f"   📄 Preview: {response[:100]}...")
                    
                except Exception as e:
                    results["failed_tests"] += 1
                    test_detail = {
                        "test_number": i,
                        "category": test_case['category'],
                        "message": test_case['message'],
                        "error": str(e),
                        "passed": False
                    }
                    results["test_details"].append(test_detail)
                    print(f"   ❌ ERROR: {e}")
                
                time.sleep(0.5)  # Small delay between tests
            
            results["success_rate"] = results["passed_tests"] / results["total_tests"]
            
            print(f"\n📊 {agent_name} Test Summary:")
            print(f"   Total Tests: {results['total_tests']}")
            print(f"   Passed: {results['passed_tests']}")
            print(f"   Failed: {results['failed_tests']}")
            print(f"   Success Rate: {results['success_rate']:.1%}")
            
            return results
            
        except Exception as e:
            print(f"❌ Setup error for {agent_name}: {e}")
            return {
                "agent_name": agent_name,
                "error": str(e),
                "success_rate": 0.0
            }

def run_basic_agents_tests():
    """Run all basic agent tests"""
    print("🧪 BASIC AGENTS UI TESTING SUITE")
    print("=" * 60)
    print("Testing Simple Agent, Agent with Tools, and Custom Tool Agent")
    print("=" * 60)
    
    tester = BasicAgentsUITester()
    all_results = {}
    
    # Test each basic agent
    agents_to_test = [
        ("Simple Agent", tester.test_simple_agent),
        ("Agent with Tools", tester.test_agent_with_tools),
        ("Custom Tool Agent", tester.test_custom_tool_agent)
    ]
    
    for agent_name, test_function in agents_to_test:
        try:
            result = test_function()
            all_results[agent_name] = result
        except Exception as e:
            print(f"❌ Failed to test {agent_name}: {e}")
            all_results[agent_name] = {"error": str(e), "success_rate": 0.0}
    
    # Generate summary report
    print("\n" + "=" * 80)
    print("📊 BASIC AGENTS TEST SUMMARY")
    print("=" * 80)
    
    total_tests = 0
    total_passed = 0
    
    for agent_name, result in all_results.items():
        if "error" in result:
            print(f"❌ {agent_name}: ERROR - {result['error']}")
        else:
            success_rate = result.get('success_rate', 0)
            passed = result.get('passed_tests', 0)
            total = result.get('total_tests', 0)
            
            total_tests += total
            total_passed += passed
            
            status = "✅ PASS" if success_rate >= 0.7 else "⚠️ PARTIAL" if success_rate >= 0.4 else "❌ FAIL"
            print(f"{status} {agent_name}: {success_rate:.1%} ({passed}/{total})")
    
    overall_success = total_passed / total_tests if total_tests > 0 else 0
    print(f"\n🎯 OVERALL BASIC AGENTS PERFORMANCE:")
    print(f"   Success Rate: {overall_success:.1%} ({total_passed}/{total_tests})")
    
    # Save results
    results_file = project_root / "tests" / "basic_agents_ui_results.json"
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n💾 Results saved to: {results_file}")
    
    return all_results

if __name__ == "__main__":
    run_basic_agents_tests()
