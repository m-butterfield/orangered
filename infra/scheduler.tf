resource "google_cloud_scheduler_job" "send-emails" {
  name     = "orangered-send-emails"
  schedule = "0 12 * * *"

  http_target {
    http_method = "POST"
    uri         = "https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/mattbutterfield/jobs/orangered-send-emails:run"
    oauth_token {
      service_account_email = google_service_account.orangered_cloud_run.email
    }
  }
}
