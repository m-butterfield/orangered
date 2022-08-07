import {createAsyncThunk, createSlice, PayloadAction} from "@reduxjs/toolkit";
import {RootState} from "app/store";
import {fetchSubreddits} from "features/SignupForm/signupFormAPI";

export interface SignupFormState {
  email: string;
}

const initialState: SignupFormState = {
  email: "",
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

export const {updateEmail} = signupFormSlice.actions;

// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state: RootState) => state.counter.value)`
export const selectEmail = (state: RootState) => state.form.email;

export default signupFormSlice.reducer;
