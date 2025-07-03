import streamlit as st
import sys
import os
from pathlib import Path
import traceback
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import agent runner from current directory
from agent_runner import AgentRunner, get_model_config

# Initialize agent runner
@st.cache_resource
def get_agent_runner():
    return AgentRunner(str(project_root))

# Page configuration
st.set_page_config(
    page_title="Strands SDK Agent Tester",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FF6B35;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .sample-input-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 2px solid #dee2e6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,123,255,0.3);
        min-height: 3rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,123,255,0.4);
    }
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 4px rgba(0,123,255,0.3);
    }
    /* Different colors for different agent types */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
        box-shadow: 0 2px 4px rgba(40,167,69,0.3);
    }
    div[data-testid="column"]:nth-child(1) .stButton > button:hover {
        background: linear-gradient(135deg, #1e7e34 0%, #155724 100%);
        box-shadow: 0 4px 12px rgba(40,167,69,0.4);
    }
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
        box-shadow: 0 2px 4px rgba(255,193,7,0.3);
        color: #212529;
    }
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background: linear-gradient(135deg, #e0a800 0%, #d39e00 100%);
        box-shadow: 0 4px 12px rgba(255,193,7,0.4);
    }
    div[data-testid="column"]:nth-child(3) .stButton > button {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        box-shadow: 0 2px 4px rgba(220,53,69,0.3);
    }
    div[data-testid="column"]:nth-child(3) .stButton > button:hover {
        background: linear-gradient(135deg, #c82333 0%, #bd2130 100%);
        box-shadow: 0 4px 12px rgba(220,53,69,0.4);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🤖 Strands SDK Agent Tester</h1>', unsafe_allow_html=True)

# Sidebar for agent selection
st.sidebar.title("🎯 Agent Selection")
st.sidebar.markdown("Choose an agent to test and interact with:")

# Agent configurations
AGENTS = {
    "Simple Agent": {
        "description": "Basic conversational agent with no tools",
        "file_path": "basic_agent/simple_agent.py",
        "class_name": "SimpleAgent",
        "supports_chat": True
    },
    "Agent with Tools": {
        "description": "Agent with built-in tools (calculator, web search, etc.)",
        "file_path": "basic_agent/agent_with_tools.py", 
        "class_name": "AgentWithTools",
        "supports_chat": True
    },
    "Custom Tool Agent": {
        "description": "Agent with custom tools and functions",
        "file_path": "basic_agent/custom_tool_agent.py",
        "class_name": "CustomToolAgent", 
        "supports_chat": True
    },
    "Web Research Agent": {
        "description": "Specialized agent for web research and information gathering",
        "file_path": "advanced_agent/web_research_agent.py",
        "class_name": "WebResearchAgent",
        "supports_chat": True
    },
    "File Manager Agent": {
        "description": "Agent for file operations and management",
        "file_path": "advanced_agent/file_manager_agent.py",
        "class_name": "FileManagerAgent",
        "supports_chat": True
    },
    "Multi Agent System": {
        "description": "Collaborative system with multiple specialized agents working together",
        "file_path": "advanced_agent/multi_agent_system.py",
        "class_name": "MultiAgentSystem",
        "supports_chat": True
    }
}

# Agent selection
selected_agent = st.sidebar.selectbox(
    "Select Agent:",
    list(AGENTS.keys()),
    help="Choose which agent you want to test"
)

# Display agent information
if selected_agent:
    agent_info = AGENTS[selected_agent]
    st.sidebar.markdown(f"**Description:** {agent_info['description']}")
    st.sidebar.markdown(f"**File:** `{agent_info['file_path']}`")

# Configuration section
st.sidebar.markdown("---")
st.sidebar.title("⚙️ Configuration")

# Model selection
model_provider = st.sidebar.selectbox(
    "Model Provider:",
    ["AWS Bedrock", "OpenAI", "Anthropic"],
    help="Select the AI model provider"
)

# Model specific settings
if model_provider == "AWS Bedrock":
    model_name = st.sidebar.selectbox(
        "Bedrock Model:",
        ["us.anthropic.claude-3-7-sonnet-20250219-v1:0",
         "anthropic.claude-3-5-sonnet-20241022-v2:0",
         "anthropic.claude-3-sonnet-20240229-v1:0", 
         "anthropic.claude-3-haiku-20240307-v1:0",
         "anthropic.claude-v2:1"],
        help="Select the Bedrock model to use"
    )
elif model_provider == "OpenAI":
    model_name = st.sidebar.text_input(
        "OpenAI Model:",
        value="gpt-4",
        help="Enter the OpenAI model name"
    )
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key:",
        type="password",
        help="Enter your OpenAI API key"
    )
elif model_provider == "Anthropic":
    model_name = st.sidebar.text_input(
        "Anthropic Model:",
        value="claude-3-sonnet-20240229",
        help="Enter the Anthropic model name"
    )
    anthropic_api_key = st.sidebar.text_input(
        "Anthropic API Key:",
        type="password",
        help="Enter your Anthropic API key"
    )

# Temperature setting
temperature = st.sidebar.slider(
    "Temperature:",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Controls randomness in responses"
)

# Max tokens
max_tokens = st.sidebar.number_input(
    "Max Tokens:",
    min_value=100,
    max_value=4000,
    value=1000,
    step=100,
    help="Maximum number of tokens in response"
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 💬 Chat Interface")
    
    # Sample inputs section for different agents
    if selected_agent in ["Simple Agent", "Agent with Tools", "Custom Tool Agent", "Web Research Agent", "File Manager Agent", "Multi Agent System"]:
        st.markdown('<div class="sample-input-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Quick Test Examples")
        st.markdown(f"*Click any example below to test the {selected_agent} instantly:*")
        
        # Create columns for sample input buttons
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        
        # Define sample inputs for each agent
        if selected_agent == "Simple Agent":
            with sample_col1:
                st.markdown("**💬 Conversation**")
                if st.button("👋 Hello, introduce yourself", key="sample1", use_container_width=True, help="Basic greeting and introduction"):
                    st.session_state.sample_input = "Hello! Can you introduce yourself and tell me what you can do?"
            
            with sample_col2:
                st.markdown("**🤔 General Knowledge**")
                if st.button("🌍 Tell me about AI", key="sample2", use_container_width=True, help="General knowledge question"):
                    st.session_state.sample_input = "Can you explain what artificial intelligence is and how it works?"
            
            with sample_col3:
                st.markdown("**✍️ Creative Writing**")
                if st.button("📝 Write a short story", key="sample3", use_container_width=True, help="Creative writing task"):
                    st.session_state.sample_input = "Write a short story about a robot learning to paint"
        
        elif selected_agent == "Agent with Tools":
            with sample_col1:
                st.markdown("**🧮 Calculator**")
                if st.button("➕ Calculate 25 * 47", key="sample1", use_container_width=True, help="Test mathematical calculation"):
                    st.session_state.sample_input = "Can you calculate 25 * 47 for me?"
            
            with sample_col2:
                st.markdown("**🔍 Web Search**")
                if st.button("🌐 Search for Python tutorials", key="sample2", use_container_width=True, help="Test web search functionality"):
                    st.session_state.sample_input = "Search for Python programming tutorials"
            
            with sample_col3:
                st.markdown("**🌤️ Weather**")
                if st.button("☀️ Weather in San Francisco", key="sample3", use_container_width=True, help="Test weather information"):
                    st.session_state.sample_input = "What's the weather like in San Francisco?"
        
        elif selected_agent == "Custom Tool Agent":
            with sample_col1:
                st.markdown("**📊 Text Analysis**")
                if st.button("📈 Analyze sample text", key="sample1", use_container_width=True, help="Test text analysis capabilities"):
                    st.session_state.sample_input = "Analyze this text: 'The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet at least once.'"
            
            with sample_col2:
                st.markdown("**🔑 Keywords**")
                if st.button("🏷️ Extract keywords", key="sample2", use_container_width=True, help="Test keyword extraction"):
                    st.session_state.sample_input = "Extract keywords from this text: 'Machine learning and artificial intelligence are transforming modern technology'"
            
            with sample_col3:
                st.markdown("**🔐 Security**")
                if st.button("🛡️ Generate password", key="sample3", use_container_width=True, help="Test password generation"):
                    st.session_state.sample_input = "Generate a secure password with 12 characters"
        
        elif selected_agent == "Web Research Agent":
            with sample_col1:
                st.markdown("**🔍 Research**")
                if st.button("📚 Research AI trends", key="sample1", use_container_width=True, help="Test research capabilities"):
                    st.session_state.sample_input = "Research the latest trends in artificial intelligence for 2024"
            
            with sample_col2:
                st.markdown("**📰 News**")
                if st.button("📺 Find tech news", key="sample2", use_container_width=True, help="Test news gathering"):
                    st.session_state.sample_input = "Find recent news about machine learning breakthroughs"
            
            with sample_col3:
                st.markdown("**🎓 Learning**")
                if st.button("📖 Best Python resources", key="sample3", use_container_width=True, help="Test educational content search"):
                    st.session_state.sample_input = "Find the best online resources for learning Python programming"
        
        elif selected_agent == "File Manager Agent":
            with sample_col1:
                st.markdown("**📁 Directory Exploration**")
                if st.button("📋 List files in current directory", key="sample1", use_container_width=True, help="Test Case 1: Basic directory listing"):
                    st.session_state.sample_input = "List files in the current directory"
            
            with sample_col2:
                st.markdown("**🔍 File Search**")
                if st.button("🐍 Search for Python files", key="sample2", use_container_width=True, help="Test Case 2: Pattern-based file search"):
                    st.session_state.sample_input = "Search for all Python files in the project"
            
            with sample_col3:
                st.markdown("**🧭 Navigation**")
                if st.button("📍 Where am I?", key="sample3", use_container_width=True, help="Test Case 3: Current directory check"):
                    st.session_state.sample_input = "Where am I? What's my current directory?"
        
        elif selected_agent == "Multi Agent System":
            with sample_col1:
                st.markdown("**🤝 Collaboration**")
                if st.button("🧮 Math + Analysis", key="sample1", use_container_width=True, help="Test multi-agent collaboration"):
                    st.session_state.sample_input = "Calculate the square root of 144 and then analyze the result"
            
            with sample_col2:
                st.markdown("**📊 Complex Task**")
                if st.button("📈 Data + Research", key="sample2", use_container_width=True, help="Test complex multi-step task"):
                    st.session_state.sample_input = "Research Python data science libraries and create a comparison"
            
            with sample_col3:
                st.markdown("**🎯 Problem Solving**")
                if st.button("🧩 Multi-step problem", key="sample3", use_container_width=True, help="Test collaborative problem solving"):
                    st.session_state.sample_input = "Help me plan a Python learning roadmap with timeline and resources"
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize sample input state
    if "sample_input" not in st.session_state:
        st.session_state.sample_input = None
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.caption(f"*{message['timestamp']}*")
    
    # Handle sample input or regular chat input
    prompt = None
    
    # Check if sample input was clicked
    if st.session_state.sample_input:
        prompt = st.session_state.sample_input
        st.session_state.sample_input = None  # Reset after use
    
    # Regular chat input
    if not prompt:
        prompt = st.chat_input("Ask your agent anything...")
    
    # Process the input (either from sample or chat input)
    if prompt:
        # Add user message to chat history
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"*{timestamp}*")
        
        # Generate agent response
        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking..."):
                try:
                    # Get agent runner
                    agent_runner = get_agent_runner()
                    
                    # Prepare model configuration
                    model_config = get_model_config(
                        provider=model_provider,
                        model=model_name,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        api_key=locals().get(f"{model_provider.lower().replace(' ', '_')}_api_key", "")
                    )
                    
                    # Run the selected agent
                    response = agent_runner.run_agent(
                        agent_type=selected_agent,
                        model_config=model_config,
                        user_input=prompt
                    )
                    
                    st.markdown(response)
                    response_timestamp = datetime.now().strftime("%H:%M:%S")
                    st.caption(f"*{response_timestamp}*")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": response_timestamp
                    })
                    
                    # Rerun to update the UI with new messages
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"❌ **Error:** {error_msg}",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

