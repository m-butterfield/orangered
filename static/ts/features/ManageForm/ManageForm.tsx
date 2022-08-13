import React, {useState} from "react";
import {useAppSelector, useAppDispatch} from "app/hooks";
import {
  selectManageValues, updateSubreddits, updateFrequency,
} from "features/ManageForm/manageFormSlice";
import {EmailFrequency} from "types";
import {
  Alert,
  Autocomplete,
  Box,
  Button,
  Container, FormControl, FormControlLabel, FormLabel,
  Grid,
  Radio,
  RadioGroup,
  TextField,
  Typography
} from "@mui/material";
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

export function ManageForm(props: manageFormProps) {
  const {account} = useAppSelector(selectManageValues);
  if (!account) return <>Account not found.</>;

  const {allSubreddits} = props;
  const dispatch = useAppDispatch();

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
        <Typography variant="h6" align="center" color="text.secondary" component="p">
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
                  dispatch(updateSubreddits(newValue));
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
                      onChange={(_, val) => val && dispatch(updateFrequency(EmailFrequency.Daily))}
                    />
                  } label="Daily" />
                  <FormControlLabel value="weekly" control={
                    <Radio
                      checked={account.emailInterval === "weekly"}
                      onChange={(_, val) => val && dispatch(updateFrequency(EmailFrequency.Weekly))}
                    />
                  } label="Weekly" />
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              {submitError && <Alert severity="error">{submitError}</Alert>}
              {successMessage && <Alert severity="success">{successMessage}</Alert> }
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{mt: 3, mb: 2}}
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
