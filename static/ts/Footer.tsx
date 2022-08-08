import React from "react";
import {Container, Link, Typography} from "@mui/material";

export const Footer = () => {
  return (
    <Container sx={{pb:2}}>
      <Typography variant="body2" color="text.secondary" align="center">
        <Link color="inherit" href="/static/html/privacy.html">
            Privacy Policy
        </Link>
        <br/>
        {"Copyright © Orangered "}
        {new Date().getFullYear()}
      </Typography>
    </Container>
  );
};
