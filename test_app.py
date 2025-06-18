#!/usr/bin/env python3
"""
Test Flask Application
This script tests if the Flask app is running correctly.
"""

import requests
import time

def test_app():
    """Test the Flask application"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Flask Application")
    print("=" * 40)
    
    try:
        # Test homepage
        print("📄 Testing homepage...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Homepage accessible")
        else:
            print(f"❌ Homepage error: {response.status_code}")
            
        # Test login page
        print("🔐 Testing login page...")
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page error: {response.status_code}")
            
        # Test register page
        print("📝 Testing register page...")
        response = requests.get(f"{base_url}/register", timeout=5)
        if response.status_code == 200:
            print("✅ Register page accessible")
        else:
            print(f"❌ Register page error: {response.status_code}")
            
        print("\n🎉 Application test completed!")
        print(f"🌐 Open your browser and go to: {base_url}")
        print("👤 Admin login: username=admin, password=admin123")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to application")
        print("Make sure the Flask app is running with: python app.py")
    except Exception as e:
        print(f"❌ Error testing application: {e}")

if __name__ == "__main__":
    test_app() 