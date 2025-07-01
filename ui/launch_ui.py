#!/usr/bin/env python3
"""
Simple launcher for Strands SDK Agent Tester UI
"""

import subprocess
import sys
import os

def main():
    print("🚀 启动 Strands SDK Agent Tester UI...")
    print("=" * 50)
    
    try:
        # 直接启动 Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "streamlit_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        print("正在启动 Streamlit 服务器...")
        print("UI 将在浏览器中自动打开: http://localhost:8501")
        print("\n按 Ctrl+C 停止服务器")
        print("=" * 50)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n👋 正在关闭 Strands SDK Agent Tester...")
    except Exception as e:
        print(f"❌ 启动错误: {e}")
        print("\n请尝试手动运行:")
        print("streamlit run streamlit_ui.py")

if __name__ == "__main__":
    main()
