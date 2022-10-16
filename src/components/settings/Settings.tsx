import { ReactElement, useCallback, useEffect } from "react";
import { CircularProgress, Grid, useTheme } from "@mui/material";
import { ipcRenderer } from "electron";

import type { SettingsSection, SettingsValue } from "@/types/settings";
import { settingsMap, settingsSections } from "@/assets/settings";
import { useSettings } from "../Contexts/Settings";
import Item from "./Item";
import Section from "./Section";

let initialized = false;
function Settings(): ReactElement {
  const [settings, setSettings] = useSettings();

  const handleSetup = useCallback(async () => {
    console.log("Setup");
    const response = await ipcRenderer.invoke("SETTINGS", {
      type: "GET",
      keys: Object.keys(settingsMap),
    });
    console.log("Setup response", response);
    setSettings(response);
  }, []);

  const handleUpdate = useCallback(
    async (key: string, value: SettingsValue) => {
      console.log("Update:", key, value);
      await ipcRenderer.invoke("SETTINGS", {
        type: "SET",
        key,
        value,
      });
      setSettings({ ...settings, [key]: value });
    },
    [settings, setSettings]
  );

  useEffect(() => {
    if (initialized) return;
    initialized = true;
    handleSetup();
  }, [handleSetup]);

  const theme = useTheme();
  return (
    <>
      <Grid
        container
        direction="column"
        spacing={2}
        alignItems="stretch"
        sx={{
          marginBottom: theme.spacing(8),
          padding: theme.spacing(2),
        }}
      >
        {settings ? (
          <>
            {settingsSections.map(
              ({ id, name, description, icon }: SettingsSection) => (
                <Section
                  key={id}
                  name={name}
                  description={description}
                  icon={icon}
                >
                  <>
                    {Object.keys(settingsMap)
                      .filter((key: string) => settingsMap[key].section === id)
                      .map((key: string, index: number) => (
                        <Item
                          key={index}
                          keyIn={key}
                          valueIn={settings[key]}
                          onUpdate={handleUpdate}
                        />
                      ))}
                  </>
                </Section>
              )
            )}
          </>
        ) : (
          <Grid
            container
            direction="row"
            justifyContent="center"
            sx={{ margin: theme.spacing(2, 0, 10) }}
          >
            <CircularProgress />
          </Grid>
        )}
      </Grid>
    </>
  );
}

export default Settings;
