#!/usr/bin/env python3
"""
Playwright-based UI Tests for Strands SDK Agents
Tests all 6 agents through the actual Streamlit web interface
"""

import sys
import time
import json
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, List, Any
import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class StreamlitUITester:
    """Playwright-based tester for Streamlit UI"""
    
    def __init__(self):
        self.project_root = project_root
        self.streamlit_process = None
        self.base_url = "http://localhost:8501"
        
    async def start_streamlit(self):
        """Start Streamlit server for testing"""
        print("🚀 Starting Streamlit server...")
        ui_script = self.project_root / "ui" / "streamlit_ui.py"
        
        self.streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", str(ui_script),
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], cwd=self.project_root / "ui")
        
        # Wait for Streamlit to start
        print("⏳ Waiting for Streamlit to initialize...")
        await asyncio.sleep(10)
        print("✅ Streamlit server started")
    
    def stop_streamlit(self):
        """Stop Streamlit server"""
        if self.streamlit_process:
            print("🛑 Stopping Streamlit server...")
            self.streamlit_process.terminate()
            self.streamlit_process.wait()
            print("✅ Streamlit server stopped")

# Test data for each agent
AGENT_TEST_CASES = {
    "Simple Agent": [
        {
            "message": "Hello, how are you today?",
            "expected_keywords": ["hello", "hi", "good", "help", "fine"],
            "category": "Greeting"
        },
        {
            "message": "What can you help me with?",
            "expected_keywords": ["help", "assist", "can", "support"],
            "category": "Capability Inquiry"
        },
        {
            "message": "Tell me about yourself",
            "expected_keywords": ["agent", "ai", "assistant", "strands"],
            "category": "Self Description"
        }
    ],
    
    "Agent with Tools": [
        {
            "message": "Calculate 15 * 23 + 45",
            "expected_keywords": ["calculate", "result", "390", "answer"],
            "category": "Math Calculation"
        },
        {
            "message": "What's the square root of 144?",
            "expected_keywords": ["square", "root", "12", "result"],
            "category": "Square Root"
        },
        {
            "message": "Search for information about Python programming",
            "expected_keywords": ["python", "programming", "search", "information"],
            "category": "Web Search"
        }
    ],
    
    "Custom Tool Agent": [
        {
            "message": "Analyze this text: 'The quick brown fox jumps over the lazy dog'",
            "expected_keywords": ["analyze", "text", "words", "characters"],
            "category": "Text Analysis"
        },
        {
            "message": "Generate a hash for the password 'test123'",
            "expected_keywords": ["hash", "password", "generated"],
            "category": "Hash Generation"
        },
        {
            "message": "What custom tools do you have?",
            "expected_keywords": ["custom", "tools", "available", "text"],
            "category": "Tool Inquiry"
        }
    ],
    
    "Web Research Agent": [
        {
            "message": "Research the latest developments in artificial intelligence",
            "expected_keywords": ["research", "ai", "artificial intelligence", "developments"],
            "category": "AI Research"
        },
        {
            "message": "Find information about climate change solutions",
            "expected_keywords": ["climate", "change", "solutions", "environment"],
            "category": "Climate Research"
        },
        {
            "message": "What are the current trends in web development?",
            "expected_keywords": ["trends", "web", "development", "current"],
            "category": "Tech Trends"
        }
    ],
    
    "File Manager Agent": [
        {
            "message": "List the files in the current directory",
            "expected_keywords": ["files", "directory", "list", "folder"],
            "category": "Directory Listing"
        },
        {
            "message": "Show me the project structure",
            "expected_keywords": ["project", "structure", "folders", "files"],
            "category": "Project Structure"
        },
        {
            "message": "What file operations can you perform?",
            "expected_keywords": ["file", "operations", "create", "read", "write"],
            "category": "File Operations"
        }
    ],
    
    "Multi Agent System": [
        {
            "message": "I need help with both calculations and research",
            "expected_keywords": ["calculations", "research", "help", "agents"],
            "category": "Multi-Task Request"
        },
        {
            "message": "Can you coordinate multiple agents to solve a problem?",
            "expected_keywords": ["coordinate", "multiple", "agents", "solve"],
            "category": "Agent Coordination"
        },
        {
            "message": "What agents are available in the system?",
            "expected_keywords": ["agents", "available", "system", "list"],
            "category": "System Inquiry"
        }
    ]
}

