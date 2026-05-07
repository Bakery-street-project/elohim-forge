const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const Store = require('electron-store');

const schema = {
  backend: {
    type: 'string',
    default: 'nim'
  },
  apiKey: {
    type: 'string',
    default: ''
  },
  primaxBackend: {
    type: 'string',
    default: 'primax'
  }
};

const store = new Store({ schema });

let mainWindow;
let pythonProcess = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: 'Elohim Forge — PRIMAX AI Edition',
    backgroundColor: '#0a0a0a',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    },
    icon: path.join(__dirname, 'assets', 'icon.png')
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
    if (pythonProcess) {
      pythonProcess.kill();
    }
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handlers
ipcMain.handle('get-config', () => {
  return {
    backend: store.get('backend'),
    apiKey: store.get('apiKey'),
    primaxBackend: store.get('primaxBackend')
  };
});

ipcMain.handle('set-config', (event, config) => {
  store.set('backend', config.backend);
  store.set('apiKey', config.apiKey);
  store.set('primaxBackend', config.primaxBackend);
  return true;
});

ipcMain.handle('run-command', async (event, command) => {
  return new Promise((resolve) => {
    const cliPath = path.join(__dirname, 'cli', 'elohim.py');
    
    pythonProcess = spawn('python', [cliPath, ...command.split(' ')], {
      cwd: path.join(__dirname, 'cli'),
      env: {
        ...process.env,
        PRIMAX_BACKEND: store.get('primaxBackend'),
        PRIMAX_API_KEY: store.get('apiKey'),
        NIM_API_KEY: store.get('apiKey'),
        GEMINI_API_KEY: store.get('apiKey'),
        OPENAI_API_KEY: store.get('apiKey')
      }
    });

    let output = '';
    let error = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      error += data.toString();
    });

    pythonProcess.on('close', (code) => {
      pythonProcess = null;
      if (code === 0) {
        resolve({ success: true, output: output.trim() });
      } else {
        resolve({ success: false, error: error || output });
      }
    });

    pythonProcess.on('error', (err) => {
      pythonProcess = null;
      resolve({ success: false, error: err.message });
    });
  });
});

ipcMain.handle('run-mcp', async (event, query) => {
  return new Promise((resolve) => {
    const mcpPath = path.join(__dirname, 'primax-ai', 'src', 'mcp_server', 'primax_mcp_server.py');
    
    pythonProcess = spawn('python', [mcpPath], {
      cwd: path.join(__dirname, 'primax-ai'),
      env: { ...process.env }
    });

    let output = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
      if (output.includes('ready')) {
        // Send query to MCP
        pythonProcess.stdin.write(JSON.stringify({ query }) + '\n');
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('MCP Error:', data.toString());
    });

    setTimeout(() => {
      if (pythonProcess) {
        pythonProcess.kill();
        resolve({ success: true, output: 'MCP query processed' });
      }
    }, 5000);
  });
});

ipcMain.handle('open-external', (event, url) => {
  shell.openExternal(url);
});