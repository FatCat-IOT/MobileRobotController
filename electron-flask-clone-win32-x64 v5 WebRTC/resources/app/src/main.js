const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const WebSocket = require('ws');
const ping = require('ping');
const fs = require('fs');

let win;
const WS_PORT = 8082;

// ✅ Load configuration from config.json (in same folder)
const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

console.log('Master IP:', config.master_ip);
console.log('Slave IP:', config.slave_ip);

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),  // ✅ Correct path
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false
    },
  });

  // ✅ Correct path to login.html
  win.loadFile(path.join(__dirname, 'views', 'login.html'));
}

app.whenReady().then(() => {
  createWindow();

  // ✅ WebSocket server for WebRTC signaling
  const wsServer = new WebSocket.Server({ port: WS_PORT, host: '0.0.0.0' });

  wsServer.on('connection', (ws) => {
    console.log('WebSocket client connected');
    ws.on('message', (msg) => {
      // ✅ Broadcast signaling messages to all other clients
      wsServer.clients.forEach(client => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(msg);
        }
      });
    });
  });

  console.log(`WebSocket signaling server listening on ws://localhost:${WS_PORT}`);
});

// ✅ Handle login from renderer
ipcMain.handle('login', async (event, { username, password }) => {
  if (username === 'danny' && password === '123') {
    win.loadFile(path.join(__dirname, 'views', 'index.html')); // ✅ Correct path
    return { success: true };
  } else {
    return { success: false, message: 'Invalid credentials' };
  }
});

// ✅ Handle ping requests from renderer
ipcMain.handle('ping', async (event, ip) => {
  const res = await ping.promise.probe(ip);
  return res;
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
