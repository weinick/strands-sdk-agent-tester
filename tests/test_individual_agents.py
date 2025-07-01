#!/usr/bin/env python3
"""
Individual Agent Playwright Tests
Test specific agents through Streamlit UI using Playwright
"""

import sys
import asyncio
import subprocess
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class IndividualAgentTester:
    """Test individual agents using Playwright"""
    
    def __init__(self):
        self.project_root = project_root
        self.streamlit_process = None
        self.base_url = "http://localhost:8501"
    
    async def start_streamlit(self):
        """Start Streamlit server"""
        print("🚀 Starting Streamlit server...")
        ui_script = self.project_root / "ui" / "streamlit_ui.py"
        
        self.streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", str(ui_script),
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], cwd=self.project_root / "ui")
        
        await asyncio.sleep(8)  # Wait for startup
        print("✅ Streamlit server ready")
    
    def stop_streamlit(self):
        """Stop Streamlit server"""
        if self.streamlit_process:
            print("🛑 Stopping Streamlit server...")
            self.streamlit_process.terminate()
            self.streamlit_process.wait()
    
    async def test_agent_conversation(self, page, agent_name: str, messages: list):
        """Test a conversation with a specific agent"""
        print(f"\n💬 Testing conversation with {agent_name}")
        print("-" * 40)
        
        conversation_result = {
            "agent_name": agent_name,
            "messages": [],
            "success_count": 0,
            "total_messages": len(messages)
        }
        
        try:
            # Navigate to Streamlit app
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")
            
            # Select the agent
            print(f"📋 Selecting {agent_name}...")
            agent_selector = page.locator("div[data-testid='stSelectbox'] select")
            await agent_selector.select_option(label=agent_name)
            await page.wait_for_timeout(2000)
            
            # Test each message in the conversation
            for i, message in enumerate(messages, 1):
                print(f"\n📝 Message {i}/{len(messages)}: {message}")
                
                message_result = {
                    "message_number": i,
                    "user_message": message,
                    "success": False,
                    "response": "",
                    "error": None
                }
                
                try:
                    # Clear any existing input and enter new message
                    chat_input = page.locator("div[data-testid='stChatInput'] textarea")
                    await chat_input.clear()
                    await chat_input.fill(message)
                    
                    # Submit message
                    submit_button = page.locator("div[data-testid='stChatInput'] button")
                    await submit_button.click()
                    
                    # Wait for response
                    print("   ⏳ Waiting for response...")
                    await page.wait_for_timeout(6000)
                    
                    # Get the latest response
                    chat_messages = page.locator("div[data-testid='stChatMessage']")
                    message_count = await chat_messages.count()
                    
                    if message_count >= 2:  # At least user + agent message
                        # Get the last message (agent response)
                        last_message = chat_messages.nth(message_count - 1)
                        response_text = await last_message.inner_text()
                        
                        # Check if response is substantial
                        if len(response_text.strip()) > 20:
                            message_result["success"] = True
                            message_result["response"] = response_text
                            conversation_result["success_count"] += 1
                            
                            print(f"   ✅ SUCCESS - Response: {len(response_text)} chars")
                            print(f"   📄 Preview: {response_text[:80]}...")
                        else:
                            message_result["response"] = response_text
                            print(f"   ❌ FAILED - Response too short: {response_text}")
                    else:
                        message_result["error"] = "No response received"
                        print("   ❌ FAILED - No response received")
                
                except Exception as e:
                    message_result["error"] = str(e)
                    print(f"   ❌ ERROR: {e}")
                
                conversation_result["messages"].append(message_result)
                
                # Brief pause between messages
                await page.wait_for_timeout(1000)
            
            # Calculate success rate
            conversation_result["success_rate"] = conversation_result["success_count"] / conversation_result["total_messages"]
            
            print(f"\n📊 Conversation Results for {agent_name}:")
            print(f"   Success Rate: {conversation_result['success_rate']:.1%}")
            print(f"   Successful Messages: {conversation_result['success_count']}/{conversation_result['total_messages']}")
            
            return conversation_result
            
        except Exception as e:
            print(f"❌ Conversation setup error: {e}")
            conversation_result["setup_error"] = str(e)
            return conversation_result

# Predefined conversations for each agent
AGENT_CONVERSATIONS = {
    "Simple Agent": [
        "Hello! I'm new to AI agents. Can you introduce yourself?",
        "What makes you different from other chatbots?",
        "How can you help me in my daily tasks?",
        "Thank you for the explanation!"
    ],
    
    "Agent with Tools": [
        "Hi! I heard you have some useful tools. What can you do?",
        "Can you calculate 25 * 18 + 127 for me?",
        "What's the square root of 225?",
        "Can you search for information about machine learning?",
        "These tools are really helpful!"
    ],
    
    "Custom Tool Agent": [
        "Hello! I'm interested in your custom capabilities.",
        "Can you analyze this text: 'Artificial intelligence is revolutionizing technology'?",
        "Generate a secure hash for the password 'mySecurePass123'",
        "What other custom tools do you have available?",
        "This is exactly what I needed for my project!"
    ],
    
    "Web Research Agent": [
        "Hi! I need help with research for my project.",
        "Can you research the latest trends in sustainable technology?",
        "Find information about the impact of AI on healthcare",
        "What are the current developments in renewable energy?",
        "This research will be very valuable for my work!"
    ],
    
    "File Manager Agent": [
        "Hello! I need help managing files and directories.",
        "Can you show me the current project structure?",
        "List the files in the docs directory",
        "What file operations can you perform?",
        "This will help me organize my project better!"
    ],
    
    "Multi Agent System": [
        "Hi! I'm curious about how multiple agents work together.",
        "Can you coordinate different agents to help with complex tasks?",
        "I need both calculations and research - can agents collaborate?",
        "Show me what agents are available in the system",
        "This multi-agent approach is fascinating!"
    ]
}

