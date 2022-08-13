import React from "react";
import {SignupForm} from "features/SignupForm/SignupForm";
import {Footer} from "Footer";
import {Header} from "Header";

declare const allSubreddits: string[];
declare const recaptchaKey: string;

function SignupApp() {
  return (
    <div className="App">
      <Header links={[
        {name: "About", href: "about"},
        {name: "Sign Up", href: "signup"}
      ]}
      />
      <SignupForm
        allSubreddits={allSubreddits}
        recaptchaKey={recaptchaKey}
      ></SignupForm>
      <Footer></Footer>
    </div>
  );
}

export default SignupApp;