# User personas for realistic testing
USER_PERSONAS = {
    "Developer": {
        "description": "Software developer exploring AI agents",
        "agents_of_interest": ["Custom Tool Agent", "File Manager Agent", "Multi Agent System"],
        "conversation_style": "technical, specific, tool-focused"
    },
    "Researcher": {
        "description": "Academic researcher needing information",
        "agents_of_interest": ["Web Research Agent", "Agent with Tools", "Multi Agent System"],
        "conversation_style": "detailed, analytical, research-focused"
    },
    "Business User": {
        "description": "Professional seeking productivity tools",
        "agents_of_interest": ["Agent with Tools", "File Manager Agent", "Simple Agent"],
        "conversation_style": "practical, efficiency-focused, results-oriented"
    },
    "Student": {
        "description": "Learning about AI and technology",
        "agents_of_interest": ["Simple Agent", "Agent with Tools", "Web Research Agent"],
        "conversation_style": "curious, learning-focused, example-seeking"
    }
}

async def test_agent_basic_functionality(page, agent_name: str, test_cases: List[Dict]):
    """Test basic functionality of a specific agent"""
    print(f"\n🤖 Testing {agent_name}")
    print("=" * 50)
    
    results = {
        "agent_name": agent_name,
        "test_cases": [],
        "success_count": 0,
        "total_tests": len(test_cases)
    }
    
    try:
        # Navigate to the Streamlit app
        await page.goto("http://localhost:8501")
        await page.wait_for_load_state("networkidle")
        
        # Select the agent from sidebar
        print(f"📋 Selecting {agent_name}...")
        agent_selector = page.locator("div[data-testid='stSelectbox'] select")
        await agent_selector.select_option(label=agent_name)
        await page.wait_for_timeout(2000)  # Wait for agent to load
        
        # Test each test case
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}/{len(test_cases)}: {test_case['category']}")
            print(f"   Message: {test_case['message']}")
            
            test_result = {
                "test_number": i,
                "category": test_case['category'],
                "message": test_case['message'],
                "success": False,
                "response": "",
                "error": None
            }
            
            try:
                # Find and fill the chat input
                chat_input = page.locator("div[data-testid='stChatInput'] textarea")
                await chat_input.fill(test_case['message'])
                
                # Submit the message
                submit_button = page.locator("div[data-testid='stChatInput'] button")
                await submit_button.click()
                
                # Wait for response
                print("   ⏳ Waiting for response...")
                await page.wait_for_timeout(8000)  # Wait up to 8 seconds for response
                
                # Get the response
                chat_messages = page.locator("div[data-testid='stChatMessage']")
                message_count = await chat_messages.count()
                
                if message_count >= 2:  # At least user message and agent response
                    last_message = chat_messages.nth(message_count - 1)
                    response_text = await last_message.inner_text()
                    
                    # Check for expected keywords
                    response_lower = response_text.lower()
                    found_keywords = [kw for kw in test_case['expected_keywords'] 
                                    if kw.lower() in response_lower]
                    
                    # Determine success
                    keyword_match_rate = len(found_keywords) / len(test_case['expected_keywords'])
                    has_substantial_response = len(response_text) > 50
                    
                    test_result["success"] = keyword_match_rate >= 0.3 or has_substantial_response
                    test_result["response"] = response_text
                    test_result["found_keywords"] = found_keywords
                    test_result["keyword_match_rate"] = keyword_match_rate
                    
                    if test_result["success"]:
                        results["success_count"] += 1
                        print(f"   ✅ SUCCESS - Keywords: {len(found_keywords)}/{len(test_case['expected_keywords'])}")
                        print(f"   📄 Response: {response_text[:100]}...")
                    else:
                        print(f"   ❌ FAILED - Keywords: {len(found_keywords)}/{len(test_case['expected_keywords'])}")
                        print(f"   📄 Response: {response_text[:100]}...")
                else:
                    test_result["error"] = "No response received"
                    print("   ❌ FAILED - No response received")
                
            except Exception as e:
                test_result["error"] = str(e)
                print(f"   ❌ ERROR: {e}")
            
            results["test_cases"].append(test_result)
            
            # Brief pause between tests
            await page.wait_for_timeout(1000)
        
        # Calculate success rate
        results["success_rate"] = results["success_count"] / results["total_tests"]
        
        print(f"\n📊 {agent_name} Results:")
        print(f"   Success Rate: {results['success_rate']:.1%} ({results['success_count']}/{results['total_tests']})")
        
        return results
        
    except Exception as e:
        print(f"❌ Agent setup error: {e}")
        results["setup_error"] = str(e)
        return results

