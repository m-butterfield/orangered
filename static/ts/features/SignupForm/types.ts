import {EmailFrequency} from "types";

export type SignupFormData = {
  email: string;
  subreddits: string[];
  captchaToken: string;
  emailInterval: EmailFrequency;
}
