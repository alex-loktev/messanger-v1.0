#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Графический PyQt 5 клиент для работы с сервером чата
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
import sys
from PyQt5 import QtWidgets
import design


class ConectorProtocol(LineOnlyReceiver):
    factory: 'Connector'

    def connectionMade(self):
        self.factory.window.protocol = self
        self.factory.window.textBrowser.append("Connected")

    def lineReceived(self, line):
        self.factory.window.textBrowser.append(line.decode())


class Connector(ClientFactory):
    protocol = ConectorProtocol
    window: 'ExampleApp'

    def __init__(self, window):
        super().__init__()
        self.window = window


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    reactor = None
    protocol: ConectorProtocol

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        message = self.lineEdit.text()
        self.protocol.sendLine(message.encode())
        self.lineEdit.clear()



app = QtWidgets.QApplication(sys.argv)

window = ExampleApp()
window.show()

import qt5reactor

qt5reactor.install()

from twisted.internet import reactor

reactor.connectTCP("localhost", 1234, Connector(window))

ExampleApp.reactor = reactor
reactor.run()
