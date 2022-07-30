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

resource "google_secret_manager_secret" "orangered_db_ip" {
  secret_id = "orangered-db-ip"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "orangered_db_ip_v1" {
  secret      = google_secret_manager_secret.orangered_db_ip.name
  secret_data = var.db_ip
}

resource "google_secret_manager_secret_iam_member" "cloud_run_orangered_db_ip" {
  project   = var.project
  secret_id = google_secret_manager_secret.orangered_db_ip.secret_id
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
