#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unity MCP Server - MCP Client Compatible Version

A Model Context Protocol (MCP) server for Unity Editor automation.
Optimized for MCP clients like Claude Desktop and Augment Code.
"""

import sys
import os

# Set environment variable for UTF-8 encoding on Windows
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from mcp.server.fastmcp import FastMCP, Context, Image
import logging
import time
import socket
import json
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, List

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("unity-mcp-server")

# Initialize FastMCP server
mcp = FastMCP("Unity MCP Server")

# Unity connection class
class UnityConnection:
    def __init__(self, host="localhost", port=6400):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Connect to Unity."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10.0)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to Unity at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.warning(f"Could not connect to Unity: {e}")
            self.connected = False
            return False
    
    def send_command(self, command_data):
        """Send command to Unity and get response."""
        if not self.connected:
            if not self.connect():
                return {"success": False, "error": "Not connected to Unity"}
        
        try:
            # Convert old format to Unity Bridge format if needed
            if "tool" in command_data and "action" in command_data:
                tool_name = command_data.pop("tool")
                params = command_data
                unity_command = {
                    "type": tool_name,
                    "params": params
                }
            else:
                unity_command = command_data
            
            # Send command
            command_json = json.dumps(unity_command)
            self.socket.send(command_json.encode('utf-8') + b'\n')
            
            # Receive response
            response_data = self.socket.recv(4096).decode('utf-8')
            response = json.loads(response_data)
            
            # Convert to old format for compatibility
            if response.get("status") == "success":
                return {"success": True, "data": response.get("result", {})}
            else:
                return {"success": False, "error": response.get("error", "Unknown error")}
                
        except Exception as e:
            logger.error(f"Unity command failed: {e}")
            self.connected = False
            return {"success": False, "error": str(e)}
    
    def disconnect(self):
        """Disconnect from Unity."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False

# Global Unity connection
unity_connection = UnityConnection()

