import React from "react";
import {Footer} from "Footer";
import {ManageForm} from "features/ManageForm/ManageForm";
import {Header} from "Header";

declare const allSubreddits: string[];

function ManageApp() {
  return (
    <div className="App">
      <Header></Header>
      <ManageForm
        allSubreddits={allSubreddits}
      ></ManageForm>
      <Footer></Footer>
    </div>
  );
}

export default ManageApp;
