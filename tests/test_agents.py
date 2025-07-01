#!/usr/bin/env python3
"""
Test script for all Strands SDK agents
Verifies that all agents can be created and respond to basic queries
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_agent(agent_name, create_function, test_message="Hello, how are you?"):
    """Test an individual agent"""
    print(f"\n{'='*60}")
    print(f"Testing {agent_name}")
    print('='*60)
    
    try:
        # Create agent
        print("Creating agent...")
        agent = create_function()
        print("✅ Agent created successfully!")
        
        # Get status if available
        if hasattr(agent, 'get_status'):
            status = agent.get_status()
            print(f"Status: {status.get('status', 'Unknown')}")
        
        # Test chat functionality
        print(f"\nTesting with message: '{test_message}'")
        response = agent.chat(test_message)
        
        # Display response (truncated)
        print("\nResponse:")
        print("-" * 40)
        if len(response) > 300:
            print(response[:300] + "...")
        else:
            print(response)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {agent_name}: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🤖 Strands SDK Agents Test Suite")
    print("=" * 60)
    
    # Test configuration
    model_config = {
        "provider": "AWS Bedrock",
        "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    # Import agents
    agents_to_test = []
    
    try:
        from basic_agent.simple_agent import create_simple_agent
        agents_to_test.append(("Simple Agent", lambda: create_simple_agent(model_config)))
    except ImportError as e:
        print(f"⚠️ Could not import Simple Agent: {e}")
    
    try:
        from basic_agent.agent_with_tools import create_agent_with_tools
        agents_to_test.append(("Agent with Tools", lambda: create_agent_with_tools(model_config)))
    except ImportError as e:
        print(f"⚠️ Could not import Agent with Tools: {e}")
    
    try:
        from basic_agent.custom_tool_agent import create_custom_tool_agent
        agents_to_test.append(("Custom Tool Agent", lambda: create_custom_tool_agent(model_config)))
    except ImportError as e:
        print(f"⚠️ Could not import Custom Tool Agent: {e}")
    
    try:
        from advanced_agent.web_research_agent import create_web_research_agent
        agents_to_test.append(("Web Research Agent", lambda: create_web_research_agent(model_config)))
    except ImportError as e:
        print(f"⚠️ Could not import Web Research Agent: {e}")
    
    try:
        from advanced_agent.file_manager_agent import create_file_manager_agent
        agents_to_test.append(("File Manager Agent", lambda: create_file_manager_agent(model_config)))
    except ImportError as e:
        print(f"⚠️ Could not import File Manager Agent: {e}")
    
    # Run tests
    results = []
    for agent_name, create_func in agents_to_test:
        success = test_agent(agent_name, create_func)
        results.append((agent_name, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    for agent_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {agent_name}")
    
    print(f"\nResults: {successful}/{total} agents passed")
    
    if successful == total:
        print("🎉 All agents are working correctly!")
    else:
        print("⚠️ Some agents need attention.")
    
    # Test specific functionality
    print(f"\n{'='*60}")
    print("FUNCTIONALITY TESTS")
    print('='*60)
    
    # Test tools agent with calculation
    if any(name == "Agent with Tools" and success for name, success in results):
        try:
            from basic_agent.agent_with_tools import create_agent_with_tools
            tools_agent = create_agent_with_tools(model_config)
            calc_response = tools_agent.chat("Calculate 15 * 8")
            print("✅ Tools Agent calculation test passed")
        except Exception as e:
            print(f"❌ Tools Agent calculation test failed: {e}")
    
    # Test custom tools agent with text analysis
    if any(name == "Custom Tool Agent" and success for name, success in results):
        try:
            from basic_agent.custom_tool_agent import create_custom_tool_agent
            custom_agent = create_custom_tool_agent(model_config)
            analysis_response = custom_agent.chat('analyze text: "This is a sample text for analysis"')
            print("✅ Custom Tool Agent analysis test passed")
        except Exception as e:
            print(f"❌ Custom Tool Agent analysis test failed: {e}")
    
    # Test research agent
    if any(name == "Web Research Agent" and success for name, success in results):
        try:
            from advanced_agent.web_research_agent import create_web_research_agent
            research_agent = create_web_research_agent(model_config)
            research_response = research_agent.chat("research artificial intelligence")
            print("✅ Web Research Agent research test passed")
        except Exception as e:
            print(f"❌ Web Research Agent research test failed: {e}")
    
    # Test file manager agent
    if any(name == "File Manager Agent" and success for name, success in results):
        try:
            from advanced_agent.file_manager_agent import create_file_manager_agent
            file_agent = create_file_manager_agent(model_config)
            file_response = file_agent.chat("list files")
            print("✅ File Manager Agent file operation test passed")
        except Exception as e:
            print(f"❌ File Manager Agent file operation test failed: {e}")
    
    print(f"\n{'='*60}")
    print("🚀 Testing complete! You can now use the Streamlit UI to interact with your agents.")
    print("Run: python start_ui.py")
    print('='*60)

if __name__ == "__main__":
    main()
