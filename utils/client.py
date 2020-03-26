import requests

def send_message(username, password, text):
    message={'username': username, 'password': password, 'text': text}
    response=requests.post('http://127.0.0.1:5000/send', json=message)
    return response.status_code == 200

username = input('enter name: ')
password = input('enter password: ')
while True:
    text = input()
    result = send_message(username, password, text)
    if result is False:
        print('Error')
