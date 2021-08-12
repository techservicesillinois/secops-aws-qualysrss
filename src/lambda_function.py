import requests, xmltodict, json, os, boto3, dateutil.parser

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
    headers = {
        'Authorization':(f"Splunk {os.environ['HEC_TOKEN']}")
    }

    payload = {
        'host':caller_identity['Arn'],
        'source':os.environ['QUALYS_URL'],
        'sourcetype':'hec:test',
        'fields':{
            'forwarder':(f"ACCT# {caller_identity['Account']}")
        },
        'event':clean_item(item)
    }

    requests.post(os.environ['HEC_ENDPOINT'], data=json.dumps(payload), headers=headers)
    log_item_sent(item['guid'])

def get_rss_data(url=os.environ['QUALYS_URL']):
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    return data['rss']['channel']['item']

def get_dynamo():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    return table

def log_item_sent(guid):
    table = get_dynamo()
    table.put_item(
        Item={
                'guid':guid
        }
    )

def check_if_should_sent(guid):
    table = get_dynamo()
    response = table.get_item(Key={'guid':guid})
    if 'Item' in response:
        return False
    else:
        return True

def lambda_handler(event, context):
    for item in get_rss_data():
        if check_if_should_sent(item['guid']):
            post_to_splunk(item)
