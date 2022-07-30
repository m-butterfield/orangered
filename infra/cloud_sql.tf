resource "google_sql_database_instance" "mattbutterfield" {
  name             = "mattbutterfield"
  region           = var.default_region
  database_version = "POSTGRES_13"

  settings {
    tier      = "db-f1-micro"
    disk_size = 10
  }
}

resource "google_sql_database" "orangered" {
  name     = "orangered"
  instance = google_sql_database_instance.mattbutterfield.name
}

resource "google_sql_user" "orangered" {
  name     = "orangered"
  instance = google_sql_database_instance.mattbutterfield.name
  password = var.db_password
}

resource "google_service_account" "orangered_cloud_run" {
  account_id = "orangered-cloud-run"
}

resource "google_project_iam_member" "orangered_cloud_run_cloud_sql" {
  project = var.project
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.orangered_cloud_run.email}"
}
