#!/usr/bin/env python3
"""
Specialized UI Test Cases for Advanced Agents
Tests Web Research Agent, File Manager Agent, and Multi Agent System
"""

import sys
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class AdvancedAgentsUITester:
    """Specialized tester for advanced agents"""
    
    def __init__(self):
        self.project_root = project_root
        self.test_results = {}
    
    def test_web_research_agent(self) -> Dict[str, Any]:
        """Test Web Research Agent - Research and information gathering"""
        print("🔍 Testing Web Research Agent - Research Capabilities")
        print("-" * 50)
        
        test_cases = [
            {
                "category": "Technology Research",
                "message": "Research the latest developments in artificial intelligence",
                "expected_keywords": ["ai", "artificial intelligence", "research", "developments", "technology"]
            },
            {
                "category": "Scientific Research",
                "message": "Find information about climate change solutions",
                "expected_keywords": ["climate", "change", "solutions", "environment", "research"]
            },
            {
                "category": "Programming Research",
                "message": "What are the current trends in web development?",
                "expected_keywords": ["web", "development", "trends", "programming", "technology"]
            },
            {
                "category": "Comparative Research",
                "message": "Compare Python vs JavaScript for beginners",
                "expected_keywords": ["python", "javascript", "compare", "beginners", "programming"]
            },
            {
                "category": "Research Capabilities",
                "message": "What research capabilities do you have?",
                "expected_keywords": ["research", "capabilities", "search", "information", "web"]
            }
        ]
        
        return self._run_agent_tests("Web Research Agent", test_cases)
    
    def test_file_manager_agent(self) -> Dict[str, Any]:
        """Test File Manager Agent - File operations and management"""
        print("📂 Testing File Manager Agent - File Management Capabilities")
        print("-" * 50)
        
        test_cases = [
            {
                "category": "Directory Listing",
                "message": "List the files in the current directory",
                "expected_keywords": ["files", "directory", "list", "folder", "contents"]
            },
            {
                "category": "Project Structure",
                "message": "Show me the project structure",
                "expected_keywords": ["project", "structure", "folders", "files", "organization"]
            },
            {
                "category": "File Operations",
                "message": "What file operations can you perform?",
                "expected_keywords": ["file", "operations", "create", "read", "write", "delete"]
            },
            {
                "category": "Specific Folder",
                "message": "What's in the docs folder?",
                "expected_keywords": ["docs", "folder", "documentation", "files", "contents"]
            },
            {
                "category": "File Creation",
                "message": "Can you create a test file for me?",
                "expected_keywords": ["create", "file", "test", "write", "new"]
            }
        ]
        
        return self._run_agent_tests("File Manager Agent", test_cases)
    
    def test_multi_agent_system(self) -> Dict[str, Any]:
        """Test Multi Agent System - Agent coordination and collaboration"""
        print("🤝 Testing Multi Agent System - Collaboration Capabilities")
        print("-" * 50)
        
        test_cases = [
            {
                "category": "Agent Coordination",
                "message": "I need help with both calculations and research",
                "expected_keywords": ["calculations", "research", "help", "agents", "coordinate"]
            },
            {
                "category": "Multi-Agent Collaboration",
                "message": "Can you coordinate multiple agents to solve a problem?",
                "expected_keywords": ["coordinate", "multiple", "agents", "solve", "collaboration"]
            },
            {
                "category": "System Overview",
                "message": "Show me how agents work together",
                "expected_keywords": ["agents", "work", "together", "system", "collaboration"]
            },
            {
                "category": "Available Agents",
                "message": "What agents are available in the system?",
                "expected_keywords": ["agents", "available", "system", "list", "capabilities"]
            },
            {
                "category": "Complex Task",
                "message": "Help me analyze data and then research related topics",
                "expected_keywords": ["analyze", "data", "research", "topics", "help"]
            }
        ]
        
        return self._run_agent_tests("Multi Agent System", test_cases)
    
    def _run_agent_tests(self, agent_name: str, test_cases: List[Dict]) -> Dict[str, Any]:
        """Run tests for a specific advanced agent"""
        try:
            from ui.agent_runner import AgentRunner
            
            agent_runner = AgentRunner(str(self.project_root))
            model_config = {
                "provider": "bedrock",
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "temperature": 0.7,
                "max_tokens": 1500  # Higher token limit for advanced agents
            }
            
            results = {
                "agent_name": agent_name,
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "failed_tests": 0,
                "test_details": [],
                "success_rate": 0.0,
                "average_response_length": 0
            }
            
            total_response_length = 0
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n📝 Test {i}: {test_case['category']}")
                print(f"   Message: {test_case['message']}")
                
                try:
                    response = agent_runner.run_agent(agent_name, model_config, test_case['message'])
                    
                    # Advanced agents should provide more detailed responses
                    response_lower = response.lower()
                    found_keywords = [kw for kw in test_case['expected_keywords'] 
                                    if kw.lower() in response_lower]
                    
                    keyword_score = len(found_keywords) / len(test_case['expected_keywords'])
                    response_length = len(response)
                    total_response_length += response_length
                    
                    # Advanced agents need higher standards
                    test_passed = (keyword_score >= 0.4 and response_length > 100) or response_length > 200
                    
                    test_detail = {
                        "test_number": i,
                        "category": test_case['category'],
                        "message": test_case['message'],
                        "response": response,
                        "response_length": response_length,
                        "expected_keywords": test_case['expected_keywords'],
                        "found_keywords": found_keywords,
                        "keyword_score": keyword_score,
                        "passed": test_passed
                    }
                    
                    results["test_details"].append(test_detail)
                    
                    if test_passed:
                        results["passed_tests"] += 1
                        print(f"   ✅ PASS - Response: {response_length} chars, Keywords: {len(found_keywords)}/{len(test_case['expected_keywords'])}")
                    else:
                        results["failed_tests"] += 1
                        print(f"   ❌ FAIL - Response: {response_length} chars, Keywords: {len(found_keywords)}/{len(test_case['expected_keywords'])}")
                    
                    print(f"   📄 Preview: {response[:150]}...")
                    
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
                
                time.sleep(1)  # Longer delay for advanced agents
            
            results["success_rate"] = results["passed_tests"] / results["total_tests"]
            results["average_response_length"] = total_response_length / len(test_cases) if test_cases else 0
            
            print(f"\n📊 {agent_name} Test Summary:")
            print(f"   Total Tests: {results['total_tests']}")
            print(f"   Passed: {results['passed_tests']}")
            print(f"   Failed: {results['failed_tests']}")
            print(f"   Success Rate: {results['success_rate']:.1%}")
            print(f"   Avg Response Length: {results['average_response_length']:.0f} chars")
            
            return results
            
        except Exception as e:
            print(f"❌ Setup error for {agent_name}: {e}")
            return {
                "agent_name": agent_name,
                "error": str(e),
                "success_rate": 0.0
            }

