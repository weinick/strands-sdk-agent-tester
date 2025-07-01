#!/usr/bin/env python3
"""
Simple launcher for Strands SDK Agent Tester UI
This script provides easy access to the UI from the root directory
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the UI"""
    print("🚀 Starting Strands SDK Agent Tester UI...")
    
    # Path to the UI startup script
    ui_script = Path(__file__).parent / "ui" / "run_ui.py"
    
    if not ui_script.exists():
        print("❌ UI script not found. Please ensure the ui folder structure is correct.")
        return 1
    
    try:
        # Run the UI script
        result = subprocess.run([sys.executable, str(ui_script)], cwd=ui_script.parent)
        return result.returncode
    except KeyboardInterrupt:
        print("\n👋 UI stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
