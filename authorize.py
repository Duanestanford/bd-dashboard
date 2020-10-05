import requests
import os
import json

headers = {'Content-Type': 'application/json',}


response = requests.post('https://www.beverage-digest.com/query', json={'query':'mutation {tokenCreate(email: \"' + os.getenv('EMAIL') + '\",password: \"' + os.getenv('PASSWORD') + '\",admin: true){ token expiresAt } }'})

json_response = response.json()

token = f"token {json_response['data']['tokenCreate']['token']}"
