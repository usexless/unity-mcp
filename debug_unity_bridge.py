#!/usr/bin/env python3
"""
Debug Unity Bridge Communication

Tests specific commands that are failing in Augment Code.
"""

import socket
import json
import time

def test_command(command_data, description):
    """Test a specific command and show detailed results."""
    print(f"\n🔍 Testing: {description}")
    print(f"Command: {json.dumps(command_data, indent=2)}")
    
    try:
        # Connect to Unity
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(60.0)  # 60 second timeout
        sock.connect(('localhost', 6400))
        
        # Send command
        command_json = json.dumps(command_data)
        print(f"Sending: {command_json}")
        
        start_time = time.time()
        sock.send(command_json.encode('utf-8') + b'\n')
        
        # Receive response
        print("Waiting for response...")
        response_data = sock.recv(4096).decode('utf-8')
        elapsed = time.time() - start_time
        
        print(f"Response after {elapsed:.2f}s: {response_data}")
        
        try:
            response = json.loads(response_data)
            if response.get("status") == "success":
                print("✅ SUCCESS")
                return True
            else:
                print(f"❌ FAILED: {response.get('error', 'Unknown error')}")
                return False
        except json.JSONDecodeError as e:
            print(f"❌ INVALID JSON: {e}")
            return False
            
        sock.close()
        
    except socket.timeout:
        print(f"❌ TIMEOUT after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("🚀 Unity Bridge Debug Test")
    print("=" * 50)
    
    # Test 1: Simple ping (we know this works)
    print("\n1. Testing simple ping...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect(('localhost', 6400))
        sock.send(b'ping')
        response = sock.recv(4096).decode('utf-8')
        print(f"Ping response: {response}")
        sock.close()
        print("✅ Ping works")
    except Exception as e:
        print(f"❌ Ping failed: {e}")
        return
    
    # Test 2: Simple manage_editor command (like Augment tried)
    success1 = test_command({
        "type": "manage_editor",
        "params": {
            "action": "get_state"
        }
    }, "manage_editor.get_state")
    
    # Test 3: Simple manage_gameobject command (like Augment tried)
    success2 = test_command({
        "type": "manage_gameobject", 
        "params": {
            "action": "create",
            "name": "TestObject",
            "position": [0, 0, 0]
        }
    }, "manage_gameobject.create")
    
    # Test 4: execute_menu_item command (like Augment tried)
    success3 = test_command({
        "type": "execute_menu_item",
        "params": {
            "menu_path": "GameObject/Create Empty",
            "action": "execute"
        }
    }, "execute_menu_item")
    
    print("\n📊 Summary:")
    print(f"manage_editor: {'✅' if success1 else '❌'}")
    print(f"manage_gameobject: {'✅' if success2 else '❌'}")
    print(f"execute_menu_item: {'✅' if success3 else '❌'}")
    
    if not (success1 and success2 and success3):
        print("\n🔧 The Unity Bridge has problems with these commands!")
        print("This explains why Augment Code gets timeouts.")
    else:
        print("\n🎉 All commands work! The problem might be elsewhere.")

if __name__ == "__main__":
    main()
