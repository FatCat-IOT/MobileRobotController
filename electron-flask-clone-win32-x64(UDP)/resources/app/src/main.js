const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const ping = require('ping');
const fs = require('fs');

let win;

// Load configuration from config.json (in same folder)
const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

console.log('Master IP:', config.master_ip);
console.log('Slave IP:', config.slave_ip);

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false
    },
  });

  win.loadFile(path.join(__dirname, 'views', 'login.html'));
}

app.whenReady().then(() => {
  createWindow();
});

// Handle login from renderer
ipcMain.handle('login', async (event, { username, password }) => {
  if (username === 'danny' && password === '123') {
    win.loadFile(path.join(__dirname, 'views', 'index.html'));
    return { success: true };
  } else {
    return { success: false, message: 'Invalid credentials' };
  }
});

// Handle ping requests from renderer
ipcMain.handle('ping', async (event, ip) => {
  const res = await ping.promise.probe(ip);
  return res;
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
