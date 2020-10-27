import requests
import json
from authorize import token


def post_request():
    body = {'query':  'query {_subscriptionStats {count}}'}

    data_to_send = {
        'query': 'query {_subscriptionStats (filterString: \"status = ACTIVE\") {count}}'}

    url = 'https://www.beverage-digest.com/query'

    headers = {'Content-Type': 'application/json',
    'Authorization': f'{token}'}

    response = requests.post(url, data=json.dumps(data_to_send), headers=headers)

    json_data = response.json()

    sub_count_active_only = json_data['data']['_subscriptionStats']['count']

    sub_count = sub_count_active_only - 22

    return sub_count