def test_file_operations_safety():
    """Test file operations in a safe manner"""
    print("\n🔒 Testing File Operations Safety")
    print("-" * 40)
    
    # Create a safe test directory
    test_dir = project_root / "tests" / "temp_test_files"
    test_dir.mkdir(exist_ok=True)
    
    # Create some test files
    test_files = [
        "test_document.txt",
        "sample_data.json",
        "readme_test.md"
    ]
    
    for filename in test_files:
        test_file = test_dir / filename
        with open(test_file, 'w') as f:
            f.write(f"This is a test file: {filename}\nCreated for testing purposes.\n")
    
    print(f"✅ Created test directory: {test_dir}")
    print(f"✅ Created {len(test_files)} test files")
    
    return test_dir

def cleanup_test_files(test_dir: Path):
    """Clean up test files after testing"""
    try:
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print(f"🧹 Cleaned up test directory: {test_dir}")
    except Exception as e:
        print(f"⚠️ Could not clean up test directory: {e}")

def run_advanced_agents_tests():
    """Run all advanced agent tests"""
    print("🧪 ADVANCED AGENTS UI TESTING SUITE")
    print("=" * 60)
    print("Testing Web Research Agent, File Manager Agent, and Multi Agent System")
    print("=" * 60)
    
    # Setup test environment
    test_dir = test_file_operations_safety()
    
    tester = AdvancedAgentsUITester()
    all_results = {}
    
    # Test each advanced agent
    agents_to_test = [
        ("Web Research Agent", tester.test_web_research_agent),
        ("File Manager Agent", tester.test_file_manager_agent),
        ("Multi Agent System", tester.test_multi_agent_system)
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
    print("📊 ADVANCED AGENTS TEST SUMMARY")
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
            avg_length = result.get('average_response_length', 0)
            
            total_tests += total
            total_passed += passed
            
            status = "✅ EXCELLENT" if success_rate >= 0.8 else "✅ GOOD" if success_rate >= 0.6 else "⚠️ FAIR" if success_rate >= 0.4 else "❌ POOR"
            print(f"{status} {agent_name}: {success_rate:.1%} ({passed}/{total}) - Avg: {avg_length:.0f} chars")
    
    overall_success = total_passed / total_tests if total_tests > 0 else 0
    print(f"\n🎯 OVERALL ADVANCED AGENTS PERFORMANCE:")
    print(f"   Success Rate: {overall_success:.1%} ({total_passed}/{total_tests})")
    
    if overall_success >= 0.8:
        print("🎉 EXCELLENT! Advanced agents are performing very well")
    elif overall_success >= 0.6:
        print("✅ GOOD! Advanced agents are working well")
    elif overall_success >= 0.4:
        print("⚠️ FAIR! Advanced agents need some improvements")
    else:
        print("❌ POOR! Advanced agents need significant attention")
    
    # Save results
    results_file = project_root / "tests" / "advanced_agents_ui_results.json"
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n💾 Results saved to: {results_file}")
    
    # Cleanup
    cleanup_test_files(test_dir)
    
    return all_results

if __name__ == "__main__":
    run_advanced_agents_tests()
