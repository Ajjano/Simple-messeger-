# qt.io
# https://build-system.fman.io/qt-designer-download
# https://www.riverbankcomputing.com/software/pyqt/download5

# pip install PyQt5
# pyuic5 messenger.ui -o clientui.py
import datetime

from PyQt5 import QtWidgets, QtCore
import clientui
import requests

class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.pressed.connect(self.button_pushed)
        self.after=0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def button_pushed(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()
        self.send_message(username, password, text)
        self.textEdit.setText('')
        self.textEdit.repaint()


    def send_message(self, username, password, text):
        message={'username': username, 'password': password, 'text': text}
        try:
            response=requests.post('http://127.0.0.1:5000/send', json=message)
            if response.status_code == 401:
                self.show_twxt('bad password')
            elif response.status_code != 200:
                self.show_twxt('connection error')
        except:
            self.show_twxt('connection error')


    def update_messages(self):
        try:
            response = requests.get('http://127.0.0.1:5000/messages',
                                    params={'after': self.after})
            data = response.json()
            for message in data['messages']:
                self.print_message(message)
                self.after=message['time']
        except:
            print('connection error')


    def print_message(self, message):
        username = message['username']
        message_time = message['time']
        text = message['text']

        dt = datetime.datetime.fromtimestamp(message_time)

        self.show_twxt(f"{dt.strftime('%H:%M:%S')} {username}\n{text}\n\n")

    def show_twxt(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()

app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec_()
