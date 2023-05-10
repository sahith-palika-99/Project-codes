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

resource "aws_cloudwatch_event_rule" "console" {
  name        = "resource-test-tf"
  description = "notify new resource created"

  event_pattern = jsonencode({
    source = ["aws.config"]
    detail-type = ["Config Configuration Item Change"]
     detail = {
        messageType = ["ConfigurationItemChangeNotification"]
        configurationItem = {
            resourceType = ["AWS::S3::BUCKET"]
            configurationItemStatus = ["ResourceDiscovered"]
        }
     }
  })
}

resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.console.name
  target_id = "SendToSNS"
  arn       = data.aws_sns_topic.example.arn

  input_transformer {
    input_paths = {
        awsRegion = "$.detail.configurationItem.awsRegion",
        awsAccountId = "$.detail.configurationItem.awsAccountId",
        resource_type = "$.detail.configurationItem.resourceType",
        resource_ID = "$.detail.configurationItem.resourceId",
        configurationItemCaptureTime = "$.detail.configurationItem.configurationItemCaptureTime"
    
    }
    input_template = "\"a new <resource_type> has been created with Id <resource_ID> on <configurationItemCaptureTime> in the account <awsAccountId> in the region <awsRegion>.\""
  }
}


data "aws_sns_topic" "example" {
  name = "cost-explorer"
}