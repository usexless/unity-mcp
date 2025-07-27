#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unity MCP Server - Production Ready Version

A Model Context Protocol (MCP) server for Unity Editor automation.
Compatible with MCP clients like Claude Desktop.
"""

import sys
import os

# Ensure UTF-8 encoding for stdout/stderr on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from mcp.server.fastmcp import FastMCP, Context, Image
import logging
import time
import socket
import json
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, List
from config import config
from tools import register_all_tools

# Import enhanced infrastructure (but use simplified connection)
from enhanced_logging import enhanced_logger, LogContext
from timeout_manager import timeout_manager
from exceptions import ConnectionError as UnityConnectionError

# Configure basic logging (enhanced logging is configured separately)
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format=config.log_format
)
logger = logging.getLogger("unity-mcp-server")

# Simplified but robust Unity connection class
class RobustUnityConnection:
    def __init__(self, host="localhost", port=6400):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.connection_start_time = None
        self.total_commands = 0
        self.successful_commands = 0
        self.failed_commands = 0

    def connect(self):
        """Connect to Unity with timeout and logging."""
        try:
            enhanced_logger.info(f"Attempting to connect to Unity at {self.host}:{self.port}")

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10.0)  # 10 second timeout
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.connection_start_time = time.time()

            enhanced_logger.info(f"Successfully connected to Unity at {self.host}:{self.port}")
            return True

        except socket.timeout:
            enhanced_logger.warning(f"Connection to Unity timed out after 10 seconds")
            self.connected = False
            return False
        except ConnectionRefusedError:
            enhanced_logger.warning(f"Unity connection refused - is Unity running with MCP Bridge?")
            self.connected = False
            return False
        except Exception as e:
            enhanced_logger.error(f"Failed to connect to Unity: {e}")
            self.connected = False
            return False

    def send_command(self, command_data):
        """Send command to Unity and get response with enhanced logging."""
        if not self.connected:
            if not self.connect():
                return {"success": False, "error": "Not connected to Unity"}

        self.total_commands += 1
        start_time = time.time()

        try:
            # Convert old format to new format if needed
            if "tool" in command_data and "action" in command_data:
                # Convert from old format: {"tool": "manage_editor", "action": "get_state", ...}
                # To new format: {"type": "manage_editor", "params": {"action": "get_state", ...}}
                tool_name = command_data.pop("tool")
                params = command_data  # All remaining data becomes params

                unity_command = {
                    "type": tool_name,
                    "params": params
                }
            else:
                # Already in correct format or special command
                unity_command = command_data

            # Send command
            command_json = json.dumps(unity_command)
            enhanced_logger.info(f"Sending Unity command: {unity_command.get('type', 'unknown')}")

            self.socket.send(command_json.encode('utf-8') + b'\n')

            # Debug: Log what we're sending
            enhanced_logger.info(f"Sent JSON: {command_json}")

            # Receive response
            response_data = self.socket.recv(4096).decode('utf-8')
            enhanced_logger.info(f"Received response: {response_data}")
            response = json.loads(response_data)

            elapsed = time.time() - start_time

            if response.get("status") == "success":
                self.successful_commands += 1
                enhanced_logger.info(f"Unity command completed successfully in {elapsed:.2f}s")
                # Convert to old format for compatibility
                return {"success": True, "data": response.get("result", {})}
            else:
                self.failed_commands += 1
                enhanced_logger.warning(f"Unity command failed: {response.get('error', 'Unknown error')}")
                return {"success": False, "error": response.get("error", "Unknown error")}

        except socket.timeout:
            self.failed_commands += 1
            elapsed = time.time() - start_time
            enhanced_logger.error(f"Unity command timed out after {elapsed:.2f}s")
            self.connected = False
            return {"success": False, "error": "Command timed out"}

        except Exception as e:
            self.failed_commands += 1
            elapsed = time.time() - start_time
            enhanced_logger.error(f"Unity command failed after {elapsed:.2f}s: {e}")
            self.connected = False
            return {"success": False, "error": str(e)}

    def ping(self):
        """Test connection with a simple ping."""
        # Use simple ping that the bridge understands
        if not self.connected:
            if not self.connect():
                return {"success": False, "error": "Not connected to Unity"}

        try:
            # Send simple ping command (not JSON)
            self.socket.send(b'ping')

            # Receive response
            response_data = self.socket.recv(4096).decode('utf-8')
            enhanced_logger.info(f"Ping response: {response_data}")
            response = json.loads(response_data)

            return response

        except Exception as e:
            enhanced_logger.error(f"Ping failed: {e}")
            self.connected = False
            return {"success": False, "error": str(e)}

    def get_metrics(self):
        """Get connection metrics."""
        uptime = time.time() - self.connection_start_time if self.connection_start_time else 0
        success_rate = (self.successful_commands / self.total_commands * 100) if self.total_commands > 0 else 0

        return {
            "connected": self.connected,
            "uptime": uptime,
            "total_commands": self.total_commands,
            "successful_commands": self.successful_commands,
            "failed_commands": self.failed_commands,
            "success_rate": success_rate
        }

    def disconnect(self):
        """Disconnect from Unity."""
        if self.socket:
            try:
                self.socket.close()
                enhanced_logger.info("Disconnected from Unity")
            except:
                pass
        self.connected = False

# Global connection state
_unity_connection: RobustUnityConnection = None

def test_unity_connection():
    """Test Unity connection on startup and provide detailed feedback."""
    global _unity_connection

    print("\n[INFO] Testing Unity Connection...")
    print("=" * 50)

    # Initialize connection
    _unity_connection = RobustUnityConnection(
        host=getattr(config, 'unity_host', 'localhost'),
        port=getattr(config, 'unity_port', 6400)
    )

    # Test connection
    if _unity_connection.connect():
        print(f"[SUCCESS] Unity Connection: SUCCESS")
        print(f"   Host: {_unity_connection.host}")
        print(f"   Port: {_unity_connection.port}")

        # Test ping
        ping_result = _unity_connection.ping()
        if ping_result.get("status") == "success":
            print(f"[SUCCESS] Unity Bridge: RESPONDING")
            pong_message = ping_result.get("result", {}).get("message", "")
            if pong_message:
                print(f"   Response: {pong_message}")
        else:
            print(f"[WARNING] Unity Bridge: NOT RESPONDING")
            print(f"   Error: {ping_result.get('error', 'Unknown')}")
            print(f"\n[INFO] Troubleshooting:")
            print(f"   1. Check Unity Console for bridge messages:")
            print(f"      - 'UnityMcpBridge started on port 6400'")
            print(f"      - Any error messages")
            print(f"   2. Install Unity MCP Bridge:")
            print(f"      - Window -> Package Manager")
            print(f"      - + -> Add package from git URL")
            print(f"      - https://github.com/usexless/unity-mcp.git?path=/UnityMcpBridge")
            print(f"   3. Restart Unity Editor")
            print(f"   4. Check Tools -> Unity MCP Bridge menu")

        print(f"[SUCCESS] Server Status: READY")

    else:
        print(f"[ERROR] Unity Connection: FAILED")
        print(f"   Host: {_unity_connection.host}")
        print(f"   Port: {_unity_connection.port}")
        print(f"[WARNING] Make sure:")
        print(f"   - Unity Editor is running")
        print(f"   - Unity MCP Bridge is installed and active")
        print(f"   - Port {_unity_connection.port} is not blocked")
        print(f"[SUCCESS] Server Status: READY (will retry on first request)")

    print("=" * 50)
    return _unity_connection

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Handle server startup and shutdown with enhanced error handling."""
    global _unity_connection

    startup_context = LogContext(operation="server_startup")
    enhanced_logger.info("Unity MCP Server starting up", context=startup_context)

    try:
        # Test Unity connection on startup
        _unity_connection = test_unity_connection()

        try:
            # Yield the connection object for tools to access
            yield {"bridge": _unity_connection}
        finally:
            # Cleanup on shutdown
            shutdown_context = LogContext(operation="server_shutdown")
            enhanced_logger.info("Unity MCP Server shutting down", context=shutdown_context)

            if _unity_connection:
                try:
                    # Log final metrics
                    final_metrics = _unity_connection.get_metrics()
                    enhanced_logger.info(
                        "Final connection metrics",
                        context=shutdown_context,
                        metrics=final_metrics
                    )

                    # Disconnect gracefully
                    _unity_connection.disconnect()
                    enhanced_logger.info("Unity connection closed", context=shutdown_context)
                except Exception as e:
                    enhanced_logger.error(
                        "Error during connection cleanup",
                        context=shutdown_context,
                        exception=e
                    )
                finally:
                    _unity_connection = None

            enhanced_logger.info("Unity MCP Server shut down complete", context=shutdown_context)

    except Exception as e:
        enhanced_logger.critical(
            f"Critical error during server lifecycle: {str(e)}",
            context=startup_context,
            exception=e
        )
        raise

