// The built directory structure
//
// ├─┬ dist-electron
// │ ├─┬ main
// │ │ └── index.js    > Electron-Main
// │ └─┬ preload
// │   └── index.js    > Preload-Scripts
// ├─┬ dist
// │ └── index.html    > Electron-Renderer
//
process.env.DIST_ELECTRON = join(__dirname, "..");
process.env.DIST = join(process.env.DIST_ELECTRON, "../../dist");
process.env.PUBLIC = app.isPackaged
  ? process.env.DIST
  : join(process.env.DIST_ELECTRON, "../../public");

import {
  app,
  BrowserWindow,
  ipcMain,
  Menu,
  MenuItemConstructorOptions,
  shell,
  Tray,
} from "electron";
import { release } from "os";
import { join } from "path";
import {
  Auth,
  callService,
  Connection,
  createConnection,
  createLongLivedTokenAuth,
  HassConfig,
  HassEntities,
  HassServices,
  subscribeConfig,
  subscribeEntities,
  subscribeServices,
} from "home-assistant-js-websocket";
import open from "open";
import settings from "electron-settings";

globalThis.WebSocket = require("ws");

// Disable GPU Acceleration for Windows 7
if (release().startsWith("6.1")) app.disableHardwareAcceleration();

// Set application name for Windows 10+ notifications
if (process.platform === "win32") app.setAppUserModelId(app.getName());

if (!app.requestSingleInstanceLock()) {
  app.quit();
  process.exit(0);
}

let win: BrowserWindow | null = null,
  tray: Tray = null;
// Here, you can also use other preload
const preload = join(__dirname, "../preload/index.js");
const url = process.env.VITE_DEV_SERVER_URL;
const indexHtml = join(process.env.DIST, "index.html");

async function createTray(): Promise<void> {
  const path = join(
    process.env.PUBLIC,
    `logo-white.${process.platform === "win32" ? "ico" : "png"}`
  );
  console.log("Logo Path:", path);
  tray = new Tray(path);
  tray.setToolTip("Home Assistant Desktop");
  tray.on("click", () => {
    tray.popUpContextMenu();
  });
  updateMenu();
}

async function createSettingsWindow(): Promise<void> {
  win = new BrowserWindow({
    title: "Settings",
    icon: join(
      process.env.PUBLIC,
      `logo-white.${process.platform === "win32" ? "ico" : "png"}`
    ),
    webPreferences: {
      preload,
      contextIsolation: false,
      nodeIntegration: true,
    },
    autoHideMenuBar: true,
    width: 1920,
    height: 1080,
  });

  if (app.isPackaged) {
    win.loadFile(indexHtml);
  } else {
    win.loadURL(url);
    win.webContents.openDevTools();
  }

  // Test actively push message to the Electron-Renderer
  win.webContents.on("did-finish-load", () => {
    win?.webContents.send("main-process-message", new Date().toLocaleString());
  });

  // Make all links open with the browser, not with the application
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("https:")) shell.openExternal(url);
    return { action: "deny" };
  });
}

app.whenReady().then(createTray);

app.on("window-all-closed", () => {
  win = null;
  // if (process.platform !== "darwin") app.quit();
});

app.on("second-instance", () => {
  if (win) {
    // Focus on the main window if the user tried to open another
    if (win.isMinimized()) win.restore();
    win.focus();
  }
});

app.on("activate", () => {
  const allWindows = BrowserWindow.getAllWindows();
  if (allWindows.length) {
    allWindows[0].focus();
  } else {
    createSettingsWindow();
  }
});

ipcMain.handle("open-win", (_event, arg) => {
  const childWindow = new BrowserWindow({
    webPreferences: {
      preload,
    },
  });

  if (app.isPackaged) {
    childWindow.loadFile(indexHtml, { hash: arg });
  } else {
    childWindow.loadURL(`${url}/#${arg}`);
    childWindow.webContents.openDevTools({ mode: "undocked", activate: true });
  }
});

// ----------------------------------------
// Settings
// ----------------------------------------
const defaultSettings = {
  autostart: false,
  logLevel: "INFO",
  homeAssistantSecure: false,
  homeAssistantHost: "homeassistant.local",
  homeAssistantPort: 8123,
  homeAssistantToken: "",
  homeAssistantSubscribedEntites: [],
};

async function getSetting(key: string): Promise<any> {
  return (await settings.get(key)) || defaultSettings[key];
}

async function getSettings(keys: Array<string>): Promise<any> {
  let result = {};
  for (const key of keys) {
    result[key] = (await getSetting(key)) || defaultSettings[key];
  }
  return result;
}

async function setSetting(key: string, value: any): Promise<void> {
  await settings.set(key, value);
  if (key.includes("homeAssistant")) {
    if (key === "homeAssistantSubscribedEntites")
      homeAssistantSubscribedEntites = {};
    await setupHomeAssistant();
    updateMenu();
  }
}

ipcMain.handle(
  "SETTINGS",
  async (
    _event,
    args: { type: string; key?: string; keys?: string[]; value: any }
  ) => {
    console.log("SETTINGS:", args);
    switch (args.type) {
      case "GET":
        if (args.key) return await getSetting(args.key);
        if (args.keys) {
          let result = {};
          for (const key of args.keys) {
            result[key] = (await getSetting(key)) || defaultSettings[key];
          }
          return result;
        } else return await getSettings(Object.keys(defaultSettings));
      case "SET":
        if (args.key) return await setSetting(args.key, args.value);
      default:
        return null;
    }
  }
);

// ----------------------------------------
// Home Assistant
// ----------------------------------------
let homeAssistantConnection: Connection,
  homeAssistantConfig: HassConfig,
  homeAssistantEntities: HassEntities,
  homeAssistantServices: HassServices,
  homeAssistantSubscribedEntites: Partial<HassEntities> = {};

