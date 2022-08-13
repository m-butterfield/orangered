import React from "react";
import {SignupForm} from "features/SignupForm/SignupForm";
import {Footer} from "Footer";
import {Header} from "Header";

declare const allSubreddits: string[];
declare const recaptchaToken: string;
declare const recaptchaRefresh: () => void;

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
        recaptchaToken={recaptchaToken}
        recaptchaRefresh={recaptchaRefresh}
      ></SignupForm>
      <Footer></Footer>
    </div>
  );
}

export default SignupApp;
