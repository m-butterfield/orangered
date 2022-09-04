import CssBaseline from "@mui/material/CssBaseline";
import {ThemeProvider} from "@mui/material/styles";
import React from "react";
import {createRoot} from "react-dom/client";
import {theme} from "theme";
import ManageApp from "ManageApp";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ManageApp />
    </ThemeProvider>
  </React.StrictMode>
);
