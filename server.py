from flask import Flask, request
import requests, json, os

app = Flask(__name__)
app.config['DEVELOPMENT'] = True

TOKEN_BOT = os.environ['BOT_TOKEN_TELEGRAM']
TOKEN_CHAT = os.environ['BOT_TOKEN_TELEGRAM_CHAT']
TOKEN_PHILIPS_HUE = os.environ['TOKEN_PHILIPS_HUE']
URL_PHILIPS_HUE = os.environ['URL_PHILIPS_HUE']

url_telegram = "https://api.telegram.org/bot" + TOKEN_BOT
url_philipshue = URL_PHILIPS_HUE + TOKEN_PHILIPS_HUE

@app.route('/webhooktelegram', methods=['POST', 'GET'])
def web_hook_telegram():
    try:
        data = request.json
        input_user = data['message']['text']
        if input_user == '/on':
            return sendMessageOn()
        if input_user == '/off':
            return sendMessageOff()
        if input_user == 'Blanco':
            return setColor([0.3,0.3])
        if input_user == 'Verde':
            return setColor([0.1,0.6])
        if input_user == 'Rojo':
            return setColor([0.7,0.3])
        if input_user == 'Azul':
            return setColor([0.1,0.2])
        if input_user == 'Violeta':
            return setColor([0.4,0.2])
        if input_user == 'Amarillo':
            return setColor([0.52,0.42])
    except:
        return '500'
    return '200'

def sendMessageOn():
    message = '¿Qué color de luz deseas?'
    payload = { 
    'chat_id': TOKEN_CHAT, 
    'text': message, 
    'parse_mode':'HTML',
    'reply_markup':{'keyboard':[[{'text':'Blanco'}],[{'text':'Verde'}],[{'text':'Azul'}],[{'text':'Rojo'}],[{'text':'Amarillo'}],[{'text':'Violeta'}]], 'one_time_keyboard': True }
    }
    headers = { 'Content-type': 'application/json' }
    requests.request('POST', url_telegram + '/sendMessage', json=payload, headers=headers)
    return '200'

def sendMessageOff():
    setLights({ 'on' : False })
    sendMessage('Se han apagado las luces.')
    return '200'

def setColor(hue):
    setLights({ 'on' : True, 'xy': hue })
    sendMessage('Se han encendido las luces.')
    return '200'

def setLights(payload):
    headers = { 'Content-type': 'application/json' }
    requests.request('PUT', url_philipshue + '/lights/1/state', json=payload, headers=headers)
    requests.request('PUT', url_philipshue + '/lights/2/state', json=payload, headers=headers)
    requests.request('PUT', url_philipshue + '/lights/3/state', json=payload, headers=headers)

def sendMessage(message):
    payload = { 
    'chat_id': TOKEN_CHAT, 
    'text': message, 
    }
    headers = { 'Content-type': 'application/json' }
    requests.request('POST', url_telegram + '/sendMessage', json=payload, headers=headers)
    return '200'

if __name__ == '__main__': app.run(debug=True, port=4000)