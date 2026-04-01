const { app, BrowserWindow, screen, ipcMain, globalShortcut } = require('electron');
const path = require('path');

const PET_CONFIGS = [
  { id: 'pet-1', name: '보라', color: '#7C6FF7' },
  { id: 'pet-2', name: '민트', color: '#4ECDC4' },
  { id: 'pet-3', name: '코랄', color: '#FF6B6B' },
];

let petWindow = null;
let appWindow = null;

// Track pet states in main process
let petStates = PET_CONFIGS.map((c, i) => ({
  ...c,
  state: 'idle', // idle, working, gone
  returnedAt: Date.now() - i * 1000,
}));

function createPetWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  petWindow = new BrowserWindow({
    width: 300,
    height: 280,
    x: width - 320,
    y: height - 300,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    resizable: false,
    skipTaskbar: true,
    hasShadow: false,
    focusable: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  petWindow.loadFile('pet.html');
  petWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });

  petWindow.webContents.once('did-finish-load', () => {
    petWindow.webContents.send('init-pets', PET_CONFIGS);
  });

  petWindow.on('closed', () => { petWindow = null; });
}

function createAppWindow() {
  if (appWindow) { appWindow.focus(); return; }

  appWindow = new BrowserWindow({
    width: 700,
    height: 550,
    title: 'Desktop Pet Office',
    frame: true,
    resizable: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  appWindow.loadFile('office.html');
  appWindow.on('closed', () => { appWindow = null; });
}

function getIdlePetsByRecent() {
  return petStates
    .filter(p => p.state === 'idle')
    .sort((a, b) => b.returnedAt - a.returnedAt);
}

app.whenReady().then(() => {
  createPetWindow();

  // Cmd+Shift+Space → chat with front pet
  globalShortcut.register('CommandOrControl+Shift+Space', () => {
    const idle = getIdlePetsByRecent();
    if (idle.length === 0 || !petWindow) return;

    petWindow.setFocusable(true);
    petWindow.focus();
    petWindow.webContents.send('open-chat', idle[0].id);
  });

  // Cmd+Shift+A → summon all to front
  globalShortcut.register('CommandOrControl+Shift+A', () => {
    if (petWindow) petWindow.webContents.send('summon-all');
  });
});

app.on('window-all-closed', () => {});
app.on('will-quit', () => { globalShortcut.unregisterAll(); });

// --- IPC ---

ipcMain.on('chat-closed', () => {
  if (petWindow) {
    petWindow.setFocusable(false);
    petWindow.blur();
  }
});

ipcMain.on('start-task', (event, { petId, message }) => {
  const pet = petStates.find(p => p.id === petId);
  if (!pet) return;

  pet.state = 'working';

  // Tell pet scene
  if (petWindow) {
    petWindow.webContents.send('pet-run-away', petId);
  }

  if (!appWindow) createAppWindow();

  setTimeout(() => {
    if (appWindow) {
      appWindow.webContents.send('task-started', { petId, petName: pet.name, petColor: pet.color, message });
    }
  }, 1000);

  const duration = 5000 + Math.random() * 2000; // 5~7초
  setTimeout(() => {
    if (appWindow) {
      appWindow.webContents.send('task-done', { petId, petName: pet.name, message });
    }

    setTimeout(() => {
      pet.state = 'idle';
      pet.returnedAt = Date.now();

      if (petWindow) {
        petWindow.webContents.send('pet-come-back', { petId, message: `"${message}" 다 했어! ✅` });
      }
    }, 1500);
  }, duration);
});

ipcMain.on('open-office', () => { createAppWindow(); });
