export enum EmailFrequency {
  Daily = "daily",
  Weekly = "weekly",
}

export type Account = {
  id: string;
  active: boolean;
  email: string;
  subreddits: string[];
  emailInterval: EmailFrequency;
}

export type HeaderLink = {
  name: string;
  href: string;
}
