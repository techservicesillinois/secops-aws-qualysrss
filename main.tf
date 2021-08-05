locals {
  lambda_zip = "qualys_rss.zip"
}

resource "aws_lambda_function" "default" {
  description      = "Forwards the Qualys outage feed to the Splunk HEC."
  function_name    = var.name
  runtime          = var.runtime
  publish          = true
  role             = aws_iam_role.default.arn
  filename         = local.lambda_zip
  source_code_hash = filebase64sha256(local.lambda_zip)
}
