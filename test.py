import os

user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
url = os.getenv('DB_URL')

creds =  f'postgresql://{user}:{password}@{url}/beverages'
print (creds)
