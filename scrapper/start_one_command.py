#!/usr/bin/env python3
"""
ONE COMMAND START - Works Everywhere!
Just run: python start_one_command.py
"""

import os
import sys
import subprocess

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except:
        return False

def main():
    print("🎬 YouTube Info App - ONE COMMAND START")
    print("=" * 45)
    
    # Install Flask if needed
    try:
        import flask
        print("✅ Flask ready!")
    except ImportError:
        print("📦 Installing Flask...")
        if install_package("Flask==2.3.3"):
            print("✅ Flask installed!")
        else:
            print("❌ Failed to install Flask")
            input("Press Enter to exit...")
            return
    
    # Install requests if needed
    try:
        import requests
        print("✅ Requests ready!")
    except ImportError:
        print("📦 Installing Requests...")
        if install_package("requests==2.31.0"):
            print("✅ Requests installed!")
        else:
            print("❌ Failed to install Requests")
            input("Press Enter to exit...")
            return
    
    # Start the app
    print("\n🚀 Starting app...")
    print("📱 Open: http://localhost:5000")
    print("⏹️  Stop: Ctrl+C")
    print("-" * 45)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
