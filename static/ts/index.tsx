import React from "react";
import {createRoot} from "react-dom/client";
import {Provider} from "react-redux";
import {theme} from "theme";
import {store} from "app/store";
import SignupApp from "SignupApp";
import {CssBaseline, ThemeProvider} from "@mui/material";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <SignupApp />
      </ThemeProvider>
    </Provider>
  </React.StrictMode>
);
