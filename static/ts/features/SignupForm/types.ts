export enum EmailFrequency {
  Daily = "daily",
  Weekly = "weekly",
}

export type SignupData = {
  email: string;
  subreddits: string[];
  captcha_token: string;
  email_interval: EmailFrequency;
}
