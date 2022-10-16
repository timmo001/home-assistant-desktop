import { NameValue } from "./nameValue";

export interface SettingsSection {
  id: string;
  name: string;
  description: string;
  icon: string;
}

export interface SettingDescription {
  name: string;
  description: string;
  icon: string;
  section: string;
  containerDisabled?: boolean;
  isList?: boolean;
  isPassword?: boolean;
  minimum?: number;
}

export type SettingsValue =
  | null
  | boolean
  | string
  | string[]
  | number
  | SettingsObject
  | SettingsValue[]
  | NameValue
  | NameValue[];

export type SettingsObject = {
  [key: string]: SettingsValue;
};
