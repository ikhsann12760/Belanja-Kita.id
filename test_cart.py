#!/usr/bin/env python3
"""
Test Cart Functionality
This script tests the cart features of the e-commerce application.
"""

import requests
import json

def test_cart_functionality():
    """Test cart functionality"""
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🧪 Testing Cart Functionality")
    print("=" * 40)
    
    # Test 1: Login
    print("1. Testing login...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data)
    if response.status_code == 200 or response.status_code == 302:
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return
    
    # Test 2: Access cart page
    print("2. Testing cart page access...")
    response = session.get(f"{base_url}/cart")
    if response.status_code == 200:
        print("✅ Cart page accessible")
    else:
        print(f"❌ Cart page error: {response.status_code}")
    
    # Test 3: Add product to cart (assuming product ID 1 exists)
    print("3. Testing add to cart...")
    cart_data = {
        'quantity': 2
    }
    
    response = session.post(f"{base_url}/add_to_cart/1", data=cart_data)
    if response.status_code == 200:
        print("✅ Add to cart successful")
        
        # Check if it's JSON response
        try:
            json_response = response.json()
            if json_response.get('success'):
                print(f"   Message: {json_response.get('message')}")
                print(f"   Cart count: {json_response.get('cart_count')}")
            else:
                print(f"   Error: {json_response.get('message')}")
        except:
            print("   Response is not JSON (redirect)")
    else:
        print(f"❌ Add to cart failed: {response.status_code}")
    
    # Test 4: Check cart again
    print("4. Testing cart after adding item...")
    response = session.get(f"{base_url}/cart")
    if response.status_code == 200:
        print("✅ Cart page accessible after adding item")
        if "Naruto" in response.text:
            print("   Product found in cart")
        else:
            print("   Product not found in cart")
    else:
        print(f"❌ Cart page error: {response.status_code}")
    
    print("\n🎉 Cart functionality test completed!")

if __name__ == "__main__":
    test_cart_functionality() 