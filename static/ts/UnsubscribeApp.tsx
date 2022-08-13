import {
  Alert,
  Box,
  Button,
  Container,
  Grid,
  Typography,
} from "@mui/material";
import React, {useState} from "react";
import {Footer} from "Footer";
import {Header} from "Header";
import {Account} from "types";

declare const account: Account;

const submit = async (accountID: string, unsubscribe: boolean): Promise<string> => {
  const response = await fetch(`/account/${accountID}/unsubscribe`, {
    method: "POST",
    headers: new Headers({"Content-Type": "application/json"}),
    body: JSON.stringify({unsubscribe: unsubscribe}),
  });
  if (response.ok) {
    return "";
  }
  return await response.text();
};

function UnsubscribeApp() {
  const [unsubscribed, setUnsubscribed] = useState(!account.active);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  return (
    <div className="App">
      <Header></Header>
      <Container disableGutters maxWidth="sm" component="main" sx={{pt: 8, pb: 6}}>
        <Typography
          component="h1"
          variant="h2"
          align="center"
          color="text.primary"
          gutterBottom
        >
          Unsubscribe
        </Typography>
        <Box component="form" noValidate sx={{mt: 3}}>
          <Grid container spacing={2}>
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
                disabled={submitting}
                onClick={(e) => {
                  e.preventDefault();
                  if (submitError) setSubmitError("");
                  if (successMessage) setSuccessMessage("");
                  setSubmitting(true);
                  submit(account.id, !unsubscribed).then((errorMessage) => {
                    if (errorMessage) {
                      alert(errorMessage);
                      setSubmitError(errorMessage);
                    } else {
                      const successMessage = "Success!";
                      alert(successMessage);
                      setSuccessMessage(successMessage);
                      setUnsubscribed(!unsubscribed);
                    }
                    setSubmitting(false);
                  });
                }}
              >
                {unsubscribed ? "Resubscribe" : "Click Here to Unsubscribe"}
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Container>
      <Footer></Footer>
    </div>
  );
}

export default UnsubscribeApp;
