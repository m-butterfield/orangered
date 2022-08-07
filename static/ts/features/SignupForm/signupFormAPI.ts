// A mock function to mimic making an async request for data
export function fetchSubreddits(query = "") {
  return new Promise<{ data: string[] }>((resolve) =>
    setTimeout(() => resolve({data: ["analog", "peloton"]}), 500)
  );
}
