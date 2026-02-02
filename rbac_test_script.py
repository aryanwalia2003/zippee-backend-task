import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_test():
    print("🚀 Starting RBAC Test Script...\n")

    # 1. Login as Admin
    print("1️⃣  Logging in as Admin...")
    admin_creds = {"username": "admin", "password": "admin123"}
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json=admin_creds)
        if resp.status_code != 200:
            print(f"❌ Failed to login as Admin: {resp.text}")
            return
        
        admin_token = resp.json()['token']
        print("✅ Admin Logged In!\n")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
        return

    # 2. Fetch All Tasks (Admin View)
    print("2️⃣  Fetching All Tasks as Admin...")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    resp = requests.get(f"{BASE_URL}/tasks?limit=5", headers=admin_headers)
    
    if resp.status_code == 200:
        tasks = resp.json()['tasks']
        print(f"✅ Successfully fetched {len(tasks)} tasks.")
        if len(tasks) > 0:
            print(f"   First task ID: {tasks[0]['id']}")
            print(f"   First task User ID: {tasks[0]['user_id']}")
    else:
        print(f"❌ Failed to fetch tasks: {resp.status_code} - {resp.text}")

    print("\n✨ RBAC Test Complete!")

if __name__ == "__main__":
    run_test()