async def test_user_persona_scenario(page, persona_name: str, persona_data: Dict):
    """Test a realistic user scenario with a specific persona"""
    print(f"\n👤 Testing User Persona: {persona_name}")
    print(f"   Description: {persona_data['description']}")
    print("=" * 60)
    
    scenario_results = {
        "persona_name": persona_name,
        "description": persona_data['description'],
        "agent_tests": [],
        "overall_success": 0
    }
    
    # Test the persona's agents of interest
    for agent_name in persona_data['agents_of_interest']:
        if agent_name in AGENT_TEST_CASES:
            print(f"\n🎭 {persona_name} interacting with {agent_name}")
            
            # Use first test case for persona testing
            test_case = AGENT_TEST_CASES[agent_name][0]
            
            try:
                # Navigate and select agent
                await page.goto("http://localhost:8501")
                await page.wait_for_load_state("networkidle")
                
                agent_selector = page.locator("div[data-testid='stSelectbox'] select")
                await agent_selector.select_option(label=agent_name)
                await page.wait_for_timeout(2000)
                
                # Send message
                chat_input = page.locator("div[data-testid='stChatInput'] textarea")
                await chat_input.fill(test_case['message'])
                
                submit_button = page.locator("div[data-testid='stChatInput'] button")
                await submit_button.click()
                
                # Wait for response
                await page.wait_for_timeout(6000)
                
                # Check response
                chat_messages = page.locator("div[data-testid='stChatMessage']")
                message_count = await chat_messages.count()
                
                success = message_count >= 2
                
                agent_result = {
                    "agent_name": agent_name,
                    "test_message": test_case['message'],
                    "success": success,
                    "persona_relevant": True
                }
                
                scenario_results["agent_tests"].append(agent_result)
                
                if success:
                    scenario_results["overall_success"] += 1
                    print(f"   ✅ {persona_name} successfully interacted with {agent_name}")
                else:
                    print(f"   ❌ {persona_name} failed to interact with {agent_name}")
                
            except Exception as e:
                print(f"   ❌ Error testing {agent_name}: {e}")
                scenario_results["agent_tests"].append({
                    "agent_name": agent_name,
                    "error": str(e),
                    "success": False
                })
    
    # Calculate overall persona success
    total_tests = len(scenario_results["agent_tests"])
    if total_tests > 0:
        scenario_results["success_rate"] = scenario_results["overall_success"] / total_tests
        print(f"\n🎯 {persona_name} Overall Success: {scenario_results['success_rate']:.1%}")
    
    return scenario_results

