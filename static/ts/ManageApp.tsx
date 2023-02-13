import React, {useEffect, useState} from "react";
import {Footer} from "Footer";
import {ManageForm} from "features/ManageForm/ManageForm";
import {Header} from "Header";
import {Account} from "types";
import {getAccount} from "utils";

declare const allSubreddits: string[];

function ManageApp() {
  const [account, setAccount] = useState<Account>(null);
  const [loading, setLoading] = useState(true);
  const params = new URLSearchParams(window.location.search);
  const accountUUID = params.has("account_uuid") ? params.get("account_uuid") : undefined;
  if (!accountUUID) return <>Account not found.</>;

  useEffect(() => {
    getAccount(accountUUID).then(data => {
      setAccount(data);
      setLoading(false);
    }).catch(() => {
      alert("Could not fetch account.");
    });
  }, []);

  if (loading) return <>Loading</>;

  return (
    <div className="App">
      <Header></Header>
      <ManageForm
        allSubreddits={allSubreddits}
        account={account}
        setAccount={setAccount}
      ></ManageForm>
      <Footer></Footer>
    </div>
  );
}

export default ManageApp;
