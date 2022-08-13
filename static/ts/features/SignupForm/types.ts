import {EmailFrequency} from "types";

export type SignupData = {
  email: string;
  subreddits: string[];
  captchaToken: string;
  emailInterval: EmailFrequency;
}
