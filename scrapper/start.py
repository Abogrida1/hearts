#!/usr/bin/env python3
"""
YouTube Downloader App - Simple Start
تطبيق تحميل YouTube - تشغيل بسيط
"""

import subprocess
import sys

def main():
    print("🚀 YouTube Downloader App")
    print("=" * 30)
    
    # Install requirements
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed!")
    except:
        print("⚠️  Some packages may not install correctly")
    
    # Start the app
    print("🌐 Starting app...")
    print("📱 Open: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 30)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 App stopped")

if __name__ == "__main__":
    main()
