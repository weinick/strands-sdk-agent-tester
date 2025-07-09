#!/usr/bin/env python3
"""
Startup script for Strands SDK Agent Tester UI
Run this script to launch the Streamlit interface
"""

import subprocess
import sys
import os
from pathlib import Path

# Add parent directory to Python path for agent imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

def check_streamlit_installed():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_ui_requirements():
    """Install UI-specific requirements"""
    print("Installing UI requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_ui.txt"
        ])
        print("✅ UI requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def launch_streamlit():
    """Launch the Streamlit application"""
    print("🚀 Launching Strands SDK Agent Tester...")
    print("📱 The UI will open in your default web browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n" + "="*50)
    print("💡 Tips:")
    print("- Use Ctrl+C to stop the server")
    print("- Refresh the browser if you make code changes")
    print("- Check the terminal for any error messages")
    print("="*50 + "\n")
    
    # Set environment variables for Strands tools
    print("⚙️ Setting up Strands SDK environment...")
    os.environ["BYPASS_TOOL_CONSENT"] = "true"
    os.environ["STRANDS_BROWSER_HEADLESS"] = "true"  # Run browser in headless mode for UI
    print("✅ Environment configured for Strands tools")
    
    try:
        # Launch Streamlit with custom configuration
        subprocess.run([
            "streamlit", "run", "streamlit_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "light"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down Strands SDK Agent Tester...")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it first:")
        print("   pip install streamlit")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")

def main():
    """Main function"""
    print("🤖 Strands SDK Agent Tester - Startup Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("streamlit_ui.py").exists():
        print("❌ Error: streamlit_ui.py not found!")
        print("Please run this script from the StrandsSDK project directory.")
        sys.exit(1)
    
    # Check if Streamlit is installed
    if not check_streamlit_installed():
        print("📦 Streamlit not found. Installing UI requirements...")
        if not install_ui_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print("   pip install -r requirements_ui.txt")
            sys.exit(1)
    
    # Check if main requirements are installed
    try:
        # Try to import a common package that should be in requirements.txt
        import boto3  # Assuming AWS SDK is in main requirements
    except ImportError:
        print("⚠️  Warning: Main project requirements may not be installed.")
        print("   Please run: pip install -r requirements.txt")
        print("   Continuing anyway...")
    
    # Launch the UI
    launch_streamlit()

if __name__ == "__main__":
    main()
