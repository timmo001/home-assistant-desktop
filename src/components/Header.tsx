import { ReactElement } from "react";
import { AppBar, IconButton, Toolbar, Typography } from "@mui/material";
import { Icon } from "@mdi/react";
import { mdiMenu } from "@mdi/js";

interface HeaderProps {
  title: string;
}

function Header({ title }: HeaderProps): ReactElement {
  return (
    <AppBar position="static" color="primary">
      <Toolbar variant="dense">
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <Icon id="icon-menu" path={mdiMenu} size={1} />
        </IconButton>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          {title}
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
