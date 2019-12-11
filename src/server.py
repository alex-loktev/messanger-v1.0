#  Created by Alexey Loktev
#  loktev.lesha@gmail.com
#
#  Copyright © 2019
#
#  Сервер для обработки сообщений от клиентов
#
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class ServerProtocol(LineOnlyReceiver):
    factory = 'Server'
    login: str = None

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)
        self.factory.logins.remove(self.login)

    def connectionMade(self):
        self.factory.clients.append(self)

    def send_history(self):
        for message in self.factory.messages:
            self.sendLine(message.encode())

    def lineReceived(self, line):
        content = line.decode()

        if self.login is not None:
            content = f"Message from {self.login}: {line}"
            self.factory.messages.append(content)
            if len(self.factory.messages) > 10:
                self.factory.messages.remove(self.factory.messages[0])

            for user in self.factory.clients:
                if user is not self:
                    user.sendLine(content.encode())

        else:
            if (content.startswith("login")) and not (content[6:] in self.factory.logins):
                self.login = content.replace("login:", "")
                self.factory.logins.append(self.login)
                self.sendLine("Success connect!".encode())
                self.send_history()

            else:
                self.sendLine("Connect error".encode())
                self.connectionLost()


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list
    logins: list
    messages: list

    def startFactory(self):
        self.clients = []
        self.logins = []
        self.messages = []
        print("Server start")


reactor.listenTCP(1234, Server())
reactor.run()
