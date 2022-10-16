import { ReactElement, useEffect, useState } from "react";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  TextField,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { Icon } from "@mdi/react";
import { mdiMinusBoxOutline, mdiPlus } from "@mdi/js";
import _ from "lodash";

import { NameValue } from "@/types/nameValue";
import { SettingDescription } from "@/types/settings";

interface ItemListProps {
  setting: SettingDescription;
  listIn: Array<string>;
  open: boolean;
  setOpen: (open: boolean) => void;
  onUpdate: (list: Array<string>) => void;
}

function ItemList({
  setting,
  listIn,
  open,
  setOpen,
  onUpdate,
}: ItemListProps): ReactElement {
  const [list, setList] = useState<Array<string>>([]);

  const { name, description, icon }: SettingDescription = setting;

  useEffect(() => {
    if (!open && listIn) setList(listIn);
  }, [listIn, open]);

  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("md"));

  return (
    <Dialog
      fullScreen={fullScreen}
      fullWidth
      maxWidth="lg"
      open={open}
      scroll="paper"
      PaperProps={{
        style: {
          background: theme.palette.background.paper,
        },
      }}
    >
      <DialogTitle>
        <Icon
          id="copy-to-clipboard"
          title="Copy to clipboard"
          size={0.7}
          path={icon}
          style={{ marginRight: theme.spacing(1) }}
        />
        {name}
      </DialogTitle>
      <DialogContentText sx={{ margin: theme.spacing(0, 3) }}>
        {description}
      </DialogContentText>
      <DialogContent>
        <List>
          {list.map((item: any, key: number) => (
            <ListItem key={key}>
              <Grid container alignItems="center">
                <Grid
                  item
                  xs
                  sx={{
                    marginRight: theme.spacing(1),
                  }}
                >
                  <TextField
                    id="entity"
                    label="Entity"
                    fullWidth
                    variant="outlined"
                    value={item}
                    onChange={(event) => {
                      const newList: Array<string> = _.cloneDeep(list);
                      console.log("Update:", key, event.target.value);
                      newList[key] = event.target.value;
                      setList(newList);
                    }}
                  />
                </Grid>
                <Grid item>
                  <IconButton
                    aria-label="Remove"
                    size="large"
                    onClick={() => {
                      const newList = _.cloneDeep(list);
                      newList.splice(key, 1);
                      setList(newList);
                    }}
                  >
                    <Icon
                      id="remove-item"
                      title="Remove"
                      size={0.8}
                      path={mdiMinusBoxOutline}
                    />
                  </IconButton>
                </Grid>
              </Grid>
            </ListItem>
          ))}
          <ListItemButton
            onClick={() => {
              const newList = _.cloneDeep(list);
              newList.push("");
              setList(newList);
            }}
          >
            <ListItemIcon>
              <Icon id="add" title="Add" size={1} path={mdiPlus} />
            </ListItemIcon>
            <ListItemText primary="Add" secondary="Add a new item" />
          </ListItemButton>
        </List>
      </DialogContent>
      <DialogActions>
        <Button
          onClick={() => {
            setOpen(false);
          }}
          color="primary"
          variant="outlined"
        >
          Cancel
        </Button>
        <Button
          onClick={() => {
            setOpen(false);
            onUpdate(list);
          }}
          color="primary"
          variant="outlined"
        >
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ItemList;
