import { ReactElement } from "react";
import { Container, Typography } from "@mui/material";

import Header from "@/components/Header";
import Settings from "@/components/settings/Settings";

const title = "Settings";
function Routes(): ReactElement {
  return (
    <>
      <Header title={title} />
      <Container maxWidth="xl" sx={{ p: 2 }}>
        <Typography component="h1" variant="h2" gutterBottom>
          {title}
        </Typography>
        <Settings />
      </Container>
    </>
  );
}

export default Routes;
