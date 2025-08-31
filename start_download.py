#!/usr/bin/env python3
"""
START WITH DOWNLOAD - Full YouTube Downloader!
Includes video and audio downloading capabilities
"""

import os
import sys
import subprocess

def install_download_packages():
    """Install packages needed for info display"""
    print("📦 Installing info packages...")
    
    packages = [
        ("Flask", "Flask==2.3.3"),
        ("Requests", "requests==2.31.0")
    ]
    
    for name, package in packages:
        try:
            __import__(name.lower().replace('-', '_'))
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
    print("🎬 YouTube Downloader App - Full Version")
    print("=" * 45)
    
    # Install packages
    if not install_download_packages():
        print("❌ Failed to install required packages")
        input("Press Enter to exit...")
        return
    
    # Start the app
    print("\n🚀 Starting downloader app...")
    print("📱 Open: http://localhost:5000")
    print("🎵 Features: Video + Audio download")
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
