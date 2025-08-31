#!/usr/bin/env python3
"""
SIMPLE DOWNLOAD START - Built-in Download System!
No external tools needed - everything works from our server
"""

import os
import sys
import subprocess

def install_packages():
    """Install only essential packages"""
    print("📦 Installing essential packages...")
    
    packages = [
        ("Flask", "Flask==2.3.3"),
        ("Requests", "requests==2.31.0")
    ]
    
    for name, package in packages:
        try:
            __import__(name.lower())
            print(f"✅ {name} ready!")
        except ImportError:
            print(f"📦 Installing {name}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {name} installed!")
            except:
                print(f"❌ Failed to install {name}")
                return False
    
    return True

def main():
    print("🎬 YouTube Downloader - Built-in System")
    print("=" * 45)
    print("🚫 No external tools needed!")
    print("💻 Everything runs from our server")
    print("🎵 Direct download buttons included!")
    print("=" * 45)
    
    # Install packages
    if not install_packages():
        print("❌ Failed to install required packages")
        input("Press Enter to exit...")
        return
    
    # Start the app
    print("\n🚀 Starting downloader app...")
    print("📱 Open: http://localhost:5000")
    print("🎵 Features: Built-in download system")
    print("🎵 Audio: MP3 format support")
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
