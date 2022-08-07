import React from "react";
import ReactDOM from "react-dom";
import {Provider} from "react-redux";
import {theme} from "theme";
import {store} from "app/store";
import App from "App";
import "index.css";
import {CssBaseline, ThemeProvider} from "@mui/material";

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);
