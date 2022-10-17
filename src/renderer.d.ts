import type { HassEntities } from "home-assistant-js-websocket";

import type { IPCArguments } from "@/types/ipcArguments";
import type { SettingsObject } from "@/types/settings";

export interface IElectronAPI {
  getHomeAssistantEntities: (args?: IPCArguments) => Promise<HassEntities>;
  getSettings: (args: IPCArguments) => Promise<SettingsObject>;
  setSettings: (args: IPCArguments) => Promise<void>;
}

declare global {
  interface Window {
    electronAPI: IElectronAPI;
  }
}
