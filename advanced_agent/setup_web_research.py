#!/usr/bin/env python3
"""
Setup script for Strands Web Research Agent
Installs all required dependencies for real web research capabilities
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr.strip()}")
        return False

def main():
    print("🌐 Strands Web Research Agent Setup")
    print("=" * 50)
    print("This script will install all dependencies needed for real web research capabilities.")
    print()
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  Warning: You're not in a virtual environment.")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please create and activate a virtual environment first:")
            print("  python -m venv venv")
            print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
            return
    
    print("🚀 Starting installation process...")
    
    # Step 1: Install core requirements
    success = run_command(
        "pip install -r requirements.txt",
        "Installing core requirements"
    )
    if not success:
        print("❌ Failed to install core requirements. Please check your pip configuration.")
        return
    
    # Step 2: Install Strands tools with all optional dependencies
    success = run_command(
        "pip install 'strands-agents-tools[all]'",
        "Installing Strands Agents Tools with all dependencies"
    )
    if not success:
        print("⚠️  Failed to install Strands tools with all dependencies. Trying basic installation...")
        success = run_command(
            "pip install strands-agents-tools",
            "Installing basic Strands Agents Tools"
        )
        if not success:
            print("❌ Failed to install Strands tools. Please check your internet connection.")
            return
    
    # Step 3: Install Playwright browsers
    success = run_command(
        "playwright install",
        "Installing Playwright browser binaries"
    )
    if not success:
        print("⚠️  Failed to install Playwright browsers. Trying alternative method...")
        success = run_command(
            "python -m playwright install",
            "Installing Playwright browsers (alternative method)"
        )
        if not success:
            print("❌ Failed to install Playwright browsers. You may need to install them manually.")
    
    # Step 4: Install UI requirements
    if Path("ui/requirements_ui.txt").exists():
        success = run_command(
            "pip install -r ui/requirements_ui.txt",
            "Installing UI requirements"
        )
        if not success:
            print("⚠️  Failed to install UI requirements. UI may not work properly.")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print()
    print("📋 What was installed:")
    print("  ✅ Core Strands SDK dependencies")
    print("  ✅ Official Strands Agents Tools (MCP tools)")
    print("  ✅ Playwright browser automation")
    print("  ✅ Browser binaries (Chromium, Firefox, WebKit)")
    print("  ✅ UI dependencies (if available)")
    print()
    print("🧪 Test your installation:")
    print("  python advanced_agent/web_research_agent.py")
    print()
    print("🚀 Start the UI:")
    print("  python start_ui.py")
    print()
    print("🔧 Environment Variables (optional):")
    print("  export STRANDS_BROWSER_HEADLESS=false    # Show browser window")
    print("  export STRANDS_BROWSER_WIDTH=1280        # Browser width")
    print("  export STRANDS_BROWSER_HEIGHT=800        # Browser height")
    print("  export BYPASS_TOOL_CONSENT=true          # Skip confirmation prompts")
    print()
    print("📚 For more information, see:")
    print("  https://github.com/strands-agents/tools")

if __name__ == "__main__":
    main()
