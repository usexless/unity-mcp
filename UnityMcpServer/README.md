# Unity MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Unity 2021.3+](https://img.shields.io/badge/Unity-2021.3+-black.svg)](https://unity.com/)

**Production-ready** Model Context Protocol (MCP) server for Unity Editor automation. Automate Unity with AI assistants like Claude Desktop.

## ✨ Features

- **🔧 8 Unity Tools** - Complete Unity automation toolkit
- **🛡️ Reliable** - Robust error handling and timeout protection
- **📊 Monitoring** - Connection testing and health checks
- **⚡ Easy Setup** - Quick installation and configuration

## 🚀 Setup

### 1. Install Python Server

```bash
git clone https://github.com/usexless/unity-mcp.git
cd unity-mcp/UnityMcpServer
pip install -r requirements.txt
```

### 2. Install Unity Bridge

**Unity Package Manager (Only Method):**
1. Open Unity Package Manager (`Window` → `Package Manager`)
2. Click `+` → `Add package from git URL...`
3. Enter: `https://github.com/usexless/unity-mcp.git?path=/UnityMcpBridge`
4. Click `Add`

**Verify Installation:**
- Unity Console: `Unity MCP Bridge: Server started on port 6400`
- Menu: `Tools` → `Unity MCP Bridge` available

### 3. Start Server & Test

```bash
cd src
python server.py
```

**Expected Output:**
```
✅ Unity Connection: SUCCESS
✅ Unity Bridge: RESPONDING
✅ Server Status: READY
```

**If Bridge Not Responding:**
- Check Unity Console for: `UnityMcpBridge started on port 6400`
- Install bridge via Package Manager (step 2)
- Restart Unity Editor

## 🔧 Claude Desktop Integration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "unity-mcp": {
      "command": "python",
      "args": ["path/to/unity-mcp/UnityMcpServer/src/server.py"],
      "cwd": "path/to/unity-mcp/UnityMcpServer"
    }
  }
}
```

## 🛠️ Available Tools

8 Unity automation tools: `manage_script`, `manage_scene`, `manage_gameobject`, `manage_asset`, `manage_editor`, `manage_shader`, `read_console`, `execute_menu_item`, `health_check`

## 🚨 Troubleshooting

**Unity Bridge Not Responding:**
1. Check Unity Console for: `UnityMcpBridge started on port 6400`
2. Install bridge: Window → Package Manager → + → Add from git URL → `https://github.com/usexless/unity-mcp.git?path=/UnityMcpBridge`
3. Restart Unity Editor
4. Check `Tools` → `Unity MCP Bridge` menu exists

## 💡 Usage Examples

**With Claude Desktop:**
- "Create a PlayerController script in Assets/Scripts/"
- "Load the MainScene and show me the hierarchy"
- "Create a Player GameObject with Rigidbody at position (0,1,0)"
- "Check Unity console for any errors"

---

**🎉 Automate Unity with AI - Fast, Reliable, Production-Ready!**
