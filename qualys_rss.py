import urllib3, xmltodict

def post_to_splunk(item):
    return item

def get_rss_data(url='https://status.qualys.com/history.rss'):
    response = urllib3.PoolManager().request('GET', url)
    data = xmltodict.parse(response.data)
    return data['rss']['channel']['item']

previous_item_title = 'place holder'
for item in get_rss_data():
    if item['title'] == previous_item_title:
        break
    else:
        post_to_splunk(item)
