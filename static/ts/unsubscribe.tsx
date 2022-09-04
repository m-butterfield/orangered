import CssBaseline from "@mui/material/CssBaseline";
import {ThemeProvider} from "@mui/material/styles";
import React from "react";
import {createRoot} from "react-dom/client";
import {theme} from "theme";
import UnsubscribeApp from "UnsubscribeApp";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <UnsubscribeApp />
    </ThemeProvider>
  </React.StrictMode>
);
