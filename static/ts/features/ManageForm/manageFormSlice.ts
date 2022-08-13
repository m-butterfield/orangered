import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {RootState} from "app/store";
import {Account, EmailFrequency} from "types";

export interface ManageState {
  account?: Account
}

const initialState: ManageState = {
  account: (window as {account?: Account}).account,
};

export const manageSlice = createSlice({
  name: "manage",
  initialState,
  reducers: {
    updateSubreddits: (state, action: PayloadAction<string[]>) => {
      state.account.subreddits = action.payload;
    },
    updateFrequency: (state, action: PayloadAction<EmailFrequency>) => {
      state.account.emailInterval = action.payload;
    },
  },
});

export const {updateSubreddits, updateFrequency} = manageSlice.actions;

export const selectManageValues = (state: RootState) => state.manage;

export default manageSlice.reducer;
