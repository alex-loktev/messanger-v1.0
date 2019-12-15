#  Created by Alexey Loktev
#  loktev.lesha@gmail.com
#
#  Copyright © 2019
#
#  Графический интерфейс PyQt 5
#
#  https://www.qt.io/
#  https://pypi.org/project/PyQt5/
#  https://build-system.fman.io/qt-designer-download
#
#  Пример простой формы на PyQt 5 с обработчиками
#
#  1. pip install PyQt5 - установка пакета
#  2. pip install PyQt5-stubs - подсказки
#  3. pip install qt5reactor - установка пакета
#  4. from PyQt5 import QtWidgets - подключить в файле .py
#
import sys
from PyQt5 import QtWidgets
import design


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def send_message(self):
        message = self.lineEdit.text()
        self.textBrowser.append(message)
        self.lineEdit.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()