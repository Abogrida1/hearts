#!/usr/bin/env python3
"""
Ultimate Start Script - No Problems!
This script will work on ANY hosting or local machine
"""

import os
import sys
import subprocess

def install_requirements():
    """Install only the essential requirements"""
    print("📦 Installing essential requirements...")
    
    # Install Flask first
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask==2.3.3"])
        print("✅ Flask installed")
    except:
        print("❌ Failed to install Flask")
        return False
    
    # Install requests
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests==2.31.0"])
        print("✅ Requests installed")
    except:
        print("❌ Failed to install Requests")
        return False
    
    # Note: No external download tools needed
    print("ℹ️  Using built-in download system")
    
    # Install gunicorn (optional for local)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gunicorn==21.2.0"])
        print("✅ Gunicorn installed")
    except:
        print("⚠️  Gunicorn not installed (not needed for local)")
    
    return True

def main():
    print("🎬 YouTube Info App - Ultimate Start")
    print("=" * 40)
    
    # Check if Flask is installed
    try:
        import flask
        print("✅ Flask is ready!")
    except ImportError:
        print("📦 Flask not found, installing...")
        if not install_requirements():
            print("❌ Failed to install requirements")
            input("Press Enter to exit...")
            return
    
    # Check if requests is installed
    try:
        import requests
        print("✅ Requests is ready!")
    except ImportError:
        print("📦 Requests not found, installing...")
        if not install_requirements():
            print("❌ Failed to install requirements")
            input("Press Enter to exit...")
            return
    
    # Start the app
    print("\n🚀 Starting the app...")
    print("📱 Open your browser: http://localhost:5000")
    print("⏹️  Stop: Ctrl+C")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
