#!/usr/bin/env python3
"""
START ANYWHERE - Works on ANY hosting or local machine!
No problems, no errors, just works!
"""

import os
import sys
import subprocess

def install_and_run():
    """Install packages and run the app"""
    print("🎬 YouTube Info App - START ANYWHERE")
    print("=" * 45)
    
    packages = [
        ("Flask", "Flask==2.3.3"),
        ("Requests", "requests==2.31.0")
    ]
    
    # Install each package if needed
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
                input("Press Enter to exit...")
                return False
    
    # Start the app
    print("\n🚀 Starting app...")
    print("📱 Open: http://localhost:5000")
    print("⏹️  Stop: Ctrl+C")
    print("-" * 45)
    
    try:
        subprocess.run([sys.executable, "app.py"])
        return True
    except KeyboardInterrupt:
        print("\n👋 Stopped")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
        return False

if __name__ == "__main__":
    install_and_run()
