import {
  mdiRocketLaunch,
  mdiTextBoxOutline,
  mdiWeb,
  mdiProtocol,
  mdiHomeAssistant,
} from "@mdi/js";

import { SettingDescription, SettingsSection } from "@/types/settings";

export const settingsSections: SettingsSection[] = [
  {
    id: "general",
    name: "General",
    description: "General settings",
    icon: mdiRocketLaunch,
  },
  {
    id: "homeAssistant",
    name: "Home Assistant",
    description: "Home Assistant settings",
    icon: mdiHomeAssistant,
  },
];

export const settingsMap: { [key: string]: SettingDescription } = {
  autostart: {
    section: "general",
    name: "Autostart",
    description: "Automatically start the application on startup",
    icon: mdiRocketLaunch,
  },
  log_level: {
    section: "general",
    name: "Log Level",
    description: "Log level for the application",
    icon: mdiTextBoxOutline,
  },
  home_assistant_host: {
    section: "homeAssistant",
    name: "Host",
    description: "Port for the API and WebSocket",
    icon: mdiWeb,
  },
  home_assistant_port: {
    section: "homeAssistant",
    name: "Port",
    description: "Port for the API and WebSocket",
    icon: mdiProtocol,
    minimum: 1,
  },
  // additional_media_directories: {
  //   name: "Additional Media Directories",
  //   description: "Additional media directories for the media endpoint",
  //   icon: mdiFolderMultipleOutline,
  //   isList: true,
  // },
};
