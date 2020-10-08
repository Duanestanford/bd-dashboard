import requests
import json
from authorize import token


def post_request():
    body = {'query':  'query {_subscriptionStats {count}}'}

    data_to_send = {
        'query': 'query {_subscriptionStats {count}}'}

    url = 'https://www.beverage-digest.com/query'

    headers = {'Content-Type': 'application/json',
    'Authorization': f'{token}'}

    response = requests.post(url, data=json.dumps(data_to_send), headers=headers)

    json_data = response.json()

    sub_count_with_free = json_data['data']['_subscriptionStats']['count']

    sub_count = sub_count_with_free - 200

    return sub_count