with col2:
    st.markdown("## 📊 Agent Status")
    
    # Agent status card
    st.markdown(f"""
    <div class="agent-card">
        <h4>🤖 {selected_agent}</h4>
        <p><strong>Status:</strong> <span style="color: green;">●</span> Ready</p>
        <p><strong>Model:</strong> {model_name}</p>
        <p><strong>Provider:</strong> {model_provider}</p>
        <p><strong>Temperature:</strong> {temperature}</p>
        <p><strong>Max Tokens:</strong> {max_tokens}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Control buttons
    st.markdown("### 🎮 Controls")
    
    col_clear, col_export = st.columns(2)
    
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col_export:
        if st.button("💾 Export Chat", use_container_width=True):
            if st.session_state.messages:
                chat_export = "\n".join([
                    f"[{msg.get('timestamp', 'N/A')}] {msg['role'].upper()}: {msg['content']}"
                    for msg in st.session_state.messages
                ])
                st.download_button(
                    label="📥 Download Chat Log",
                    data=chat_export,
                    file_name=f"chat_log_{selected_agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.info("No chat history to export")
    
    # Statistics
    st.markdown("### 📈 Session Stats")
    total_messages = len(st.session_state.messages)
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    agent_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    
    st.metric("Total Messages", total_messages)
    st.metric("User Messages", user_messages)
    st.metric("Agent Responses", agent_messages)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 <strong>Strands SDK Agent Tester</strong> | Built with Streamlit</p>
    <p>Test and interact with your AI agents in a user-friendly interface</p>
</div>
""", unsafe_allow_html=True)

# Instructions in expander
with st.expander("📖 How to Use This Interface"):
    st.markdown("""
    ### Getting Started:
    1. **Select an Agent** from the sidebar dropdown
    2. **Configure Settings** like model provider and parameters
    3. **Start Chatting** using the input box at the bottom
    4. **Monitor Status** in the right panel
    
    ### Features:
    - 💬 **Interactive Chat**: Real-time conversation with selected agent
    - ⚙️ **Flexible Configuration**: Switch between different models and providers
    - 📊 **Live Monitoring**: Track agent status and session statistics
    - 💾 **Export Capability**: Download chat logs for analysis
    - 🎨 **Clean Interface**: User-friendly design for easy testing
    
    ### Tips:
    - Try different agents to see their unique capabilities
    - Adjust temperature for more creative or focused responses
    - Use the clear button to start fresh conversations
    - Export important conversations for future reference
    """)
