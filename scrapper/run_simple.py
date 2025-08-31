#!/usr/bin/env python3
"""
Ultra Simple Start Script
Just run this file and it will handle everything!
"""

import os
import sys
import subprocess

def main():
    print("🎬 YouTube Info App")
    print("=" * 30)
    
    # Try to import Flask
    try:
        import flask
        print("✅ Ready to start!")
    except ImportError:
        print("📦 Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Done!")
        except:
            print("❌ Failed to install. Please run: pip install -r requirements.txt")
            input("Press Enter to exit...")
            return
    
    # Start the app
    print("\n🚀 Starting app...")
    print("📱 Open: http://localhost:5000")
    print("⏹️  Stop: Ctrl+C")
    print("-" * 30)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
