import React from "react";
import {Link, Typography} from "@mui/material";

export const Footer = () => {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      <Link color="inherit" href="/static/html/privacy.html">
            Privacy Policy
      </Link>
      <br/>
      {"Copyright © Orangered "}
      {new Date().getFullYear()}
    </Typography>
  );
};
