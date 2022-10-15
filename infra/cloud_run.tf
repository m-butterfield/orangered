resource "google_cloud_run_service" "orangered" {
  name     = "orangered"
  location = var.default_region

  template {
    spec {
      containers {
        image = "gcr.io/mattbutterfield/orangered.email"
        ports {
          container_port = 8000
        }
        env {
          name  = "SERVER_NAME"
          value = "orangered.email"
        }
        env {
          name  = "PGDATABASE"
          value = "orangered"
        }
        env {
          name  = "PGUSER"
          value = "orangered"
        }
        env {
          name = "PGPASSWORD"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.orangered_db_password.secret_id
              key  = "latest"
            }
          }
        }
        env {
          name = "PGHOST"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.orangered_db_host.secret_id
              key  = "latest"
            }
          }
        }
        env {
          name = "RECAPTCHA_SITE_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.orangered_recaptcha_site_key.secret_id
              key  = "latest"
            }
          }
        }
        env {
          name = "RECAPTCHA_SECRET_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.orangered_recaptcha_secret_key.secret_id
              key  = "latest"
            }
          }
        }
        env {
          name = "SENDGRID_API_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.orangered_sendgrid_api_key.secret_id
              key  = "latest"
            }
          }
        }
      }
      service_account_name = google_service_account.orangered_cloud_run.email
    }
    metadata {
      annotations = {
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.mattbutterfield.connection_name
        "autoscaling.knative.dev/maxScale"      = "100"
        "client.knative.dev/user-image"         = "gcr.io/mattbutterfield/orangered.email"
        "run.googleapis.com/client-name"        = "gcloud"
        "run.googleapis.com/client-version"     = "396.0.0"
      }
    }
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.orangered.location
  project  = google_cloud_run_service.orangered.project
  service  = google_cloud_run_service.orangered.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

resource "google_cloud_run_domain_mapping" "orangered" {
  location = var.default_region
  name     = "orangered.email"

  metadata {
    namespace = var.project
  }

  spec {
    route_name = google_cloud_run_service.orangered.name
  }
}

# note: we need this to invoke the cloud run job that sends the emails, triggered by the send-emails scheduler
# cloud run jobs are not supported by terraform yet so I created it in the console, it is very similar to the cloud
# run service above just with a different command to start it and different env variables for scraping and sending.
resource "google_project_iam_member" "mattbutterfield_cloud_run_invoker" {
  project = var.project
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}