# Health check tool
@mcp.tool()
def health_check() -> Dict[str, Any]:
    """Check the health status of the Unity MCP Server and Unity connection."""
    try:
        logger.info("Health check requested")
        
        # Test Unity connection
        connection_healthy = unity_connection.connected
        if not connection_healthy:
            connection_healthy = unity_connection.connect()
        
        # Test ping if connected
        ping_result = None
        if connection_healthy:
            try:
                unity_connection.socket.send(b'ping')
                response_data = unity_connection.socket.recv(4096).decode('utf-8')
                ping_result = json.loads(response_data)
                connection_healthy = ping_result.get("status") == "success"
            except:
                connection_healthy = False
        
        health_data = {
            "status": "healthy" if connection_healthy else "degraded",
            "connection": {
                "healthy": connection_healthy,
                "host": unity_connection.host,
                "port": unity_connection.port
            },
            "server": {
                "version": "2.0.0"
            }
        }
        
        if ping_result:
            health_data["ping_response"] = ping_result
        
        logger.info(f"Health check completed - Status: {health_data['status']}")
        
        return {
            "success": True,
            "data": health_data
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Unity tool implementations
@mcp.tool()
def manage_script(action: str, name: str, path: str, contents: str, script_type: str, namespace: str) -> Dict[str, Any]:
    """Manages C# scripts in Unity (create, read, update, delete)."""
    try:
        command_data = {
            "tool": "manage_script",
            "action": action,
            "name": name,
            "path": path,
            "contents": contents,
            "script_type": script_type,
            "namespace": namespace
        }
        
        logger.info(f"Script operation: {action} - {name}")
        response = unity_connection.send_command(command_data)
        
        if response.get("success"):
            logger.info(f"Script operation completed successfully")
        else:
            logger.error(f"Script operation failed: {response.get('error', 'Unknown error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Script management error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def manage_scene(action: str, name: str, path: str, build_index: int) -> Dict[str, Any]:
    """Manages Unity scenes (load, save, create, get hierarchy, etc.)."""
    try:
        command_data = {
            "tool": "manage_scene",
            "action": action,
            "name": name,
            "path": path,
            "build_index": build_index
        }
        
        logger.info(f"Scene operation: {action} - {name}")
        response = unity_connection.send_command(command_data)
        
        if response.get("success"):
            logger.info(f"Scene operation completed successfully")
        else:
            logger.error(f"Scene operation failed: {response.get('error', 'Unknown error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Scene management error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def manage_editor(action: str, tool_name: str = None, tag_name: str = None, layer_name: str = None, wait_for_completion: bool = None) -> Dict[str, Any]:
    """Controls and queries the Unity editor's state and settings."""
    try:
        command_data = {
            "tool": "manage_editor",
            "action": action,
            "tool_name": tool_name,
            "tag_name": tag_name,
            "layer_name": layer_name,
            "wait_for_completion": wait_for_completion
        }
        
        logger.info(f"Editor operation: {action}")
        response = unity_connection.send_command(command_data)
        
        if response.get("success"):
            logger.info(f"Editor operation completed successfully")
        else:
            logger.error(f"Editor operation failed: {response.get('error', 'Unknown error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Editor management error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def manage_gameobject(action: str, target: str = None, search_method: str = None, name: str = None, 
                     position: list = None, rotation: list = None, scale: list = None,
                     components_to_add: list = None, component_properties: dict = None) -> Dict[str, Any]:
    """Manages GameObjects: create, modify, delete, find, and component operations."""
    try:
        command_data = {
            "tool": "manage_gameobject",
            "action": action,
            "target": target,
            "search_method": search_method,
            "name": name,
            "position": position,
            "rotation": rotation,
            "scale": scale,
            "components_to_add": components_to_add,
            "component_properties": component_properties
        }
        
        logger.info(f"GameObject operation: {action}")
        response = unity_connection.send_command(command_data)
        
        if response.get("success"):
            logger.info(f"GameObject operation completed successfully")
        else:
            logger.error(f"GameObject operation failed: {response.get('error', 'Unknown error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"GameObject management error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def manage_asset(action: str, path: str, asset_type: str = None, properties: dict = None) -> Dict[str, Any]:
    """Performs asset operations (import, create, modify, delete, etc.) in Unity."""
    try:
        command_data = {
            "tool": "manage_asset",
            "action": action,
            "path": path,
            "asset_type": asset_type,
            "properties": properties
        }
        
        logger.info(f"Asset operation: {action} - {path}")
        response = unity_connection.send_command(command_data)
        
        if response.get("success"):
            logger.info(f"Asset operation completed successfully")
        else:
            logger.error(f"Asset operation failed: {response.get('error', 'Unknown error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Asset management error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def read_console(action: str = "get", types: list = None, count: int = None) -> Dict[str, Any]:
    """Gets messages from or clears the Unity Editor console."""
    try:
        command_data = {
            "tool": "read_console",
            "action": action,
            "types": types,
            "count": count
        }
        
        logger.info(f"Console operation: {action}")
        response = unity_connection.send_command(command_data)
        
        if response.get("success"):
            logger.info(f"Console operation completed successfully")
        else:
            logger.error(f"Console operation failed: {response.get('error', 'Unknown error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Console operation error: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def execute_menu_item(menu_path: str, action: str = "execute") -> Dict[str, Any]:
    """Executes a Unity Editor menu item via its path."""
    try:
        command_data = {
            "tool": "execute_menu_item",
            "menu_path": menu_path,
            "action": action
        }
        
        logger.info(f"Menu operation: {menu_path}")
        response = unity_connection.send_command(command_data)
        
        if response.get("success"):
            logger.info(f"Menu operation completed successfully")
        else:
            logger.error(f"Menu operation failed: {response.get('error', 'Unknown error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Menu operation error: {e}")
        return {"success": False, "error": str(e)}

logger.info("Unity MCP Server (MCP Client Compatible) initialized")

if __name__ == "__main__":
    # Start the MCP server
    mcp.run(transport='stdio')
