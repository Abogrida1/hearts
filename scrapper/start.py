#!/usr/bin/env python3
"""
Simple Start Script - No Problems!
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
        print("✅ Flask ready!")
    except ImportError:
        print("📦 Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask==2.3.3"])
            print("✅ Flask installed!")
        except:
            print("❌ Failed to install Flask")
            input("Press Enter to exit...")
            return
    
    # Try to import requests
    try:
        import requests
        print("✅ Requests ready!")
    except ImportError:
        print("📦 Installing Requests...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests==2.31.0"])
            print("✅ Requests installed!")
        except:
            print("❌ Failed to install Requests")
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
