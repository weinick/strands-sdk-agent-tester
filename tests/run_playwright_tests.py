#!/usr/bin/env python3
"""
Simple Playwright Test Runner for Strands SDK Agents
Runs browser-based UI tests using Playwright MCP tool
"""

import sys
import asyncio
import subprocess
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def run_playwright_tests():
    """Run Playwright tests for Streamlit UI"""
    print("🎭 Starting Playwright UI Tests")
    print("=" * 50)
    
    try:
        # Import and run the comprehensive tests
        from test_streamlit_ui import run_comprehensive_ui_tests
        
        results = await run_comprehensive_ui_tests()
        
        # Display summary
        summary = results.get("summary", {})
        overall_success = summary.get("overall_success_rate", 0)
        
        print(f"\n🏆 FINAL ASSESSMENT:")
        if overall_success >= 0.8:
            print("🎉 EXCELLENT! All agents working great through UI")
        elif overall_success >= 0.6:
            print("✅ GOOD! Most agents working well through UI")
        elif overall_success >= 0.4:
            print("⚠️ FAIR! Some agents need UI improvements")
        else:
            print("❌ POOR! Significant UI issues need attention")
        
        return results
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure Playwright is installed: pip install playwright")
        print("Then install browsers: playwright install")
        return None
    except Exception as e:
        print(f"❌ Test execution error: {e}")
        return None

def check_playwright_setup():
    """Check if Playwright is properly set up"""
    print("🔍 Checking Playwright Setup")
    print("-" * 30)
    
    try:
        import playwright
        print("✅ Playwright package installed")
        
        # Check if browsers are installed
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--dry-run"],
            capture_output=True,
            text=True
        )
        
        if "chromium" in result.stdout.lower():
            print("✅ Chromium browser available")
        else:
            print("❌ Chromium browser not installed")
            print("   Run: playwright install chromium")
        
        return True
        
    except ImportError:
        print("❌ Playwright not installed")
        print("   Run: pip install playwright")
        print("   Then: playwright install")
        return False

def install_playwright():
    """Install Playwright and browsers"""
    print("📦 Installing Playwright...")
    
    try:
        # Install playwright package
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        print("✅ Playwright package installed")
        
        # Install browsers
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("✅ Chromium browser installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Playwright UI Tests")
    parser.add_argument("--check", action="store_true", help="Check Playwright setup")
    parser.add_argument("--install", action="store_true", help="Install Playwright")
    
    args = parser.parse_args()
    
    if args.install:
        install_playwright()
    elif args.check:
        check_playwright_setup()
    else:
        if check_playwright_setup():
            asyncio.run(run_playwright_tests())
        else:
            print("\n❌ Playwright not properly set up. Run with --install to set up.")
