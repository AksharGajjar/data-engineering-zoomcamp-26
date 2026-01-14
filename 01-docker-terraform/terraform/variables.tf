variable "google_credentials" {
  description = "Google Service Runner Credentials"
  default     = "/workspaces/data-engineering-zoomcamp-26/.secrets/google-service-runner-creds.json"
}

variable "project" {
  description = "Project Name"
  default     = "taxi-rides-ny-483918"
}

variable "region" {
  description = "Default Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

// Needs to be globally unique across all of google cloud
variable "bq_dataset_name" {
  description = "My BigQuery Dataset"
  default     = "taxi_rides_ny_483918_terraform_example_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "taxi_rides_ny_483918_terraform_bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}