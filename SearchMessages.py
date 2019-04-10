import os

from PyQt5 import QtGui, QtCore

from db import ConnectionManager as db
from ml import TweetPolarityClassifier as pclassifier
from twitter.TweetsDownloader import TweetsDownloader

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QToolTip, QWidget, QGridLayout, QLabel, QPushButton, \
    QDesktopWidget, QHBoxLayout, QCalendarWidget, QLineEdit, QDialog


class SearchMessages(QDialog):

    # def __init__(self, *__args):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(450, 350, 250, 250)
        self.setWindowTitle('Search Messages')
        QToolTip.setFont(QFont('SansSerif', 10))

        central_widget = QWidget(self)

        search_layout = QGridLayout()
        search_layout.setSpacing(10)

        search_label = QLabel("Enter query : ")
        self.query_edit = QLineEdit(self)

        search_layout.addWidget(search_label, 1, 0)
        search_layout.addWidget(self.query_edit, 1, 1, 1, 1)

        self.date_label = QLabel(self)
        calender = QCalendarWidget(self)
        calender.setGridVisible(True)
        calender.clicked[QDate].connect(self.showDate)
        calender.clicked.connect(self.showDate)
        date = calender.selectedDate()
        self.date_label.setText(date.toString())

        search_layout.addWidget(calender, 2, 1)
        search_layout.addWidget(self.date_label, 2, 0)

        search_button = QPushButton("Search")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_clicked)
        search_button.clicked.connect(self.search_clicked)

        bottom_widget = QWidget(self)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_widget.setLayout(bottom_layout)
        bottom_layout.addWidget(search_button)
        bottom_layout.addWidget(cancel_button)

        search_layout.addWidget(bottom_widget, 3, 1, 1, 1)

        self.setLayout(search_layout)

        # self.setCentralWidget(central_widget)

        self.center()

    @classmethod
    def launch(cls, parent=None):
        dlg = cls(parent)
        dlg.exec_()
        messages = dlg.messages
        return messages

    def set_connection(self, connection):
        self.connection = connection

    def show_window(self):
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def cancel_clicked(self):
        self.destroy()

    def search_clicked(self):
        query = self.query_edit.text()
        tw_loader = TweetsDownloader()
        # format '2019-04-04'

        since_date = self.date_label.text()

        self.messages = tw_loader.get_tweet_messages(query, since_date)

        path_to_db = os.getcwd() + "/resources/tweets.db"

        classifier = pclassifier.TweetPolarityClassifier()
        classifier.classify_tweets(self.messages)

        connection_manager = db.ConnectionManager(path_to_db)
        connection_manager.save_messages(self.messages, query)
        self.close()

    def showDate(self, date):
        self.date_label.setText(date.toString("yyyy-MM-dd"))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
