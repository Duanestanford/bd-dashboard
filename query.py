import requests
import json
from authorize import token


def request_sub_count():

    data_to_send = {
        'query': 'query {_subscriptionStats (filterString: \"status = ACTIVE\") {count}}'
        }

    url = 'https://www.beverage-digest.com/query'

    headers = {'Content-Type': 'application/json',
    'Authorization': f'{token}'}

    response = requests.post(url, data=json.dumps(data_to_send), headers=headers)

    json_data = response.json()

    sub_count_active_only = json_data['data']['_subscriptionStats']['count']

    sub_count = sub_count_active_only - 19

    return sub_count


def request_delegate_count():

    data_to_send = {
        'query':  'query {events (filterString: "title = Beverage Digest Future Smarts 2020") {title _attendantStats {count }}}'
        }

    url = 'https://www.beverage-digest.com/query'

    headers = {'Content-Type': 'application/json',
    'Authorization': f'{token}'}

    response = requests.post(url, data=json.dumps(data_to_send), headers=headers)

    json_data = response.json()

    all_delegates = json_data['data']['events'][0]['_attendantStats']['count']

    paid_delagates = all_delegates - 5

    return paid_delagates
