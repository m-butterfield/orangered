import {Account} from "types";

declare const APP_BASE_URL: string;
export const APP_BASE = APP_BASE_URL;

export const getAccount = async (accountID: string): Promise<Account> => {
  return await (await fetch(`${APP_BASE}/account/${accountID}`)).json();
};
