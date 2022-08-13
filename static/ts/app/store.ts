import {configureStore} from "@reduxjs/toolkit";
import formReducer from "features/SignupForm/signupFormSlice";
import manageReducer from "features/ManageForm/manageFormSlice";

export const store = configureStore({
  reducer: {
    form: formReducer,
    manage: manageReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
