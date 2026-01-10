terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.15.0"
    }
  }
}

provider "google" {
  project     = "taxi-rides-ny-483918"
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "taxi-rides-ny-483918-terraform-bucket" // Needs to be globally unique across all of google cloud
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}