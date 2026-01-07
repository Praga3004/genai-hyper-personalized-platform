"""
Quick test script to verify API endpoints are working
Run this from the python-backend directory after starting the server
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /api/health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_filter_options():
    """Test filter options endpoint"""
    print("\nTesting /api/voters/filters/options...")
    try:
        response = requests.get(f"{BASE_URL}/api/voters/filters/options")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Voter categories: {len(data.get('voter_categories', []))} found")
            print(f"  Genders: {len(data.get('genders', []))} found")
        else:
            print(f"  Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_voters():
    """Test voters endpoint"""
    print("\nTesting /api/voters?limit=5...")
    try:
        response = requests.get(f"{BASE_URL}/api/voters?limit=5")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Voters found: {len(data.get('results', []))}")
            if data.get('results'):
                print(f"  First voter: {data['results'][0].get('voter_name', 'N/A')}")
        else:
            print(f"  Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_all():
    """Test all endpoints"""
    print("=" * 50)
    print("Testing API Endpoints")
    print("=" * 50)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Filter Options", test_filter_options()))
    results.append(("Get Voters", test_voters()))
    
    print("\n" + "=" * 50)
    print("Results:")
    print("=" * 50)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    if not all_passed:
        print("\n⚠️  Some tests failed. Make sure:")
        print("  1. Backend server is running (uvicorn main:app --reload)")
        print("  2. Environment variables are set (.env file)")
        print("  3. Supabase connection is working")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_all()

