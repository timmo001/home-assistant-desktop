import React, { ChangeEvent, ReactElement, useMemo, useState } from "react";
import {
  Autocomplete,
  FormControl,
  Grid,
  IconButton,
  InputAdornment,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemSecondaryAction,
  ListItemText,
  OutlinedInput,
  Switch,
  TextField,
  useTheme,
} from "@mui/material";
import { Icon } from "@mdi/react";
import { mdiContentSaveOutline, mdiEye, mdiEyeOff } from "@mdi/js";

import type { SettingDescription, SettingsValue } from "@/types/settings";
import { settingsMap } from "@/assets/settings";
import ItemList from "./ItemList";

interface ItemProps {
  keyIn: string;
  valueIn: SettingsValue;
  onUpdate: (key: string, value: SettingsValue) => Promise<void>;
}

function Item({ keyIn, valueIn, onUpdate }: ItemProps): ReactElement {
  const [open, setOpen] = useState<boolean>(false);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [value, setValue] = useState<SettingsValue>(valueIn);

  function handleSetSetting(valueIn: SettingsValue): void {
    setValue(valueIn);
  }

  function handleInputChanged(event: ChangeEvent<HTMLInputElement>): void {
    handleSetSetting(event.target.value);
  }

  function handleCheckedChanged(
    _event: ChangeEvent<HTMLInputElement>,
    checked: boolean
  ): void {
    handleSetSetting(checked);
  }

  function handleAutocompleteChanged(_event: any, value: string | null): void {
    if (value) handleSetSetting(value);
  }

  function handleClickShowPassword(): void {
    setShowPassword(!showPassword);
  }

  function handleMouseDownPassword(
    event: React.MouseEvent<HTMLButtonElement>
  ): void {
    event.preventDefault();
  }

  const valueChanged = useMemo(() => valueIn !== value, [valueIn, value]);

  const {
    name,
    description,
    icon,
    containerDisabled,
    isList,
    isPassword,
    minimum,
  }: SettingDescription = settingsMap[keyIn];

  const theme = useTheme();

  const ItemContainer = ({
    children,
  }: {
    children: ReactElement;
  }): ReactElement => {
    if (isList)
      return (
        <ListItemButton onClick={() => setOpen(true)}>
          {children}
        </ListItemButton>
      );
    return <ListItem>{children}</ListItem>;
  };

  return (
    <>
      <ItemContainer>
        <>
          <ListItemIcon>
            <Icon id="icon" title={name} size={1} path={icon} />
          </ListItemIcon>
          <ListItemText
            primary={name}
            secondary={description}
            sx={{ maxWidth: "64%", userSelect: "none" }}
          />
          <ListItemSecondaryAction sx={{ width: 420, textAlign: "end" }}>
            <Grid container alignItems="center" justifyContent="flex-end">
              <Grid item>
                {typeof value === "boolean" ? (
                  <Switch
                    edge="end"
                    disabled={containerDisabled}
                    checked={value}
                    onChange={handleCheckedChanged}
                  />
                ) : typeof valueIn === "string" &&
                  typeof value === "string" &&
                  keyIn === "logLevel" ? (
                  <Autocomplete
                    id={keyIn}
                    options={["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]}
                    renderInput={(params) => (
                      <TextField {...params} variant="outlined" />
                    )}
                    onChange={handleAutocompleteChanged}
                    sx={{ width: 210 }}
                    value={value}
                  />
                ) : typeof valueIn === "string" && isPassword ? (
                  <FormControl variant="outlined">
                    <OutlinedInput
                      type={showPassword ? "text" : "password"}
                      defaultValue={value}
                      onChange={handleInputChanged}
                      endAdornment={
                        <InputAdornment position="end">
                          <IconButton
                            aria-label="Toggle visibility"
                            onClick={handleClickShowPassword}
                            onMouseDown={handleMouseDownPassword}
                            size="large"
                          >
                            <Icon
                              id="copy-to-clipboard"
                              title="Copy to clipboard"
                              size={0.8}
                              path={showPassword ? mdiEye : mdiEyeOff}
                            />
                          </IconButton>
                        </InputAdornment>
                      }
                    />
                  </FormControl>
                ) : typeof valueIn === "string" ? (
                  <TextField
                    type="text"
                    defaultValue={value}
                    disabled={containerDisabled}
                    onChange={handleInputChanged}
                    variant="outlined"
                  />
                ) : typeof valueIn === "number" ? (
                  <TextField
                    error={minimum ? Number(value) < minimum : false}
                    type="number"
                    disabled={containerDisabled}
                    inputProps={{ minimum: minimum }}
                    defaultValue={value}
                    onChange={handleInputChanged}
                    variant="outlined"
                  />
                ) : (
                  ""
                )}
              </Grid>
              {isList ? (
                ""
              ) : (
                <Grid item>
                  <IconButton
                    disabled={valueChanged === false}
                    onClick={() => {
                      onUpdate(keyIn, value);
                    }}
                    sx={{ margin: theme.spacing(1) }}
                  >
                    <Icon
                      id="save"
                      title="Save"
                      size={1}
                      path={mdiContentSaveOutline}
                      style={{ opacity: valueChanged ? 1 : 0.25 }}
                    />
                  </IconButton>
                </Grid>
              )}
            </Grid>
          </ListItemSecondaryAction>
        </>
      </ItemContainer>
      {isList && Array.isArray(value) ? (
        <>
          <ItemList
            setting={settingsMap[keyIn]}
            listIn={value as unknown as Array<string>}
            open={open}
            setOpen={setOpen}
            onUpdate={(newValue: Array<string>) => {
              setValue(newValue);
              onUpdate(keyIn, newValue);
            }}
          />
        </>
      ) : (
        ""
      )}
    </>
  );
}

export default Item;
