import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {RootState} from "app/store";
import {SignupFormData} from "features/SignupForm/types";
import {EmailFrequency} from "types";

const initialState: SignupFormData = {
  email: "",
  subreddits: [],
  emailInterval: EmailFrequency.Daily,
  captchaToken: "",
};

export const signupFormSlice = createSlice({
  name: "form",
  initialState,
  reducers: {
    updateEmail: (state, action: PayloadAction<string>) => {
      state.email = action.payload;
    },
    updateSubreddits: (state, action: PayloadAction<string[]>) => {
      state.subreddits = action.payload;
    },
    updateFrequency: (state, action: PayloadAction<EmailFrequency>) => {
      state.emailInterval = action.payload;
    },
  },
});

export const {updateEmail, updateSubreddits, updateFrequency} = signupFormSlice.actions;

export const selectFormValues = (state: RootState) => state.form;

export default signupFormSlice.reducer;
