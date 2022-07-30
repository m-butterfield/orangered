resource "google_secret_manager_secret" "orangered_db_password" {
  secret_id = "orangered-db-password"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_db_password_v1" {
  secret      = google_secret_manager_secret.orangered_db_password.name
  secret_data = var.db_password
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_db_password" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_db_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}

resource "google_secret_manager_secret" "orangered_db_host" {
  secret_id = "orangered-db-host"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_db_host_v1" {
  secret      = google_secret_manager_secret.orangered_db_host.name
  secret_data = var.db_host
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_db_host" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_db_host.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}

resource "google_secret_manager_secret" "orangered_recaptcha_site_key" {
  secret_id = "orangered-recaptcha-site-key"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_recaptcha_site_key_v1" {
  secret      = google_secret_manager_secret.orangered_recaptcha_site_key.name
  secret_data = var.recaptcha_site_key
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_recaptcha_site_key" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_recaptcha_site_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}

resource "google_secret_manager_secret" "orangered_recaptcha_secret_key" {
  secret_id = "orangered-recaptcha-secret-key"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_recaptcha_secret_key_v1" {
  secret      = google_secret_manager_secret.orangered_recaptcha_secret_key.name
  secret_data = var.recaptcha_secret_key
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_recaptcha_secret_key" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_recaptcha_secret_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}

resource "google_secret_manager_secret" "orangered_mailjet_api_key" {
  secret_id = "orangered-mailjet-api-key"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_mailjet_api_key_v1" {
  secret      = google_secret_manager_secret.orangered_mailjet_api_key.name
  secret_data = var.mailjet_api_key
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_mailjet_api_key" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_mailjet_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}

resource "google_secret_manager_secret" "orangered_mailjet_secret_key" {
  secret_id = "orangered-mailjet-secret-key"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_mailjet_secret_key_v1" {
  secret      = google_secret_manager_secret.orangered_mailjet_secret_key.name
  secret_data = var.mailjet_secret_key
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_mailjet_secret_key" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_mailjet_secret_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}

resource "google_secret_manager_secret" "orangered_reddit_client_id" {
  secret_id = "orangered-reddit-client-id"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_reddit_client_id_v1" {
  secret      = google_secret_manager_secret.orangered_reddit_client_id.name
  secret_data = var.reddit_client_id
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_reddit_client_id" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_reddit_client_id.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}

resource "google_secret_manager_secret" "orangered_reddit_client_secret" {
  secret_id = "orangered-reddit-client-secret"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_reddit_client_secret_v1" {
  secret      = google_secret_manager_secret.orangered_reddit_client_secret.name
  secret_data = var.reddit_client_secret
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_reddit_client_secret" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_reddit_client_secret.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}
