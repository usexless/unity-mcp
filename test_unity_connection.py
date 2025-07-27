#!/usr/bin/env python3
"""
Unity MCP Connection Test Tool

Tests the Unity MCP Bridge connection and creates a test report.
"""

import socket
import json
import time
import sys
import os

def test_unity_connection():
    """Test Unity connection and create detailed report."""
    
    print("🔍 Unity MCP Connection Test")
    print("=" * 50)
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tests": [],
        "summary": {}
    }
    
    # Test 1: Basic Connection
    print("1. Testing basic connection to Unity...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect(('localhost', 6400))
        
        results["tests"].append({
            "name": "Basic Connection",
            "status": "PASS",
            "message": "Successfully connected to Unity on port 6400"
        })
        print("   ✅ PASS - Connected to Unity")
        
        # Test 2: Send a real Unity command
        print("2. Testing Unity Bridge response...")
        
        # Try simple ping first (as string, not JSON)
        ping_command = "ping"
        print(f"   Sending: {ping_command}")

        sock.send(ping_command.encode('utf-8'))
        
        # Wait for response
        response_data = sock.recv(4096).decode('utf-8')
        print(f"   Received: {response_data}")
        
        try:
            response = json.loads(response_data)
            if response.get("status") == "success":
                results["tests"].append({
                    "name": "Unity Bridge Response",
                    "status": "PASS",
                    "message": "Unity Bridge responded successfully",
                    "response": response
                })
                print("   ✅ PASS - Unity Bridge is responding")
            else:
                results["tests"].append({
                    "name": "Unity Bridge Response",
                    "status": "FAIL",
                    "message": "Unity Bridge responded but with error",
                    "response": response
                })
                print("   ❌ FAIL - Unity Bridge responded with error")
        except json.JSONDecodeError as e:
            results["tests"].append({
                "name": "Unity Bridge Response",
                "status": "FAIL", 
                "message": f"Invalid JSON response: {str(e)}",
                "raw_response": response_data
            })
            print(f"   ❌ FAIL - Invalid JSON response: {e}")
        
        sock.close()
        
    except socket.timeout:
        results["tests"].append({
            "name": "Basic Connection",
            "status": "FAIL",
            "message": "Connection timed out after 5 seconds"
        })
        print("   ❌ FAIL - Connection timed out")
        
    except ConnectionRefusedError:
        results["tests"].append({
            "name": "Basic Connection", 
            "status": "FAIL",
            "message": "Connection refused - Unity not running or bridge not installed"
        })
        print("   ❌ FAIL - Connection refused")
        
    except Exception as e:
        results["tests"].append({
            "name": "Basic Connection",
            "status": "FAIL", 
            "message": f"Unexpected error: {str(e)}"
        })
        print(f"   ❌ FAIL - Unexpected error: {e}")
    
    # Test 3: Check if Unity MCP Bridge package is installed
    print("3. Checking Unity project structure...")
    
    unity_project_paths = [
        "Assets/UnityMcpBridge",
        "Packages/com.unity.mcp.bridge", 
        "Library/PackageCache"
    ]
    
    bridge_found = False
    for path in unity_project_paths:
        if os.path.exists(path):
            bridge_found = True
            results["tests"].append({
                "name": "Unity Bridge Package",
                "status": "PASS",
                "message": f"Found Unity MCP Bridge at: {path}"
            })
            print(f"   ✅ PASS - Found bridge at: {path}")
            break
    
    if not bridge_found:
        results["tests"].append({
            "name": "Unity Bridge Package",
            "status": "WARN",
            "message": "Unity MCP Bridge package not found in common locations"
        })
        print("   ⚠️  WARN - Bridge package not found in common locations")
    
    # Summary
    passed = len([t for t in results["tests"] if t["status"] == "PASS"])
    failed = len([t for t in results["tests"] if t["status"] == "FAIL"])
    warned = len([t for t in results["tests"] if t["status"] == "WARN"])
    
    results["summary"] = {
        "total_tests": len(results["tests"]),
        "passed": passed,
        "failed": failed,
        "warned": warned,
        "overall_status": "PASS" if failed == 0 else "FAIL"
    }
    
    print("\n📊 Test Summary:")
    print(f"   Total Tests: {results['summary']['total_tests']}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Warnings: {warned}")
    print(f"   Overall: {results['summary']['overall_status']}")
    
    # Write results to file
    report_file = "unity_mcp_test_report.json"
    try:
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Test report saved to: {report_file}")
    except Exception as e:
        print(f"\n❌ Failed to save report: {e}")
    
    print("=" * 50)
    
    return results["summary"]["overall_status"] == "PASS"

if __name__ == "__main__":
    success = test_unity_connection()
    sys.exit(0 if success else 1)
