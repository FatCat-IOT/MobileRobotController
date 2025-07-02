const { contextBridge, ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

// ✅ Same folder as preload.js
const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

contextBridge.exposeInMainWorld('appConfig', config);
contextBridge.exposeInMainWorld('electron', {
  invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args)
});
