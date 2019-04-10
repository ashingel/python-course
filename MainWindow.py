import sys
from SearchMessages import SearchMessages
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolTip, QMenuBar, QMessageBox, QDesktopWidget

import Settings


class MainWindow(QMainWindow):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.init_ui()

    # init ui interface
    def init_ui(self):
        self.setGeometry(300, 300, 700, 420)
        self.setWindowTitle('Voice of customer prototype')
        QToolTip.setFont(QFont('SansSerif', 10))

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        actionMenu = self.menu_bar.addMenu("&File")
        actionMenu.addAction("Settings", self.settings_action)
        actionMenu.addAction("Exit", self.exit_action)

        twitter_menu = self.menu_bar.addMenu("&Twitter")
        twitter_menu.addAction("Search", self.search_messages)
        twitter_menu.addAction("Report", self.report_messages)

        # help menu
        helpMenu = self.menu_bar.addMenu("&Help")
        helpMenu.addAction("About", self.showhelp)

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def exit_action(self):
        QCoreApplication.instance().quit()

    def settings_action(self):
        self.settings = Settings.Settings(self)
        self.settings.show_window()

    def search_messages(self):
        messages = SearchMessages.launch(self)
        # search_win.show_window()
        print()

    def report_messages(self):
        print("RESULT RETURNED !")

    def showhelp(self):
        QMessageBox.information(self, "Help",
                                "Voice of peoples prototype.\n This is a simple prototype which can help to show\n peoples opinion about the data entered",
                                QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
