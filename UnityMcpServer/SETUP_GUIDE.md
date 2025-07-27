# Unity MCP Server - Setup Guide

## 🚀 How to Use Unity MCP Server

This guide explains how to set up and use the Unity MCP Server for Unity automation.

## Prerequisites

- **Python 3.8+** installed on your system
- **Unity 2021.3+** with a project open
- **Network connection** between Python and Unity

## Step 1: Install the Server

```bash
# Clone the repository
git clone https://github.com/usexless/unity-mcp.git
cd unity-mcp/UnityMcpServer

# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Unity Setup

### Option A: Manual Unity Bridge Setup
1. Copy the `UnityMcpBridge` folder to your Unity project's `Assets/` directory
2. Unity will automatically import the bridge scripts
3. The bridge will start automatically when Unity runs

### Option B: Package Manager (if available)
1. Open Unity Package Manager
2. Add package from git URL: `https://github.com/usexless/unity-mcp-bridge.git`
3. Import the package

## Step 3: Start the Server

```bash
# Navigate to the server directory
cd src

# Start the MCP server
python server.py
```

You should see output like:
```
Unity MCP Server starting...
Server listening on port 6500
Waiting for Unity connection on port 6400...
```

## Step 4: Connect Unity

1. **Start Unity Editor** with your project
2. **Check Console** - you should see: `Unity MCP Bridge: Connected to server`
3. **Verify Connection** - the server should show: `Unity connected successfully`

## Step 5: Test the Connection

### Health Check
```bash
curl http://localhost:6500/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "connection": {"healthy": true}
  }
}
```

### Test a Simple Operation
You can test the server by using it with an LLM client or by making direct HTTP requests.

## Using with LLM Clients

### Claude Desktop
Add to your Claude Desktop configuration:
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

### Other MCP Clients
The server implements the standard MCP protocol and works with any MCP-compatible client.

## Available Operations

Once connected, you can use these tools:

### Script Management
- Create new C# scripts
- Read existing script content
- Update script files
- Delete scripts

### Scene Operations
- Load different scenes
- Get scene hierarchy
- Manage build settings

### GameObject Manipulation
- Create GameObjects
- Modify transforms
- Add/remove components
- Set component properties

### Asset Management
- Import assets
- Search project assets
- Get asset information
- Manage asset metadata

### Editor Control
- Change active tools
- Add tags and layers
- Execute menu commands
- Read console messages

## Configuration

### Basic Configuration
Create `src/config_local.py`:
```python
# Network settings
unity_host = "localhost"
unity_port = 6400
mcp_port = 6500

# Timeout settings
operation_timeouts = {
    "connection": 10.0,
    "script_operation": 30.0,
    "scene_operation": 60.0
}

# Features
enable_strict_validation = True
enable_health_checks = True
```

### Environment Variables
```bash
export UNITY_HOST=localhost
export UNITY_PORT=6400
export MCP_PORT=6500
export LOG_LEVEL=INFO
```

## Troubleshooting

### Unity Not Connecting
1. **Check Unity Console** for MCP Bridge messages
2. **Verify Port 6400** is not blocked by firewall
3. **Restart Unity** if the bridge doesn't start
4. **Check Unity Project** has the MCP Bridge scripts

### Server Connection Issues
1. **Check Port 6500** is available
2. **Verify Python Dependencies** are installed
3. **Check Firewall Settings** allow Python network access
4. **Review Server Logs** for error messages

### Operation Timeouts
1. **Increase Timeouts** in configuration
2. **Check Unity Performance** - complex operations take longer
3. **Verify Unity is Responsive** - not frozen or busy

### Permission Errors
1. **Run with Admin Rights** if accessing system directories
2. **Check File Permissions** in Unity project
3. **Verify Unity Project Path** is accessible

## Advanced Usage

### Remote Connections
To connect from a different machine:
1. Change `unity_host` in configuration
2. Ensure network connectivity between machines
3. Configure firewall rules for ports 6400 and 6500

### Multiple Unity Instances
Each Unity instance needs a unique port:
1. Configure different `unity_port` for each instance
2. Start separate server instances with different configurations
3. Use different MCP server ports for each

### Production Deployment
For production use:
1. Use proper logging configuration
2. Set up monitoring and health checks
3. Configure automatic restart on failure
4. Use environment variables for configuration

## Example Workflows

### Automated Script Creation
```python
# Create a new player controller script
{
  "tool": "manage_script",
  "action": "create",
  "name": "PlayerController",
  "path": "Assets/Scripts/Player/",
  "script_type": "MonoBehaviour",
  "contents": "using UnityEngine;\n\npublic class PlayerController : MonoBehaviour\n{\n    public float speed = 5f;\n    \n    void Update()\n    {\n        // Movement logic here\n    }\n}"
}
```

### Scene Setup Automation
```python
# Load a scene and create objects
{
  "tool": "manage_scene",
  "action": "load",
  "name": "GameScene"
}

{
  "tool": "manage_gameobject",
  "action": "create",
  "name": "Player",
  "position": [0, 1, 0],
  "components_to_add": ["CharacterController", "PlayerController"]
}
```

### Asset Pipeline Automation
```python
# Import and configure assets
{
  "tool": "manage_asset",
  "action": "import",
  "path": "Assets/Textures/player_texture.png",
  "properties": {
    "textureType": "Sprite",
    "filterMode": "Point"
  }
}
```

## Next Steps

1. **Explore the Tools** - Try different operations with your Unity project
2. **Integrate with LLM** - Use with Claude, ChatGPT, or other AI assistants
3. **Automate Workflows** - Create scripts for repetitive Unity tasks
4. **Customize Configuration** - Adjust timeouts and settings for your needs
5. **Monitor Performance** - Use health checks and logging for production use

## Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the main README and other docs
- **Community**: Share your use cases and improvements

---

**🎉 You're ready to automate Unity with the MCP Server!**
