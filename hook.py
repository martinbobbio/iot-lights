import requests, json, os

TOKEN_BOT = os.environ['BOT_TOKEN_TELEGRAM']

url = "https://api.telegram.org/bot" + TOKEN_BOT

payload = {'url': 'https://52a69dbd7ed7.ngrok.io/webhooktelegram'}
response = requests.request('POST', url + '/setWebHook', json=payload)
data = json.loads(response.text)
if data['ok']:
    print(response.text)
else:
    print('Error')