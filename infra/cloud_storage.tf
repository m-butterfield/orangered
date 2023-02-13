resource "google_storage_bucket" "orangered" {
  name                        = "orangered.email"
  location                    = "US"
  uniform_bucket_level_access = true
  website {
    main_page_suffix = "index.html"
  }
}

resource "google_storage_bucket_iam_member" "orangered_public" {
  bucket = google_storage_bucket.orangered.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_compute_global_address" "orangered" {
  name = "orangered"
}

resource "google_compute_managed_ssl_certificate" "orangered" {
  name = "orangered"

  managed {
    domains = ["orangered.email"]
  }
}

resource "google_compute_backend_bucket" "orangered" {
  name        = "orangered"
  bucket_name = google_storage_bucket.orangered.name
}

resource "google_compute_url_map" "orangered" {
  name            = "orangered"
  default_service = google_compute_backend_bucket.orangered.id
}

resource "google_compute_target_https_proxy" "orangered" {
  name             = "orangered-target-proxy"
  url_map          = google_compute_url_map.orangered.id
  ssl_certificates = [google_compute_managed_ssl_certificate.orangered.id]
}

resource "google_compute_global_forwarding_rule" "orangered" {
  name       = "orangered"
  target     = google_compute_target_https_proxy.orangered.id
  ip_address = google_compute_global_address.orangered.address
  port_range = 443
}

# begin http -> https redirect

resource "google_compute_url_map" "orangered_http" {
  name = "orangered-http"
  default_url_redirect {
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
    https_redirect         = true
  }
}

resource "google_compute_target_http_proxy" "orangered_http" {
  name    = "orangered-http"
  url_map = google_compute_url_map.orangered_http.self_link
}

resource "google_compute_global_forwarding_rule" "orangered_http" {
  name       = "orangered-http"
  target     = google_compute_target_http_proxy.orangered_http.self_link
  ip_address = google_compute_global_address.orangered.address
  port_range = "80"
}
