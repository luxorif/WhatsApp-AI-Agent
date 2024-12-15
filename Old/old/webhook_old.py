import requests
import json


webhook_url = 'https://webhook.site/f154f35a-b2c8-45a0-b0d3-73eb02316499'
data = { 'name': 'This is an example for webhook' }
requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
