import React from "react";
import {createRoot} from "react-dom/client";
import {Provider} from "react-redux";
import {theme} from "theme";
import {store} from "app/store";
import {CssBaseline, ThemeProvider} from "@mui/material";
import ManageApp from "ManageApp";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <ManageApp />
      </ThemeProvider>
    </Provider>
  </React.StrictMode>
);
