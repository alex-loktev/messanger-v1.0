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
    factory: 'Server'
    login: str = None

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

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
            if content.startswith("login:"):
                for user in self.factory.clients:
                    if content[6:] == user.login:
                        self.sendLine("Connect error 11".encode())
                        self.transport.loseConnection()

                    else:
                        self.login = content[6:]
                        self.sendLine("Success connect!".encode())
                        self.send_history()
                        break

            else:
                self.sendLine("Connect error".encode())
                self.transport.loseConnection()


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list
    messages: list

    def startFactory(self):
        self.clients = []
        self.messages = []
        print("Server start")


reactor.listenTCP(1234, Server())
reactor.run()
