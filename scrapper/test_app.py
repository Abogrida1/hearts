#!/usr/bin/env python3
"""
Test script for YouTube Info App
Run this to test if everything is working correctly
"""

import requests
import time
import sys

def test_app():
    """Test the Flask app"""
    print("🧪 Testing YouTube Info App...")
    print("=" * 40)
    
    # Start the app in background (you need to start it manually first)
    print("⚠️  Please start the app first by running: python app.py")
    print("   Then press Enter to continue testing...")
    input()
    
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test main page
    print("\n2️⃣ Testing main page...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Main page working")
        else:
            print(f"❌ Main page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main page error: {e}")
    
    # Test video info endpoint
    print("\n3️⃣ Testing video info endpoint...")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
    
    try:
        response = requests.post(f"{base_url}/get_info", 
                               json={"url": test_url}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Video info endpoint working")
            print(f"   Title: {data.get('title', 'N/A')}")
            print(f"   Author: {data.get('author', 'N/A')}")
        else:
            print(f"❌ Video info failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Video info error: {e}")
    
    print("\n🎉 Testing completed!")
    print("If all tests passed, your app is working correctly!")

if __name__ == "__main__":
    test_app()
