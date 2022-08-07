import React from "react";
import {useAppSelector, useAppDispatch} from "app/hooks";
import {
  getSubreddits,
  updateEmail,
  selectEmail,
} from "features/SignupForm/signupFormSlice";
import {AppBar, Button, Link, Toolbar, Typography} from "@mui/material";

export function SignupForm() {
  const email = useAppSelector(selectEmail);
  // const dispatch = useAppDispatch();
  // can eventually dispatch getSubreddits

  return (
    <>
      <AppBar
        position="static"
      >
        <Toolbar>
          <Typography variant="h6" sx={{flexGrow: 1}}>
            Orangered
          </Typography>
          <nav>
            <Link
              variant="button"
              color="text.primary"
              href="#about"
              sx={{my: 1, mx: 1.5}}
            >
              About
            </Link>
            <Link
              variant="button"
              color="text.primary"
              href="#signup"
              sx={{my: 1, mx: 1.5}}
            >
              Sign Up
            </Link>
          </nav>
        </Toolbar>
      </AppBar>
    </>
  );
}
