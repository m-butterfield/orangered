import React from "react";
import {AppBar, Link, Toolbar, Typography} from "@mui/material";
import {HeaderLink} from "types";

export const Header = (props: {links?: HeaderLink[]}) => {
  return (
    <AppBar
      position="static"
    >
      <Toolbar>
        <Typography variant="h6" sx={{flexGrow: 1}}>
          <Link underline="hover" color="text.primary" href="/">Orangered</Link>
        </Typography>
        <nav>
          {props.links && props.links.map(link => <Link
            key={`${link.href}-link`}
            variant="button"
            underline="hover"
            color="text.primary"
            href={`#${link.href}`}
            sx={{my: 1, mx: 1.5}}
          >
            {link.name}
          </Link>)}
        </nav>
      </Toolbar>
    </AppBar>
  );
};
