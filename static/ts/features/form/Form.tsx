import React from "react";

import {useAppSelector, useAppDispatch} from "app/hooks";
import {
  getSubreddits,
  updateEmail,
  selectEmail,
} from "features/form/formSlice";

export function Form() {
  const email = useAppSelector(selectEmail);
  // const dispatch = useAppDispatch();
  // can eventually dispatch getSubreddits

  return (
    <div>
      <input value={email} onChange={(e) => updateEmail(e.target.value)} />
    </div>
  );
}
