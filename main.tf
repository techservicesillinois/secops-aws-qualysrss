locals {
  lambda_zip = "qualys_rss.zip"
}

resource "aws_dynamodb_table" "qualys_rss" {
  name     = var.name
  hash_key = "guid"
  write_capacity = 100
  read_capacity = 100
  attribute {
    name = "guid"
    type = "S"
  }
}

resource "aws_lambda_function" "default" {
  description      = "Forwards the Qualys outage feed to the Splunk HEC."
  function_name    = var.name
  runtime          = var.runtime
  publish          = true
  role             = aws_iam_role.default.arn
  handler          = "lambda_function.lambda_handler"
  filename         = local.lambda_zip
  source_code_hash = filebase64sha256(local.lambda_zip)
  timeout          = 300
  environment {
    variables = {
      HEC_ENDPOINT = var.hec_endpoint
      HEC_TOKEN    = var.hec_token
      QUALYS_URL   = var.qualys_url
      TABLE_NAME   = resource.aws_dynamodb_table.qualys_rss.name
    }
  }
}
