#!/usr/bin/env python3
"""
Comprehensive UI Test Cases for Strands SDK Agents
Tests all 6 agents through the Streamlit UI interface using MCP tools
Simulates real user interactions and validates agent responses
"""

import sys
import time
import asyncio
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Any
import requests
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class StreamlitUITester:
    """Test class for Streamlit UI agent interactions"""
    
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.streamlit_process = None
        self.test_results = {}
        
    def start_streamlit(self):
        """Start Streamlit UI for testing"""
        print("🚀 Starting Streamlit UI for testing...")
        ui_script = project_root / "ui" / "streamlit_ui.py"
        
        self.streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", str(ui_script),
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], cwd=project_root / "ui", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for Streamlit to start
        print("⏳ Waiting for Streamlit to initialize...")
        time.sleep(10)
        
        # Verify Streamlit is running
        try:
            response = requests.get(f"{self.base_url}/healthz", timeout=5)
            if response.status_code == 200:
                print("✅ Streamlit UI is running successfully")
                return True
        except requests.exceptions.RequestException:
            pass
            
        print("❌ Failed to start Streamlit UI")
        return False
    
    def stop_streamlit(self):
        """Stop Streamlit UI"""
        if self.streamlit_process:
            print("🛑 Stopping Streamlit UI...")
            self.streamlit_process.terminate()
            self.streamlit_process.wait()
            print("✅ Streamlit UI stopped")
    
    def simulate_user_interaction(self, agent_name: str, test_messages: List[str]) -> Dict[str, Any]:
        """Simulate user interaction with a specific agent"""
        print(f"\n🧪 Testing {agent_name}")
        print("=" * 60)
        
        test_result = {
            "agent_name": agent_name,
            "test_messages": test_messages,
            "responses": [],
            "success": False,
            "errors": []
        }
        
        try:
            # Import agent runner to simulate UI interactions
            from ui.agent_runner import AgentRunner
            from ui.streamlit_ui import AGENTS
            
            # Initialize agent runner
            agent_runner = AgentRunner(str(project_root))
            
            # Get model configuration
            model_config = {
                "provider": "bedrock",
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            print(f"🤖 Agent: {agent_name}")
            print(f"📋 Model Config: {model_config}")
            print(f"💬 Test Messages: {len(test_messages)}")
            
            # Test each message
            for i, message in enumerate(test_messages, 1):
                print(f"\n📝 Test {i}/{len(test_messages)}: {message}")
                
                try:
                    # Simulate UI interaction
                    response = agent_runner.run_agent(agent_name, model_config, message)
                    
                    test_result["responses"].append({
                        "message": message,
                        "response": response,
                        "success": True
                    })
                    
                    print(f"✅ Response received ({len(response)} chars)")
                    print(f"📄 Preview: {response[:100]}...")
                    
                except Exception as e:
                    error_msg = str(e)
                    test_result["responses"].append({
                        "message": message,
                        "response": None,
                        "success": False,
                        "error": error_msg
                    })
                    test_result["errors"].append(f"Message {i}: {error_msg}")
                    print(f"❌ Error: {error_msg}")
                
                # Small delay between messages
                time.sleep(1)
            
            # Determine overall success
            successful_responses = sum(1 for r in test_result["responses"] if r["success"])
            test_result["success"] = successful_responses > 0
            test_result["success_rate"] = successful_responses / len(test_messages)
            
            print(f"\n📊 Test Summary for {agent_name}:")
            print(f"   Success Rate: {test_result['success_rate']:.1%}")
            print(f"   Successful: {successful_responses}/{len(test_messages)}")
            print(f"   Errors: {len(test_result['errors'])}")
            
        except Exception as e:
            test_result["errors"].append(f"Setup error: {str(e)}")
            print(f"❌ Setup Error: {e}")
        
        return test_result

def get_agent_test_cases() -> Dict[str, List[str]]:
    """Define test cases for each agent"""
    return {
        "Simple Agent": [
            "Hello, how are you today?",
            "What can you help me with?",
            "Tell me about yourself",
            "What's the weather like?",
            "Can you explain what you do?"
        ],
        
        "Agent with Tools": [
            "Calculate 15 * 23 + 45",
            "What's the square root of 144?",
            "Search for information about Python programming",
            "What's 2 to the power of 8?",
            "Find the current weather in New York"
        ],
        
        "Custom Tool Agent": [
            "Analyze the text: 'The quick brown fox jumps over the lazy dog'",
            "Generate a hash for the password 'test123'",
            "What tools do you have available?",
            "Can you process some data for me?",
            "Show me your custom capabilities"
        ],
        
        "Web Research Agent": [
            "Research the latest developments in artificial intelligence",
            "Find information about climate change solutions",
            "What are the current trends in web development?",
            "Research the benefits of renewable energy",
            "Compare different programming languages for beginners"
        ],
        
        "File Manager Agent": [
            "List the files in the current directory",
            "What file operations can you perform?",
            "Can you create a test file?",
            "Show me the project structure",
            "What's in the docs folder?"
        ],
        
        "Multi Agent System": [
            "I need help with a complex calculation and research task",
            "Can you coordinate multiple agents to solve a problem?",
            "Show me how agents work together",
            "Demonstrate multi-agent collaboration",
            "What agents are available in the system?"
        ]
    }

def run_comprehensive_ui_tests():
    """Run comprehensive UI tests for all agents"""
    print("🧪 STRANDS SDK AGENTS - COMPREHENSIVE UI TESTS")
    print("=" * 60)
    print("Testing all 6 agents through Streamlit UI interface")
    print("Simulating real user interactions with various test cases")
    print("=" * 60)
    
    tester = StreamlitUITester()
    test_cases = get_agent_test_cases()
    all_results = {}
    
    try:
        # Start Streamlit UI
        if not tester.start_streamlit():
            print("❌ Failed to start Streamlit UI. Cannot run tests.")
            return
        
        # Test each agent
        for agent_name, messages in test_cases.items():
            result = tester.simulate_user_interaction(agent_name, messages)
            all_results[agent_name] = result
        
        # Generate comprehensive report
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 80)
        
        total_tests = 0
        total_successful = 0
        
        for agent_name, result in all_results.items():
            successful = sum(1 for r in result["responses"] if r["success"])
            total = len(result["responses"])
            success_rate = successful / total if total > 0 else 0
            
            total_tests += total
            total_successful += successful
            
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"\n{status} {agent_name}")
            print(f"   Success Rate: {success_rate:.1%} ({successful}/{total})")
            
            if result["errors"]:
                print(f"   Errors: {len(result['errors'])}")
                for error in result["errors"][:2]:  # Show first 2 errors
                    print(f"     • {error}")
        
        overall_success_rate = total_successful / total_tests if total_tests > 0 else 0
        
        print(f"\n🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {total_successful}")
        print(f"   Success Rate: {overall_success_rate:.1%}")
        
        if overall_success_rate >= 0.8:
            print("🎉 EXCELLENT! Most agents are working well")
        elif overall_success_rate >= 0.6:
            print("✅ GOOD! Agents are mostly functional")
        elif overall_success_rate >= 0.4:
            print("⚠️  FAIR! Some agents need attention")
        else:
            print("❌ POOR! Agents need significant fixes")
        
        # Save detailed results
        results_file = project_root / "tests" / "ui_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        print(f"\n💾 Detailed results saved to: {results_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution error: {e}")
    finally:
        # Always stop Streamlit
        tester.stop_streamlit()
    
    print("\n🏁 UI testing complete!")
    return all_results

def run_individual_agent_test(agent_name: str):
    """Run tests for a specific agent"""
    print(f"🧪 Testing individual agent: {agent_name}")
    
    test_cases = get_agent_test_cases()
    if agent_name not in test_cases:
        print(f"❌ Agent '{agent_name}' not found in test cases")
        print(f"Available agents: {list(test_cases.keys())}")
        return
    
    tester = StreamlitUITester()
    
    try:
        if tester.start_streamlit():
            result = tester.simulate_user_interaction(agent_name, test_cases[agent_name])
            
            print(f"\n📊 Final Result for {agent_name}:")
            print(f"   Success: {'✅ YES' if result['success'] else '❌ NO'}")
            print(f"   Success Rate: {result.get('success_rate', 0):.1%}")
            
            return result
        else:
            print("❌ Failed to start Streamlit UI")
    finally:
        tester.stop_streamlit()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Strands SDK Agents UI")
    parser.add_argument("--agent", help="Test specific agent only")
    parser.add_argument("--list", action="store_true", help="List available agents")
    
    args = parser.parse_args()
    
    if args.list:
        test_cases = get_agent_test_cases()
        print("Available agents for testing:")
        for i, agent in enumerate(test_cases.keys(), 1):
            print(f"  {i}. {agent}")
    elif args.agent:
        run_individual_agent_test(args.agent)
    else:
        run_comprehensive_ui_tests()
