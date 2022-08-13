import React from "react";
import {createRoot} from "react-dom/client";
import {theme} from "theme";
import {CssBaseline, ThemeProvider} from "@mui/material";
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
