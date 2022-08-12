import {createAsyncThunk, createSlice, PayloadAction} from "@reduxjs/toolkit";
import {RootState} from "app/store";
import {fetchSubreddits} from "features/SignupForm/signupFormAPI";
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

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched. Thunks are
// typically used to make async requests.
export const getSubreddits = createAsyncThunk(
  "form/fetchSubreddits",
  async (query: string) => {
    const response = await fetchSubreddits(query);
    // The value we return becomes the `fulfilled` action payload
    return response.data;
  }
);

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
  extraReducers: (builder) => {
    builder
      .addCase(getSubreddits.pending, (state) => {
        // state.status = 'loading';
      })
      .addCase(getSubreddits.fulfilled, (state, action) => {
        // state.status = 'idle';
        // state.value += action.payload;
      })
      .addCase(getSubreddits.rejected, (state) => {
        // state.status = 'failed';
      });
  },
});

export const {updateEmail, updateSubreddits, updateFrequency} = signupFormSlice.actions;

// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state: RootState) => state.counter.value)`
export const selectFormValues = (state: RootState) => state.form;

export default signupFormSlice.reducer;
