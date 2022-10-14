import Alert from "@mui/material/Alert";
import Autocomplete from "@mui/material/Autocomplete";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormLabel from "@mui/material/FormLabel";
import Grid from "@mui/material/Grid";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import React, {useState} from "react";
import {SignupFormData} from "features/SignupForm/types";
import {EmailFrequency} from "types";
import mailImg from "img/mail_orange.png";
import Link from "@mui/material/Link";

const submit = async (data: SignupFormData): Promise<string> => {
  const response = await fetch("/signup", {
    method: "POST",
    headers: new Headers({"Content-Type": "application/json"}),
    body: JSON.stringify(data),
  });
  if (response.ok) {
    return "";
  }
  return await response.text();
};

type signupFormProps = {
  allSubreddits: string[];
  recaptchaKey: string;
}

declare const grecaptcha: {
  ready: (readyFunc: () => void) => void;
  execute: (key: string, kwargs: {[key: string]: string}) => Promise<string>;
};

export function SignupForm(props: signupFormProps) {
  const {allSubreddits, recaptchaKey} = props;

  const params = new URLSearchParams(window.location.search);
  const subredditSearch = params.has("subreddits") ? params.get("subreddits").split(",") : undefined;

  const [subreddits, setSubreddits] = useState(subredditSearch || []);
  const [email, setEmail] = useState("");
  const [emailInterval, setEmailInterval] = useState(EmailFrequency.Daily);


  const [subredditWarning, setSubredditWarning] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const emailValid = /\S+@\S+/.test(email);
  const subredditsValid = subreddits.length > 0 && subreddits.length <= 10;

  return (
    <>
      <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 6}}>
        <Typography
          component="h1"
          variant="h2"
          align="center"
          color="text.primary"
          gutterBottom
        >
          <div><img src={mailImg}  alt="mail envelope"/></div>
          Orangered
        </Typography>
        <Typography variant="h5" align="center" component="p">
          The best content from your favorite subreddits delivered to your inbox
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
                autoFocus
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <Autocomplete
                disablePortal
                multiple
                fullWidth
                value={subreddits}
                id="combo-box-demo"
                options={allSubreddits}
                onChange={(_, newValue) => {
                  if (newValue.length > 10) {
                    setSubredditWarning("Too many subreddits selected. Select a maximum of 10.");
                  } else if (subredditWarning) {
                    setSubredditWarning("");
                  }
                  setSubreddits(newValue);
                }}
                renderInput={(params) => {
                  return <TextField
                    {...params}
                    error={subredditWarning.length > 0}
                    helperText={subredditWarning}
                    required
                    label="Subreddits"
                  />;
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl>
                <FormLabel>Email Frequency</FormLabel>
                <RadioGroup
                  name="radio-buttons-group"
                >
                  <FormControlLabel value="daily" control={
                    <Radio
                      checked={emailInterval === "daily"}
                      onChange={(_, val) => val && setEmailInterval(EmailFrequency.Daily)}
                    />
                  } label="Daily" />
                  <FormControlLabel value="weekly" control={
                    <Radio
                      checked={emailInterval === "weekly"}
                      onChange={(_, val) => val && setEmailInterval(EmailFrequency.Weekly)}
                    />
                  } label="Weekly" />
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              {submitError && <Alert sx={{bgcolor: "#2C3E50"}} severity="error">{submitError}</Alert>}
              {successMessage && <Alert sx={{bgcolor: "#2C3E50"}} severity="success">{successMessage}</Alert> }
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{mt: 3, mb: 2, boxShadow: "unset"}}
                disabled={submitting || !subredditsValid || !emailValid}
                onClick={(e) => {
                  e.preventDefault();
                  setSubmitting(true);
                  if (submitError) setSubmitError("");
                  if (successMessage) setSuccessMessage("");

                  const doSubmit = (token: string) => {
                    submit({
                      email: email,
                      subreddits: subreddits,
                      captchaToken: token,
                      emailInterval: emailInterval,
                    }).then((errorMessage) => {
                      if (errorMessage) {
                        alert(errorMessage);
                        setSubmitError(errorMessage);
                        setSubmitting(false);
                      } else {
                        const successMessage = "Success! You will receive your first email soon.";
                        alert(successMessage);
                        setSuccessMessage(successMessage);
                      }
                    });
                  };

                  if (typeof grecaptcha !== "undefined") {
                    grecaptcha.ready(() => {
                      grecaptcha.execute(recaptchaKey, {action: "submit"}).then((token) => {
                        doSubmit(token);
                      });
                    });
                  } else {
                    doSubmit("");
                  }
                }}
              >
                Sign Up
              </Button>
              <Typography color="text.secondary" fontSize="small">This site is protected by reCAPTCHA and the Google <Link color="text.secondary" href="https://policies.google.com/privacy">Privacy Policy</Link> and <Link color="text.secondary" href="https://policies.google.com/terms">Terms of Service</Link> apply.</Typography>
            </Grid>
          </Grid>
        </Box>
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
        <Typography variant="h6" align="center" component="p">
          Select your favorite subreddits and we'll send you a daily email with the top posts from each one.
          <br/>
          <Link href="/static/html/sample_email.html" target="_blank">Click here to see a sample email.</Link>
        </Typography>
      </Container>
    </>
  );
}
