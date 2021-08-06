#Overview

Provides a Lambda function for forwarding Qualys outage & maintenance events to Splunk via the HTTP Event Collector (HEC).

Argument Reference
-----------------

The following arguments are supported:

* `function_name` - (Optional) Name of the lambda function and role
to be deployed (Default qualys-rss-to-splunk).

* `runtime` - (Optional) Lambda function's runtime environment
(Default python3.7).

* `qualys_url` - (Optional) URL for the Qualys RSS feed
(Default https://status.qualys.com/history.rss).

* `hec_endpoint` - (Optional) URL for the Splunk HEC endpoint
(Default https://splunk-hec.machinedata.illinois.edu:8088/services/collector).

* `hec_token` - (Required) Auth token for the Splunk HEC endpoint

#Deployment
1) Create package using
```Makefile
make qualys_rss.zip
```
2) Deploy using terraform and providing the HEC token & region when prompted
```Terraform
terraform init
terraform apply
```

#To-Do
* Impliment a way to track last sent event, likely a SQS queue. The entire RSS feed it pulled everytime so the last sent event GUID should be recorded somewhere so that duplicate events are not forwarded to Splunk.
