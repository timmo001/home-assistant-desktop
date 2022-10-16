import { ReactElement } from "react";
import { Grid, List, Paper, Typography } from "@mui/material";
import { Icon } from "@mdi/react";

export interface SectionProps {
  name: string;
  description: string;
  icon: string;
  children: ReactElement;
}

function Section({
  name,
  description,
  icon,
  children,
}: SectionProps): ReactElement {
  return (
    <Grid container direction="row" item xs={12}>
      <Grid item xs={4} style={{ userSelect: "none" }}>
        <Typography component="h3" variant="h5">
          <Icon
            id={`icon-${name}`}
            title={name}
            size={1}
            path={icon}
            style={{ marginRight: "0.6rem", paddingTop: "0.2rem" }}
          />
          {name}
        </Typography>
        <Typography variant="subtitle1" sx={{ pl: "2.1rem" }}>
          {description}
        </Typography>
      </Grid>
      <Grid item xs={8}>
        <Paper>
          <List>{children}</List>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Section;
