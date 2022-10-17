import React, {
  createContext,
  ReactElement,
  useContext,
  useState,
} from "react";

import type { SettingsObject } from "@/types/settings";

const SettingsContext = createContext<SettingsObject | undefined>(undefined);
const SetSettingsContext = createContext<null | React.Dispatch<
  React.SetStateAction<SettingsObject | undefined>
>>(null);

export const SettingsProvider = ({
  children,
}: {
  children: ReactElement;
}): ReactElement => {
  const [config, setConfig] = useState<SettingsObject>();

  return (
    <SetSettingsContext.Provider value={setConfig}>
      <SettingsContext.Provider value={config}>
        {children}
      </SettingsContext.Provider>
    </SetSettingsContext.Provider>
  );
};

export const useSettings = (): [
  settings: SettingsObject | undefined,
  setSettings: React.Dispatch<React.SetStateAction<SettingsObject | undefined>>
] => {
  const settings = useContext(SettingsContext);
  const setSettings = useContext(SetSettingsContext);
  if (setSettings === null) throw new Error(); // this will make setSettings non-null
  return [settings, setSettings];
};
