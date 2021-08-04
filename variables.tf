variable "name" {
  description = "Name of the lambda function to be deployed"
  default     = "qualys-rss-to-splunk"
}

variable "runtime" {
  description = "Lambda function's runtime environment"
  default     = "python3.7"
}