async def test_specific_agent(agent_name: str):
    """Test a specific agent with its conversation"""
    if agent_name not in AGENT_CONVERSATIONS:
        print(f"❌ Agent '{agent_name}' not found in test conversations")
        print(f"Available agents: {list(AGENT_CONVERSATIONS.keys())}")
        return None
    
    tester = IndividualAgentTester()
    
    try:
        await tester.start_streamlit()
        
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            # Test the specific agent
            conversation = AGENT_CONVERSATIONS[agent_name]
            result = await tester.test_agent_conversation(page, agent_name, conversation)
            
            await browser.close()
            
            # Save individual result
            results_file = project_root / "tests" / f"{agent_name.lower().replace(' ', '_')}_test_result.json"
            with open(results_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            
            print(f"\n💾 Results saved to: {results_file}")
            
            return result
    
    finally:
        tester.stop_streamlit()

async def test_all_agents():
    """Test all agents with their conversations"""
    print("🎭 TESTING ALL AGENTS WITH PLAYWRIGHT")
    print("=" * 60)
    
    tester = IndividualAgentTester()
    all_results = {}
    
    try:
        await tester.start_streamlit()
        
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            # Test each agent
            for i, (agent_name, conversation) in enumerate(AGENT_CONVERSATIONS.items(), 1):
                print(f"\n🤖 Testing Agent {i}/{len(AGENT_CONVERSATIONS)}: {agent_name}")
                print("=" * 50)
                
                result = await tester.test_agent_conversation(page, agent_name, conversation)
                all_results[agent_name] = result
                
                # Brief pause between agents
                if i < len(AGENT_CONVERSATIONS):
                    print("\n⏳ Preparing next agent...")
                    await asyncio.sleep(2)
            
            await browser.close()
            
            # Generate summary
            print("\n" + "=" * 80)
            print("🎭 ALL AGENTS TEST SUMMARY")
            print("=" * 80)
            
            total_conversations = len(all_results)
            successful_conversations = 0
            total_messages = 0
            successful_messages = 0
            
            for agent_name, result in all_results.items():
                success_rate = result.get("success_rate", 0)
                success_count = result.get("success_count", 0)
                total_count = result.get("total_messages", 0)
                
                total_messages += total_count
                successful_messages += success_count
                
                if success_rate >= 0.6:  # Consider 60%+ as successful
                    successful_conversations += 1
                
                status = "✅ PASS" if success_rate >= 0.7 else "⚠️ PARTIAL" if success_rate >= 0.4 else "❌ FAIL"
                print(f"{status} {agent_name}: {success_rate:.1%} ({success_count}/{total_count})")
            
            overall_conversation_success = successful_conversations / total_conversations
            overall_message_success = successful_messages / total_messages if total_messages > 0 else 0
            
            print(f"\n🎯 OVERALL RESULTS:")
            print(f"   Successful Conversations: {successful_conversations}/{total_conversations} ({overall_conversation_success:.1%})")
            print(f"   Successful Messages: {successful_messages}/{total_messages} ({overall_message_success:.1%})")
            
            # Save comprehensive results
            comprehensive_results = {
                "summary": {
                    "total_agents": total_conversations,
                    "successful_agents": successful_conversations,
                    "agent_success_rate": overall_conversation_success,
                    "total_messages": total_messages,
                    "successful_messages": successful_messages,
                    "message_success_rate": overall_message_success
                },
                "individual_results": all_results
            }
            
            results_file = project_root / "tests" / "all_agents_playwright_results.json"
            with open(results_file, 'w') as f:
                json.dump(comprehensive_results, f, indent=2, default=str)
            
            print(f"\n💾 Comprehensive results saved to: {results_file}")
            
            return comprehensive_results
    
    finally:
        tester.stop_streamlit()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test individual agents with Playwright")
    parser.add_argument("--agent", help="Test specific agent")
    parser.add_argument("--list", action="store_true", help="List available agents")
    parser.add_argument("--all", action="store_true", help="Test all agents")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available agents for testing:")
        for i, agent in enumerate(AGENT_CONVERSATIONS.keys(), 1):
            print(f"  {i}. {agent}")
    elif args.agent:
        asyncio.run(test_specific_agent(args.agent))
    elif args.all:
        asyncio.run(test_all_agents())
    else:
        # Default: test all agents
        asyncio.run(test_all_agents())
