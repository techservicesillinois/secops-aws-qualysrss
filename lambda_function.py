import requests, xmltodict, json, os, datetime, boto3, dateutil.parser

qualys_url = 'https://status.qualys.com/history.rss'
# This is used to populate metadata in the Splunk event without hard coding the values
caller_identity = boto3.client('sts').get_caller_identity()

def clean_item(item):
    # The "description" field is just raw HTML that is available in human readable form via the "link" field so it's removed to make the events smaller
    del item['description']

    # The publish date is converted to ISO format to be consistent with Splunk's preferences
    item['pubDate'] = dateutil.parser.parse(item['pubDate']).isoformat()

    # Splunk gets a formatted timestamp for ingestion time
    item['timestamp'] = datetime.datetime.now().isoformat()

    return item

def post_to_splunk(item):
    headers = {'Authorization':f"Splunk {os.environ['HEC_TOKEN']}"}

    payload = {
        'host':caller_identity['Arn'],
        'source':qualys_url,
        'sourcetype':'hec:test',
        'fields':{'Account':caller_identity['Account']},
        'event':clean_item(item)
    }

    requests.post(os.environ['HEC_ENDPOINT'], data=json.dumps(payload), headers=headers)

def get_rss_data(url=qualys_url):
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    return data['rss']['channel']['item']

def lambda_handler(event, context):
    for item in get_rss_data():
        post_to_splunk(item)
