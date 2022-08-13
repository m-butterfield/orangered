import React from "react";
import {SignupForm} from "features/SignupForm/SignupForm";
import {Footer} from "Footer";

function SignupApp() {
  return (
    <div className="App">
      <SignupForm></SignupForm>
      <Footer></Footer>
    </div>
  );
}

export default SignupApp;
