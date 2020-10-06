import requests
import os
import json

headers = {'Content-Type': 'application/json',}

my_email = str(os.getenv('EMAIL'))
my_password = str(os.getenv('PASSWORD'))


response = requests.post('https://www.beverage-digest.com/query', json={'query':'mutation {tokenCreate(email: \"' + my_email + '\",password: \"' + my_password + '\",admin: true){ token expiresAt } }'})

json_response = response.json()

token = f"token {json_response['data']['tokenCreate']['token']}"