# Initialize MCP server
mcp = FastMCP(
    "unity-mcp-server",
    description="Unity Editor integration via Model Context Protocol",
    lifespan=server_lifespan
)

# Register all tools
register_all_tools(mcp)

# Provide access to Unity connection for tools
def get_unity_connection():
    """Get the current Unity connection instance."""
    return _unity_connection

# Compatibility wrapper for enhanced_connection
def get_enhanced_unity_connection():
    """Compatibility wrapper for tools that expect enhanced connection."""
    return _unity_connection

# Health check tool for monitoring
@mcp.tool()
def health_check(ctx: Context) -> Dict[str, Any]:
    """Check the health status of the Unity MCP Server and Unity connection."""
    try:
        health_context = LogContext(operation="health_check")
        enhanced_logger.info("Health check requested", context=health_context)

        # Get connection metrics
        connection = get_unity_connection()
        metrics = connection.get_metrics() if connection else {}

        # Test connection with ping
        connection_healthy = False
        ping_error = None

        if connection:
            try:
                ping_result = connection.ping()
                connection_healthy = ping_result.get("success", False)
                if connection_healthy:
                    enhanced_logger.info("Health check ping successful", context=health_context)
                else:
                    ping_error = ping_result.get("error", "Ping failed")
            except Exception as e:
                ping_error = str(e)
                enhanced_logger.warning(
                    f"Health check ping failed: {ping_error}",
                    context=health_context,
                    exception=e
                )
        else:
            ping_error = "No connection available"

        # Get timeout manager status
        active_operations = timeout_manager.get_active_operations()

        health_status = {
            "status": "healthy" if connection_healthy else "degraded",
            "timestamp": time.time(),
            "connection": {
                "healthy": connection_healthy,
                "error": ping_error,
                "metrics": metrics
            },
            "operations": {
                "active_count": len(active_operations),
                "active_operations": active_operations
            },
            "server": {
                "version": "2.0.0",
                "config": {
                    "host": getattr(config, 'unity_host', 'localhost'),
                    "port": getattr(config, 'unity_port', 6400),
                    "timeouts_enabled": True,
                    "validation_enabled": getattr(config, 'enable_strict_validation', True),
                    "health_checks_enabled": getattr(config, 'enable_health_checks', True)
                }
            }
        }

        return {
            "success": True,
            "message": f"Health check completed - status: {health_status['status']}",
            "data": health_status
        }

    except Exception as e:
        enhanced_logger.error(
            "Health check failed with unexpected error",
            context=LogContext(operation="health_check"),
            exception=e
        )
        return {
            "success": False,
            "error": f"Health check failed: {str(e)}",
            "data": {
                "status": "unhealthy",
                "timestamp": time.time(),
                "error": str(e)
            }
        }

