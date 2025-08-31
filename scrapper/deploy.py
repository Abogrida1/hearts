#!/usr/bin/env python3
"""
Script to test the Flask application locally
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def test_app():
    """Test the Flask application"""
    print("🚀 Starting Flask application...")
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['DEBUG'] = 'True'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    
    try:
        # Import and test the app
        from app import create_app
        
        app = create_app()
        print("✅ Flask application created successfully")
        
        # Test basic functionality
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
            
            # Test index endpoint
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Index endpoint working")
            else:
                print(f"❌ Index endpoint failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test application: {e}")
        return False

def run_app():
    """Run the Flask application"""
    print("🌐 Starting local server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to run application: {e}")

def main():
    """Main function"""
    print("🎯 YouTube Downloader App - Local Test")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Test app
    if not test_app():
        return
    
    # Run app
    run_app()

if __name__ == "__main__":
    main()
