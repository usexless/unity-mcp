# Unity MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Unity 2021.3+](https://img.shields.io/badge/Unity-2021.3+-black.svg)](https://unity.com/)

**Production-ready** Model Context Protocol (MCP) server for Unity Editor automation. Provides reliable Unity integration with comprehensive error handling, timeout protection, and monitoring.

## ✨ Key Features

- **🛡️ Reliable Operations** - No infinite waiting, all operations have timeouts
- **🔧 8 Unity Tools** - Script, scene, asset, GameObject, shader, editor, console, menu management
- **📊 Health Monitoring** - Real-time status and performance metrics
- **🌐 Remote Support** - Connect to Unity from anywhere
- **⚡ Fast Setup** - One-command installation and configuration

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/usexless/unity-mcp.git
cd unity-mcp/UnityMcpServer

# Install dependencies
pip install -r requirements.txt
```

### 2. Unity Setup

1. **Install Unity MCP Bridge** in your Unity project:
   - Add the Unity MCP Bridge package to your project
   - Configure connection settings (default: localhost:6400)

2. **Start Unity Editor** with your project

### 3. Start the Server

**Option A: Full Server (Recommended) ✅**
```bash
cd src
python server.py
```
*Features: Enhanced logging, monitoring, validation, connection testing*

**Option B: Simple Server (Basic)**
```bash
cd src
python simple_server.py
```
*Features: Basic functionality, minimal dependencies*

### 4. Test Connection

The server runs via stdio (standard input/output) for MCP protocol communication. To test:

1. **With MCP Client**: Use Claude Desktop or another MCP client
2. **Direct Test**: The server will respond to MCP protocol messages on stdin/stdout

**Health Check**: Use the `health_check` tool through your MCP client to verify Unity connection.

## 🛠️ Available Tools

The server provides 8 Unity automation tools:

| Tool | Description | Example Usage |
|------|-------------|---------------|
| **manage_script** | Create, read, update, delete Unity scripts | Create MonoBehaviour scripts, manage namespaces |
| **manage_scene** | Scene operations and build settings | Load scenes, manage build index, get hierarchy |
| **manage_gameobject** | GameObject manipulation and components | Create objects, set transforms, manage components |
| **manage_asset** | Asset import, export, and management | Import textures, search assets, manage metadata |
| **manage_editor** | Unity Editor state and settings | Change active tool, add tags/layers, editor control |
| **manage_shader** | Shader script creation and management | Create custom shaders, manage shader properties |
| **read_console** | Unity console message retrieval | Get error logs, filter messages, debug information |
| **execute_menu_item** | Execute Unity menu commands | Trigger menu actions, automate workflows |

## 🔧 Configuration

### Basic Configuration

Create `src/config_local.py` to customize settings:

```python
# Network settings
unity_host = "localhost"  # Unity Editor host
unity_port = 6400        # Unity MCP Bridge port
mcp_port = 6500          # MCP server port

# Timeout settings (seconds)
operation_timeouts = {
    "connection": 10.0,
    "script_operation": 30.0,
    "scene_operation": 60.0,
    # ... customize as needed
}

# Features
enable_strict_validation = True
enable_health_checks = True
enable_performance_logging = True
```

### Environment Variables

```bash
# Alternative configuration via environment variables
export UNITY_HOST=localhost
export UNITY_PORT=6400
export MCP_PORT=6500
export LOG_LEVEL=INFO
```

## 💡 Usage Examples

### Script Management
```python
# Create a new MonoBehaviour script
{
  "action": "create",
  "name": "PlayerController",
  "path": "Assets/Scripts/",
  "contents": "using UnityEngine;\n\npublic class PlayerController : MonoBehaviour\n{\n    void Start() { }\n}",
  "script_type": "MonoBehaviour",
  "namespace": "Game"
}
```

### GameObject Operations
```python
# Create a GameObject with components
{
  "action": "create",
  "name": "Player",
  "position": [0, 0, 0],
  "components_to_add": ["Rigidbody", "BoxCollider"],
  "component_properties": {
    "Rigidbody": {"mass": 1.0, "useGravity": true}
  }
}
```

### Scene Management
```python
# Load a scene and get hierarchy
{
  "action": "load",
  "name": "MainScene",
  "path": "Assets/Scenes/"
}
```

## 🔍 Health Monitoring

### Health Check Tool
Use the `health_check` tool through your MCP client:

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "connection": {
      "healthy": true
    },
    "server": {
      "version": "2.0.0"
    }
  }
}
```

## 🧪 Testing

```bash
# Run basic tests
cd src
python test_improvements.py

# Test with Unity (requires Unity Editor running)
python test_integration.py
```

## 🚨 Troubleshooting

### Common Issues

**Connection Refused:**
```
Error: Could not connect to Unity at localhost:6400
```
**Solution:** Verify Unity Editor is running and MCP Bridge is active.

**Timeout Errors:**
```
Error: Operation timed out after 30 seconds
```
**Solution:** Check Unity Editor performance or increase timeout in config.

**Permission Errors:**
```
Error: Access denied to Unity project files
```
**Solution:** Run with appropriate permissions or check file paths.

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)** - Technical details of all changes
- **[FUTURE_DEV_IMPLEMENTATION.md](FUTURE_DEV_IMPLEMENTATION.md)** - Implemented features from roadmap

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🎉 Ready to automate Unity with reliable, production-ready tools!**