# Asset Creation Strategy

@mcp.prompt()
def asset_creation_strategy() -> str:
    """Guide for discovering and using Unity MCP tools effectively."""
    return (
        "Available Unity MCP Server Tools:\\n\\n"
        "- `manage_editor`: Controls editor state and queries info.\\n"
        "- `execute_menu_item`: Executes Unity Editor menu items by path.\\n"
        "- `read_console`: Reads or clears Unity console messages, with filtering options.\\n"
        "- `manage_scene`: Manages scenes.\\n"
        "- `manage_gameobject`: Manages GameObjects in the scene.\\n"
        "- `manage_script`: Manages C# script files.\\n"
        "- `manage_asset`: Manages prefabs and assets.\\n"
        "- `manage_shader`: Manages shaders.\\n"
        "- `health_check`: Check server and Unity connection health.\\n\\n"
        "Enhanced Features:\\n"
        "- Robust error handling with detailed error messages\\n"
        "- Operation timeouts to prevent infinite waiting\\n"
        "- Input validation for all parameters\\n"
        "- Comprehensive logging for debugging\\n"
        "- Connection health monitoring and auto-recovery\\n\\n"
        "Tips:\\n"
        "- Create prefabs for reusable GameObjects.\\n"
        "- Always include a camera and main light in your scenes.\\n"
        "- Use health_check tool to monitor connection status.\\n"
    )

# Run the server
if __name__ == "__main__":
    mcp.run(transport='stdio')
