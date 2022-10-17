import {
  mdiRocketLaunch,
  mdiWeb,
  mdiProtocol,
  mdiHomeAssistant,
  mdiSecurity,
  mdiFormTextboxPassword,
} from "@mdi/js";

import type { SettingDescription, SettingsSection } from "@/types/settings";

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
  // logLevel: {
  //   section: "general",
  //   name: "Log Level",
  //   description: "Log level for the application",
  //   icon: mdiTextBoxOutline,
  // },
  homeAssistantSecure: {
    section: "homeAssistant",
    name: "SSL",
    description: "Use SSL to connect to Home Assistant",
    icon: mdiSecurity,
  },
  homeAssistantHost: {
    section: "homeAssistant",
    name: "Host",
    description: "The host of the Home Assistant instance",
    icon: mdiWeb,
  },
  homeAssistantPort: {
    section: "homeAssistant",
    name: "Port",
    description: "The port of the Home Assistant instance",
    icon: mdiProtocol,
    minimum: 1,
  },
  homeAssistantToken: {
    section: "homeAssistant",
    name: "Token",
    description: "The long-lived access token for Home Assistant",
    icon: mdiFormTextboxPassword,
  },
  homeAssistantSubscribedEntites: {
    section: "homeAssistant",
    name: "Subscribed Entities",
    description: "The entities to subscribe to",
    icon: mdiHomeAssistant,
    isList: true,
  },
};