async function connectToHomeAssistant(): Promise<Connection> {
  console.log("Connecting to Home Assistant...");
  const {
    homeAssistantHost,
    homeAssistantPort,
    homeAssistantSecure,
    homeAssistantToken,
  } = await getSettings([
    "homeAssistantHost",
    "homeAssistantPort",
    "homeAssistantSecure",
    "homeAssistantToken",
  ]);
  const hassUrl = `http${
    homeAssistantSecure ? "s" : ""
  }://${homeAssistantHost}:${homeAssistantPort}`;
  console.log("Home Assistant URL:", hassUrl);
  const auth: Auth = createLongLivedTokenAuth(hassUrl, homeAssistantToken);
  const connection: Connection = await createConnection({ auth });
  console.log("Connected to Home Assistant");
  return connection;
}

async function openInHomeAssistant(entityId?: string): Promise<void> {
  const { homeAssistantHost, homeAssistantPort, homeAssistantSecure } =
    await getSettings([
      "homeAssistantHost",
      "homeAssistantPort",
      "homeAssistantSecure",
    ]);
  const hassUrl = `http${
    homeAssistantSecure ? "s" : ""
  }://${homeAssistantHost}:${homeAssistantPort}`;

  const url = `${hassUrl}/history?entity_id=${entityId}`;
  console.log("Open in Home Assistant:", url);
  open(url);
}

function setHomeAssistantConfig(config: HassConfig): void {
  homeAssistantConfig = config;
  console.log("Home Assistant Config Updated");
}

async function setHomeAssistantEntities(entities: HassEntities): Promise<void> {
  homeAssistantEntities = entities;
  // console.log("Home Assistant Entities Updated");
  let subscribedEntitiesUpdated: boolean = false;
  for (const entityId of await getSetting("homeAssistantSubscribedEntites")) {
    if (
      !homeAssistantSubscribedEntites[entityId] ||
      homeAssistantSubscribedEntites[entityId].state !==
        homeAssistantEntities[entityId].state
    ) {
      homeAssistantSubscribedEntites[entityId] =
        homeAssistantEntities[entityId];
      subscribedEntitiesUpdated = true;
    }
  }
  if (subscribedEntitiesUpdated) {
    console.log("Home Assistant Subscribed Entities Updated");
    updateMenu();
  }
}

function setHomeAssistantServices(services: HassServices): void {
  homeAssistantServices = services;
  console.log("Home Assistant Services Updated");
}

async function setupHomeAssistant(): Promise<void> {
  if (homeAssistantConfig) {
    console.log("Home Assistant already connected");
    return;
  }

  console.log("Setting up Home Assistant...");
  // Connect to Home Assistant
  homeAssistantConnection = await connectToHomeAssistant();

  // Subscribe to Home Assistant Config
  subscribeConfig(homeAssistantConnection, setHomeAssistantConfig);

  // Subscribe to Home Assistant Services
  subscribeServices(homeAssistantConnection, setHomeAssistantServices);

  // Subscribe to Home Assistant Entities
  subscribeEntities(homeAssistantConnection, setHomeAssistantEntities);
}

setupHomeAssistant();

ipcMain.handle(
  "HOME_ASSISTANT_ENTITIES",
  async (
    _event,
    args: { type: string; key?: string; keys?: string[]; value: any }
  ) => {
    console.log("HOME_ASSISTANT_ENTITIES:", args);
    switch (args.type) {
      case "GET":
        if (args.key) return homeAssistantEntities[args.key];
        if (args.keys) {
          let result = {};
          for (const key of args.keys) {
            result[key] = homeAssistantEntities[key];
          }
          return result;
        } else return homeAssistantEntities;
      default:
        return null;
    }
  }
);

// ----------------------------------------
// Menu
// ----------------------------------------
function updateMenu(): void {
  const menuItemsEntities: Array<MenuItemConstructorOptions> = [];

  for (const entity of Object.values(homeAssistantSubscribedEntites)) {
    const domain = entity.entity_id.split(".")[0];
    let serviceNames: Array<string> = [];
    if (homeAssistantServices && domain in homeAssistantServices)
      serviceNames = Object.keys(homeAssistantServices[domain]);

    menuItemsEntities.push({
      type: serviceNames.includes("toggle") ? "checkbox" : "normal",
      checked: serviceNames.includes("toggle")
        ? entity.state === "on"
          ? true
          : false
        : undefined,
      label: serviceNames.includes("toggle")
        ? entity.attributes.friendly_name
        : `${entity.attributes.friendly_name} - ${entity.state}${
            entity.attributes.unit_of_measurement
              ? ` ${entity.attributes.unit_of_measurement}`
              : ""
          }`,
      click: async () => {
        if (serviceNames.includes("toggle"))
          await callService(homeAssistantConnection, domain, "toggle", {
            entity_id: entity.entity_id,
          });
        else if (serviceNames.includes("turn_on"))
          await callService(homeAssistantConnection, domain, "turn_on", {
            entity_id: entity.entity_id,
          });
        else await openInHomeAssistant(entity.entity_id);
      },
    });
  }

  if (menuItemsEntities.length > 0)
    menuItemsEntities.push({ type: "separator" });

  tray.setContextMenu(
    Menu.buildFromTemplate([
      ...menuItemsEntities,
      {
        type: "normal",
        label: "Settings",
        click: async () => {
          await createSettingsWindow();
        },
      },
      { type: "separator" },
      {
        type: "normal",
        label: "Exit",
        click: () => {
          app.quit();
        },
      },
    ])
  );
}
