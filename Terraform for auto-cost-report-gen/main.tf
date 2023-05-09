terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

module "iam_policy" {
  source  = "cloudposse/iam-policy/aws"
  # Cloud Posse recommends pinning every module to a specific version
  # version = "x.x.x"

  iam_policy_statements = {
    terraform1 = {
      effect     = "Allow"
      actions    = ["*"]
      resources  = ["*"]
      conditions = []
    }
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda_terraform"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  inline_policy {
            name = "test_policy"
            policy = module.iam_policy.json
  }
}


data "archive_file" "lambda" {
  type        = "zip"
  source_file = "lambda.py"
  output_path = "lambda_function_terraform.zip"
}

resource "aws_lambda_layer_version" "lambda_layer_1" {
  filename   = "datetime-terraform.zip"
  layer_name = "lambda_datetime_layer_tf"

  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_layer_version" "lambda_layer_2" {
  filename   = "tabulate-terraform.zip"
  layer_name = "lambda_tabulate_layer_tf"

  compatible_runtimes = ["python3.9"]
}

#data "aws_lambda_layer_version" "lambda_layer_3" {
  #layer_name = "AWSSDKPandas-Python39"
#}

resource "aws_lambda_function" "lambda_test" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda_function_terraform.zip"
  function_name = "${var.lambda_name}"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda.lambda_handler"
  layers = [aws_lambda_layer_version.lambda_layer_1.arn, aws_lambda_layer_version.lambda_layer_2.arn, "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:4" ]
  runtime = "python3.9"
  tags = {
    owner = "aws"
    project = "devops"
    team = "aws"
    environment = "dev"
  }
}

resource "aws_cloudwatch_event_rule" "my_rule" {
  name        = "my-cron-rule-tf"
  schedule_expression = "cron(030 4 * * ? *)" # Runs every day at 10am IST
}

resource "aws_cloudwatch_event_target" "my_target" {
  rule      = aws_cloudwatch_event_rule.my_rule.name
  arn       = aws_lambda_function.lambda_test.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda_test.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.my_rule.arn
}
resource "aws_ses_email_identity" "email_1" {
  email = "jayasree.gundasu@cloudangles.com"
}

resource "aws_ses_email_identity" "email_2" {
  email = "sahithpalika@cloudangles.com"
}