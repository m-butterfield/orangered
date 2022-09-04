import Container from "@mui/material/Container";
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";
import React from "react";

export const Footer = () => {
  return (
    <Container sx={{pb:2}}>
      <Typography variant="body2" color="text.secondary" align="center">
        <Link color="inherit" href="/static/html/privacy.html">
            Privacy Policy
        </Link>
        <br/>
        {"Contact: "}<Link href="mailto:help@orangered.email" color="text.secondary">help@orangered.email</Link>
        <br/>
        {"Copyright © Orangered "}
        {new Date().getFullYear()}
      </Typography>
    </Container>
  );
};
