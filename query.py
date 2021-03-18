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

    # Free Subs as of 2020/12/09: 21

    sub_count = json_data['data']['_subscriptionStats']['count']

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

    return all_delegates


def get_sys():

    count = 0;
    
    template = 'query {orderItems (perPage:100, page:19) {cost id status order {oid email} }}'

    data_to_send = {
        'query': template
        }

    url = 'https://www.beverage-digest.com/query'

    headers = {'Content-Type': 'application/json',
    'Authorization': f'{token}'}

    response = requests.post(url, data=json.dumps(data_to_send), headers=headers)

    json_data = response.json()

    orders = json_data['data']['orderItems']

    sys_sales = {}

    for order in orders:
        if order['cost'] == '895.00 USD' and order['order']['oid'] > 989:
            count +=1
            sys_sales[count] = order['order']['email']


    return (sys_sales, count)