async def run_comprehensive_ui_tests():
    """Run comprehensive Playwright UI tests"""
    print("🎭 STRANDS SDK AGENTS - PLAYWRIGHT UI TESTS")
    print("=" * 80)
    print("Testing all 6 agents through actual Streamlit web interface")
    print("Using Playwright for realistic browser-based interactions")
    print("=" * 80)
    
    # Start Streamlit server
    tester = StreamlitUITester()
    await tester.start_streamlit()
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            all_results = {
                "agent_tests": {},
                "persona_tests": {},
                "summary": {}
            }
            
            # Test each agent
            print("\n🤖 TESTING INDIVIDUAL AGENTS")
            print("=" * 40)
            
            for agent_name, test_cases in AGENT_TEST_CASES.items():
                result = await test_agent_basic_functionality(page, agent_name, test_cases)
                all_results["agent_tests"][agent_name] = result
            
            # Test user personas
            print("\n\n👥 TESTING USER PERSONAS")
            print("=" * 40)
            
            for persona_name, persona_data in USER_PERSONAS.items():
                result = await test_user_persona_scenario(page, persona_name, persona_data)
                all_results["persona_tests"][persona_name] = result
            
            # Generate summary
            total_agent_tests = sum(r.get("total_tests", 0) for r in all_results["agent_tests"].values())
            total_agent_success = sum(r.get("success_count", 0) for r in all_results["agent_tests"].values())
            
            total_persona_tests = sum(len(r.get("agent_tests", [])) for r in all_results["persona_tests"].values())
            total_persona_success = sum(r.get("overall_success", 0) for r in all_results["persona_tests"].values())
            
            all_results["summary"] = {
                "total_agents_tested": len(AGENT_TEST_CASES),
                "agent_test_success_rate": total_agent_success / total_agent_tests if total_agent_tests > 0 else 0,
                "total_personas_tested": len(USER_PERSONAS),
                "persona_test_success_rate": total_persona_success / total_persona_tests if total_persona_tests > 0 else 0,
                "overall_success_rate": (total_agent_success + total_persona_success) / (total_agent_tests + total_persona_tests) if (total_agent_tests + total_persona_tests) > 0 else 0
            }
            
            # Display final results
            print("\n" + "=" * 100)
            print("🎭 PLAYWRIGHT UI TEST RESULTS")
            print("=" * 100)
            
            print(f"\n🤖 AGENT TESTING RESULTS:")
            for agent_name, result in all_results["agent_tests"].items():
                success_rate = result.get("success_rate", 0)
                status = "✅ PASS" if success_rate >= 0.7 else "⚠️ PARTIAL" if success_rate >= 0.4 else "❌ FAIL"
                print(f"   {status} {agent_name}: {success_rate:.1%}")
            
            print(f"\n👥 PERSONA TESTING RESULTS:")
            for persona_name, result in all_results["persona_tests"].items():
                success_rate = result.get("success_rate", 0)
                status = "✅ PASS" if success_rate >= 0.7 else "⚠️ PARTIAL" if success_rate >= 0.4 else "❌ FAIL"
                print(f"   {status} {persona_name}: {success_rate:.1%}")
            
            summary = all_results["summary"]
            print(f"\n🎯 OVERALL RESULTS:")
            print(f"   Agents Tested: {summary['total_agents_tested']}")
            print(f"   Agent Success Rate: {summary['agent_test_success_rate']:.1%}")
            print(f"   Personas Tested: {summary['total_personas_tested']}")
            print(f"   Persona Success Rate: {summary['persona_test_success_rate']:.1%}")
            print(f"   Overall Success Rate: {summary['overall_success_rate']:.1%}")
            
            # Save results
            results_file = project_root / "tests" / "playwright_ui_results.json"
            with open(results_file, 'w') as f:
                json.dump(all_results, f, indent=2, default=str)
            print(f"\n💾 Results saved to: {results_file}")
            
            await browser.close()
            
            return all_results
    
    finally:
        tester.stop_streamlit()

if __name__ == "__main__":
    asyncio.run(run_comprehensive_ui_tests())
