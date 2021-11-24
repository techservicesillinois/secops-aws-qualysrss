variable "name" {
  description = "Name of the lambda function to be deployed"
  default     = "qualys-rss-to-splunk"
}

variable "runtime" {
  description = "Lambda function's runtime environment"
  default     = "python3.8"
}

variable "qualys_url" {
  description = "URL for the Qualys RSS feed"
  default     = "https://status.qualys.com/history.rss"
}

variable "hec_endpoint" {
  description = "URL for the Splunk HEC endpoint"
}

variable "hec_token" {
  description = "Auth token for the Splunk HEC endpoint"
}

variable "tags" {
  description = "Tags to be applied to resources where supported"
  type        = map(string)
  default     = {}
}
