import requests, xmltodict, json, os, datetime, boto3, dateutil.parser

# This is used to populate metadata in the Splunk event without hard coding the values
caller_identity = boto3.client('sts').get_caller_identity()

def clean_item(item):
    # The "description" field is just raw HTML that is available in human readable form via the "link" field so it's removed to make the events smaller
    del item['description']

    # Splunk wants a field named "timestamp" and prefers iso format so it's converted and renamed.
    item['timestamp'] = dateutil.parser.parse(item['pubDate']).isoformat()
    del item['pubDate']

    return item

def post_to_splunk(item):
    headers = {'Authorization':f"Splunk {os.environ['HEC_TOKEN']}"}

    payload = {
        'host':caller_identity['Arn'],
        'source':os.environ['QUALYS_URL'],
        'sourcetype':'hec:test',
        'fields':{'forwarder':(f"ACCT# {caller_identity['Account']}")},
        'event':clean_item(item)
    }

    requests.post(os.environ['HEC_ENDPOINT'], data=json.dumps(payload), headers=headers)

def get_rss_data(url=os.environ['QUALYS_URL']):
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    return data['rss']['channel']['item']

def lambda_handler(event, context):
    for item in get_rss_data():
        post_to_splunk(item)
