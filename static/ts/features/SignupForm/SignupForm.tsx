import React from "react";
import {useAppSelector, useAppDispatch} from "app/hooks";
import {
  updateEmail,
  selectEmail,
} from "features/SignupForm/signupFormSlice";
import {
  AppBar, Autocomplete,
  Box,
  Button,
  Container,
  Grid,
  Link,
  TextField,
  Toolbar,
  Typography
} from "@mui/material";
import mailImg from "img/mail_orange.png";

declare const subreddits: string[];

export function SignupForm() {
  const email = useAppSelector(selectEmail);
  const dispatch = useAppDispatch();

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
      <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 6}}>
        <Typography
          component="h1"
          variant="h1"
          align="center"
          color="text.primary"
          gutterBottom
        >
          <div><img src={mailImg}  alt="mail envelope"/></div>
          Orangered
        </Typography>
        <Typography variant="h5" align="center" color="text.secondary" component="p">
          The best content from your favorite subreddits delivered to your inbox
        </Typography>
      </Container>
      <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 6}}>
        <Typography
          id="about"
          component="h1"
          variant="h2"
          align="center"
          color="text.primary"
          gutterBottom
        >
          About
        </Typography>
        <Typography variant="h6" align="center" color="text.secondary" component="p">
          Select your favorite subreddits and we'll send you a daily email with the top posts from each one.
          <br/>
          <Link href="/static/html/sample_email.html" target="_blank">Click here to see a sample email.</Link>
        </Typography>
      </Container>
      <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 6}}>
        <Typography
          id="signup"
          component="h1"
          variant="h2"
          align="center"
          color="text.primary"
          gutterBottom
        >
          Sign Up
        </Typography>
        <Box component="form" noValidate sx={{mt: 3}}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                value={email}
                onChange={(e) => dispatch(updateEmail(e.target.value))}
              />
            </Grid>
            <Grid item xs={12}>
              <Autocomplete
                disablePortal
                multiple
                fullWidth
                id="combo-box-demo"
                options={subreddits}
                renderInput={(params) => <TextField {...params} label="Subreddits" />}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{mt: 3, mb: 2}}
          >
            Sign Up
          </Button>
        </Box>
      </Container>
    </>
  );
}
