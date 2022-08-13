import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {RootState} from "app/store";
import {EmailFrequency} from "./types";

export interface SignupFormState {
  email: string;
  subreddits: string[];
  emailFrequency: EmailFrequency;
}

const initialState: SignupFormState = {
  email: "",
  subreddits: [],
  emailFrequency: EmailFrequency.Daily,
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
      state.emailFrequency = action.payload;
    },
  },
});

export const {updateEmail, updateSubreddits, updateFrequency} = signupFormSlice.actions;

export const selectFormValues = (state: RootState) => state.form;

export default signupFormSlice.reducer;
