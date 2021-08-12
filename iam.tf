data "aws_iam_policy_document" "trust" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com",
      ]
    }
  }
}

data "aws_iam_policy_document" "dynamodb_access" {
  statement {
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"]
    resources = [resource.aws_dynamodb_table.qualys_rss.arn]
  }
}

resource "aws_iam_policy" "dynamodb_access" {
  name        = "qualys_rss_dynamodb_rw"
  description = "allows for reading and writing of the qualyss_rss table"
  policy      = data.aws_iam_policy_document.dynamodb_access.json
}

resource "aws_iam_role" "default" {
  name_prefix = var.name
  description = "Role for Lambda function ${var.name}"

  assume_role_policy = data.aws_iam_policy_document.trust.json
}

resource "aws_iam_role_policy_attachment" "lambda" {
  role       = aws_iam_role.default.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "dynamodb_access" {
  role       = aws_iam_role.default.name
  policy_arn = aws_iam_policy.dynamodb_access.arn
}
