# Unity MCP Bridge - Installation Guide

## 🚀 **Schritt-für-Schritt Installation**

Die Unity MCP Bridge ist erforderlich, damit der MCP Server mit Unity kommunizieren kann.

### **Methode 1: Manueller Copy (Empfohlen) ✅**

1. **Navigiere zu deinem Unity Projekt:**
```bash
cd "D:\dein\unity\projekt\pfad"
```

2. **Kopiere die Bridge aus dem Repository:**
```bash
# Von diesem Repository
xcopy "D:\unity\VoiceGame\unity-mcp\UnityMcpBridge" "Assets\UnityMcpBridge" /E /I

# ODER von temporärem Ordner (falls kopiert)
xcopy "D:\temp\UnityMcpBridge_Install" "Assets\UnityMcpBridge" /E /I
```

3. **Unity öffnen/neu laden:**
   - Unity wird automatisch die neuen Skripte importieren
   - Warte bis die Kompilierung abgeschlossen ist

### **Methode 2: Unity Package Manager**

1. **Unity Package Manager öffnen:**
   - `Window` → `Package Manager`

2. **Package hinzufügen:**
   - Klicke auf `+` (oben links)
   - Wähle `Add package from git URL...`

3. **Git URL eingeben:**
```
https://github.com/usexless/unity-mcp.git?path=/UnityMcpBridge
```

4. **Add klicken** und warten bis Installation abgeschlossen

### **Methode 3: Direkte Datei-Kopie**

1. **Download das Repository:**
```bash
git clone https://github.com/usexless/unity-mcp.git
cd unity-mcp
```

2. **Kopiere UnityMcpBridge Ordner:**
   - Kopiere den gesamten `UnityMcpBridge` Ordner
   - Füge ihn in dein Unity Projekt unter `Assets/` ein

## ✅ **Installation Verifizieren**

### **1. Unity Console prüfen:**
Nach der Installation solltest du in der Unity Console sehen:
```
Unity MCP Bridge: Initialized
Unity MCP Bridge: Server started on port 6400
Unity MCP Bridge: Ready for connections
```

### **2. Unity Menu prüfen:**
- Gehe zu `Tools` → `Unity MCP Bridge`
- Du solltest das MCP Bridge Fenster sehen können

### **3. Server-Test:**
```bash
cd UnityMcpServer/src
python server.py
```

**Erwartete Ausgabe:**
```
🔍 Testing Unity Connection...
==================================================
✅ Unity Connection: SUCCESS
   Host: localhost
   Port: 6400
✅ Unity Bridge: RESPONDING  # <-- Das sollte jetzt funktionieren!
✅ Server Status: READY
==================================================
```

## 🔧 **Konfiguration**

### **Standard-Konfiguration:**
- **Host:** localhost
- **Port:** 6400
- **Auto-Start:** Aktiviert

### **Konfiguration ändern:**
1. **Unity MCP Bridge Fenster öffnen:**
   - `Tools` → `Unity MCP Bridge`

2. **Einstellungen anpassen:**
   - Host/Port ändern falls nötig
   - Auto-Start aktivieren/deaktivieren

## 🚨 **Troubleshooting**

### **Problem: Bridge startet nicht**
**Lösung:**
1. Unity Console auf Fehlermeldungen prüfen
2. Unity neu starten
3. Projekt neu kompilieren (`Assets` → `Reimport All`)

### **Problem: Port 6400 bereits belegt**
**Lösung:**
1. Anderen Port in Bridge-Konfiguration wählen
2. Server-Konfiguration entsprechend anpassen:
```python
# In config.py oder als Umgebungsvariable
unity_port = 6401  # Neuer Port
```

### **Problem: "Connection Refused"**
**Lösung:**
1. Unity läuft und Projekt ist geladen
2. Bridge ist installiert und aktiv
3. Firewall blockiert Port nicht
4. Kein anderer Prozess verwendet Port 6400

### **Problem: "Bridge Not Responding"**
**Lösung:**
1. Unity Console prüfen auf Bridge-Nachrichten
2. Bridge manuell starten: `Tools` → `Unity MCP Bridge` → `Start Server`
3. Unity neu starten

## 📁 **Dateistruktur nach Installation**

```
YourUnityProject/
├── Assets/
│   ├── UnityMcpBridge/
│   │   ├── Editor/
│   │   │   ├── UnityMcpBridge.cs
│   │   │   ├── Tools/
│   │   │   ├── Windows/
│   │   │   └── ...
│   │   ├── Runtime/
│   │   └── package.json
│   └── ...
```

## 🎯 **Nächste Schritte**

1. **Installation abschließen** (eine der obigen Methoden)
2. **Unity neu starten** um sicherzustellen, dass alles geladen ist
3. **Server testen:** `python server.py`
4. **Bei Erfolg:** Integration mit Claude Desktop
5. **Unity-Automatisierung genießen!**

## 💡 **Tipps**

- **Auto-Start aktivieren:** Bridge startet automatisch mit Unity
- **Console überwachen:** Wichtige Statusmeldungen werden dort angezeigt
- **Port-Konflikte vermeiden:** Standard-Port 6400 ist meist frei
- **Firewall-Ausnahme:** Falls nötig, Port 6400 in Firewall freigeben

---

**Nach erfolgreicher Installation sollte der Server-Test zeigen:**
```
✅ Unity Bridge: RESPONDING
```

**Dann ist alles bereit für die Unity-Automatisierung!** 🚀
