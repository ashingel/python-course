import sys
from SearchMessages import SearchMessages
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolTip, QMenuBar, QMessageBox, QDesktopWidget, QWidget, \
    QVBoxLayout, QTableView, QCheckBox, QComboBox, QHBoxLayout, QPushButton

import Settings
import os

import pandas as pd
import matplotlib.pyplot as plt

from db import ConnectionManager as db


class MainWindow(QMainWindow):
    table = None

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

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.table_layout = QVBoxLayout(self)
        self.central_widget.setLayout(self.table_layout)

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
        if messages is not None:
            if self.table is None:
                self.table = QTableView(self)
            else:
                self.table_layout.removeWidget(self.table)

            self.tweets_model = QStandardItemModel()
            self.table.setModel(self.tweets_model)
            # Do the resize of the columns by content
            self.tweets_model.setColumnCount(5)
            headers = ("Name", "Text", "Polarity", "Intensity", "Date")
            self.tweets_model.setHorizontalHeaderLabels(headers)
            for i in range(len(messages)):
                tweet = messages[i]

                column_1 = QStandardItem((tweet.name))
                column_2 = QStandardItem((tweet.twitter_text))
                column_3 = QStandardItem((str(tweet.polarity)))
                column_4 = QStandardItem((str(tweet.intensity)))
                column_5 = QStandardItem((tweet.creation_date.strftime("%m/%d/%Y, %H:%M:%S")))

                self.tweets_model.setItem(i, 0, column_1)
                self.tweets_model.setItem(i, 1, column_2)
                self.tweets_model.setItem(i, 2, column_3)
                self.tweets_model.setItem(i, 3, column_4)
                self.tweets_model.setItem(i, 4, column_5)

                self.table.resizeColumnsToContents()

                self.table_layout.addWidget(self.table)

                self.table.setGeometry(self.central_widget.geometry())

    def report_messages(self):
        self.central_widget.deleteLater()

        self.central_widget = QWidget(self)

        self.queries_combo_box = QComboBox(self)
        # self.queries_combo_box.currentIndexChanged.connect(self.query_changed)

        self.connection_manager = db.ConnectionManager(None)
        show_button = QPushButton("Show")
        show_button.clicked.connect(self.query_changed)

        queries = self.connection_manager.get_queries_items()

        for item in queries:
            self.queries_combo_box.addItem(item[0])

        layout = QHBoxLayout(self)
        layout.addWidget(self.queries_combo_box)
        layout.addWidget(show_button)

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        # sentiment_df = pd.DataFrame()

    def showhelp(self):
        QMessageBox.information(self, "Help",
                                "Voice of peoples prototype.\n This is a simple prototype which can help to show\n peoples opinion about the data entered",
                                QMessageBox.Ok)

    def query_changed(self):
        query = self.queries_combo_box.currentText()
        tweets = self.connection_manager.get_polarity_messages(query)

        # for tweet in tweets:
        #
        #     pass

        sentiment_df = pd.DataFrame(tweets)

        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot histogram with break at zero
        sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1],
                          ax=ax,
                          color="purple")

        plt.title("Sentiments from Tweets " + query)
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
