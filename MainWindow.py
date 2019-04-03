import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolTip, QMenuBar, QMessageBox, QDesktopWidget

import twitter.TweetsDownloader as twd


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
        actionMenu.addAction("Exit", self.exit_action)

        # help menu
        helpMenu = self.menu_bar.addMenu("&Help")
        helpMenu.addAction("About", self.showhelp)

        self.center()
        # try:
        #     twitter_downloader = twd.TweetsDownloader()
        #     twitter_downloader.get_tweet_messages()
        # except Exception as ex:
        #     print(ex)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def exit_action(self):
        QCoreApplication.instance().quit()

    def showhelp(self):
        QMessageBox.information(self, "Help",
                                "Voice of peoples prototype.\n This is a simple prototype which can help to show\n peoples opinion about the data entered",
                                QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
