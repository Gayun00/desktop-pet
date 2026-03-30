const { app, BrowserWindow, screen, ipcMain, globalShortcut } = require('electron');
const path = require('path');

// --- Pet definitions ---
const PET_CONFIGS = [
  { id: 'pet-1', name: '보라', color: '#7C6FF7', offsetX: 0 },
  { id: 'pet-2', name: '민트', color: '#4ECDC4', offsetX: 320 },
  { id: 'pet-3', name: '코랄', color: '#FF6B6B', offsetX: 640 },
];

let pets = [];       // { id, name, color, window, state, returnedAt }
let appWindow = null;

function createPetWindow(config) {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  const win = new BrowserWindow({
    width: 160,
    height: 280,
    x: width - 180 - config.offsetX * 0.55,
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

  win.loadFile('pet.html');
  win.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });

  // Send config after load
  win.webContents.once('did-finish-load', () => {
    win.webContents.send('init-pet', config);
  });

  const pet = {
    id: config.id,
    name: config.name,
    color: config.color,
    window: win,
    state: 'idle',      // idle, working, gone
    returnedAt: Date.now(),
  };

  win.on('closed', () => {
    pet.window = null;
  });

  return pet;
}

function createAppWindow() {
  if (appWindow) {
    appWindow.focus();
    return;
  }

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

  appWindow.on('closed', () => {
    appWindow = null;
  });
}

// --- Get idle pets sorted by most recently returned ---
function getIdlePetsByRecent() {
  return pets
    .filter(p => p.state === 'idle' && p.window)
    .sort((a, b) => b.returnedAt - a.returnedAt);
}

// --- App ready ---
app.whenReady().then(() => {
  // Create all 3 pets
  PET_CONFIGS.forEach(config => {
    pets.push(createPetWindow(config));
  });

  // Global shortcut: Cmd+Shift+Space → focus most recently returned pet
  globalShortcut.register('CommandOrControl+Shift+Space', () => {
    const idlePets = getIdlePetsByRecent();
    if (idlePets.length > 0) {
      const pet = idlePets[0];
      if (pet.window) {
        pet.window.setFocusable(true);
        pet.window.focus();
        pet.window.webContents.send('open-chat');
      }
    }
  });
});

app.on('window-all-closed', () => {
  // Do nothing — keep app alive
});

app.on('activate', () => {
  // Recreate pets if needed
  pets.forEach((pet, i) => {
    if (!pet.window) {
      const newPet = createPetWindow(PET_CONFIGS[i]);
      Object.assign(pet, { window: newPet.window });
    }
  });
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});

// --- IPC handlers ---

// Chat closed → make window unfocusable again
ipcMain.on('chat-closed', (event) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  if (win) {
    win.setFocusable(false);
    win.blur();
  }
});

// Pet sends a task
ipcMain.on('start-task', (event, { petId, message }) => {
  const pet = pets.find(p => p.id === petId);
  if (!pet) return;

  pet.state = 'working';

  // Tell pet to run away
  if (pet.window) {
    pet.window.webContents.send('run-away');
  }

  // Open office
  if (!appWindow) {
    createAppWindow();
  }

  // Tell office about new task
  setTimeout(() => {
    if (appWindow) {
      appWindow.webContents.send('task-started', { petId, petName: pet.name, petColor: pet.color, message });
    }
  }, 1000);

  // Simulate task completion after 15-25 seconds (random)
  const duration = 15000 + Math.random() * 10000;
  setTimeout(() => {
    if (appWindow) {
      appWindow.webContents.send('task-done', { petId, petName: pet.name, message });
    }

    // Pet comes back
    setTimeout(() => {
      pet.state = 'idle';
      pet.returnedAt = Date.now();

      if (pet.window) {
        pet.window.webContents.send('come-back', `"${message}" 다 했어! ✅`);
      }
    }, 1500);
  }, duration);
});

ipcMain.on('open-office', () => {
  createAppWindow();
});
