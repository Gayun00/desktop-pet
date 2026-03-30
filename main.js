const { app, BrowserWindow, screen, ipcMain, Tray, nativeImage } = require('electron');
const path = require('path');

let petWindow;   // desktop pet (transparent overlay)
let appWindow;   // workspace window (the "office")

function createPetWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  petWindow = new BrowserWindow({
    width: 300,
    height: 400,
    x: width - 350,
    y: height - 450,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    resizable: false,
    skipTaskbar: false,
    hasShadow: false,
    focusable: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  petWindow.loadFile('pet.html');
  petWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });

  petWindow.on('closed', () => {
    petWindow = null;
  });
}

function createAppWindow() {
  if (appWindow) {
    appWindow.focus();
    return;
  }

  appWindow = new BrowserWindow({
    width: 600,
    height: 500,
    title: 'Desktop Pet Office',
    frame: true,
    resizable: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  appWindow.loadFile('office.html');

  appWindow.on('closed', () => {
    appWindow = null;
  });
}

app.whenReady().then(() => {
  createPetWindow();
});

// macOS: don't quit when all windows close
app.on('window-all-closed', (e) => {
  // Do nothing — keep app alive
});

// Reopen pet window if activated with no windows
app.on('activate', () => {
  if (!petWindow) {
    createPetWindow();
  }
});

// --- IPC handlers ---

// User sent a message → pet runs away, start working
ipcMain.on('start-task', (event, message) => {
  // Tell pet to run away
  if (petWindow) {
    petWindow.webContents.send('run-away');
  }

  // Open/update office window
  if (!appWindow) {
    createAppWindow();
  }

  // Wait for pet to finish running animation, then tell office to start
  setTimeout(() => {
    if (appWindow) {
      appWindow.webContents.send('task-started', message);
    }
  }, 1000);

  // Simulate task completion after 5 seconds
  setTimeout(() => {
    if (appWindow) {
      appWindow.webContents.send('task-done', message);
    }

    // Pet comes back
    setTimeout(() => {
      if (petWindow) {
        petWindow.webContents.send('come-back', `"${message}" 다 했어! ✅`);
      } else {
        createPetWindow();
        petWindow.webContents.once('did-finish-load', () => {
          petWindow.webContents.send('come-back', `"${message}" 다 했어! ✅`);
        });
      }
    }, 1500);
  }, 6000);
});

// Open office window
ipcMain.on('open-office', () => {
  createAppWindow();
});
