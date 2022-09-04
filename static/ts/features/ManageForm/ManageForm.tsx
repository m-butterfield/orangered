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
import {Account, EmailFrequency} from "types";
import {ManageData} from "features/ManageForm/types";

const submit = async (accountID: string, data: ManageData): Promise<string> => {
  const response = await fetch(`/account/${accountID}/manage`, {
    method: "POST",
    headers: new Headers({"Content-Type": "application/json"}),
    body: JSON.stringify(data),
  });
  if (response.ok) {
    return "";
  }
  return await response.text();
};

type manageFormProps = {
  allSubreddits: string[];
}

const gAccount = (window as {account?: Account}).account;

export function ManageForm(props: manageFormProps) {
  if (!gAccount) return <>Account not found.</>;
  const [account, setAccount] = useState(gAccount);

  const {allSubreddits} = props;

  const [subredditWarning, setSubredditWarning] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const subredditsValid = account.subreddits.length > 0 && account.subreddits.length <= 10;

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
          Settings
        </Typography>
        <Typography variant="h6" align="center" component="p">
          Select your subreddits.
        </Typography>
        <Box component="form" noValidate sx={{mt: 3}}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Autocomplete
                disablePortal
                multiple
                fullWidth
                value={account.subreddits}
                id="combo-box-demo"
                options={allSubreddits}
                onChange={(_, newValue) => {
                  if (newValue.length > 10) {
                    setSubredditWarning("Too many subreddits selected. Select a maximum of 10.");
                  } else if (subredditWarning) {
                    setSubredditWarning("");
                  }
                  setAccount({
                    ...account,
                    subreddits: newValue,
                  });
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
                      checked={account.emailInterval === "daily"}
                      onChange={(_, val) => val && setAccount({...account, emailInterval: EmailFrequency.Daily})}
                    />
                  } label="Daily" />
                  <FormControlLabel value="weekly" control={
                    <Radio
                      checked={account.emailInterval === "weekly"}
                      onChange={(_, val) => val && setAccount({...account, emailInterval: EmailFrequency.Weekly})}
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
                disabled={submitting || !subredditsValid}
                onClick={(e) => {
                  e.preventDefault();
                  if (submitError) setSubmitError("");
                  if (successMessage) setSuccessMessage("");
                  setSubmitting(true);
                  submit(account.id, {
                    subreddits: account.subreddits,
                    emailInterval: account.emailInterval,
                  }).then((errorMessage) => {
                    if (errorMessage) {
                      alert(errorMessage);
                      setSubmitError(errorMessage);
                    } else {
                      const successMessage = "Success! Account updated.";
                      alert(successMessage);
                      setSuccessMessage(successMessage);
                    }
                    setSubmitting(false);
                  });
                }}
              >
                Update
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </>
  );
}
