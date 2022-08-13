export enum EmailFrequency {
  Daily = "daily",
  Weekly = "weekly",
}

export type SignupData = {
  email: string;
  subreddits: string[];
  captchaToken: string;
  emailInterval: EmailFrequency;
}
