# Overview

Provides a Lambda function for forwarding Qualys outage & maintenance events to Splunk via the HTTP Event Collector (HEC). A log of events sent is kept in DynamoDB to prevent duplicate events in Splunk.

Argument Reference
-----------------

The following arguments are supported:

* `function_name` - (Optional) Name of the lambda function and role
to be deployed (Default qualys-rss-to-splunk).

* `runtime` - (Optional) Lambda function's runtime environment
(Default python3.8).

* `qualys_url` - (Optional) URL for the Qualys RSS feed
(Default https://status.qualys.com/history.rss).

* `hec_endpoint` - (Optional) URL for the Splunk HEC endpoint
(Default https://splunk-hec.machinedata.illinois.edu:8088/services/collector).

* `hec_token` - (Required) Auth token for the Splunk HEC endpoint

# Testing
1) The Makefile is set up with tests for the terraform and zip file. The zip file must be kept up to date with the source code. Unfortunately the zip must be committed to the repo in order for the terraform validation to function.
```Makefile
make validate
```

# Deployment
1) Create package using
```Makefile
make qualys_rss.zip
```
2) Deploy using terraform and providing the HEC token & region when prompted
```Terraform
terraform init
terraform apply
```
