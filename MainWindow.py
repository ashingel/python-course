import sys
from SearchMessages import SearchMessages
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolTip, QMenuBar, QMessageBox, QDesktopWidget, QWidget, \
    QVBoxLayout, QTableView, QCheckBox, QComboBox, QHBoxLayout, QPushButton, QGridLayout, QLabel, QRadioButton

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

        self.connection_manager = db.ConnectionManager(None)
        show_button = QPushButton("Show")
        show_button.clicked.connect(self.query_changed)

        queries = self.connection_manager.get_queries_items()

        for item in queries:
            self.queries_combo_box.addItem(item[0])

        self.polarity_combo = QComboBox(self)
        self.polarity_combo.addItem("All Polarity")
        self.polarity_combo.addItem("Positive")
        self.polarity_combo.addItem("Neutral")
        self.polarity_combo.addItem("Negative")

        label = QLabel("Query :")
        polarity_label = QLabel("Polarity Type :")

        self.text_rb = QRadioButton("Show as Table ")
        self.text_rb.setChecked(True)
        self.histogram_rb = QRadioButton("Show as Histogram")

        main_layout = QGridLayout(self)

        self.right_layout = QVBoxLayout(self)

        left_widget = QWidget()
        right_widget = QWidget()

        left_layout = QVBoxLayout(self)
        left_layout.addWidget(label)
        left_layout.addWidget(self.queries_combo_box)
        left_layout.addWidget(polarity_label)
        left_layout.addWidget(self.polarity_combo)
        left_layout.addWidget(self.queries_combo_box)

        left_layout.addWidget(self.text_rb)
        left_layout.addWidget(self.histogram_rb)

        left_layout.addWidget(show_button)

        self.report_table = QTableView(self)
        self.right_layout.addWidget(self.report_table)

        left_widget.setLayout(left_layout)
        right_widget.setLayout(self.right_layout)

        main_layout.addWidget(left_widget, 0, 0)
        main_layout.addWidget(right_widget, 0, 1)

        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

        # sentiment_df = pd.DataFrame()

    def showhelp(self):
        QMessageBox.information(self, "Help",
                                "Voice of peoples prototype.\n This is a simple prototype which can help to show\n peoples opinion about the data entered",
                                QMessageBox.Ok)

    def query_changed(self):
        query = self.queries_combo_box.currentText()
        polarity = self.polarity_combo.currentText()
        # tweets = self.connection_manager.get_polarity_messages(query)
        tweets = self.connection_manager.get_polarity_messages(query, polarity)

        if self.histogram_rb.isChecked():

            sentiment_df = pd.DataFrame(tweets)

            fig, ax = plt.subplots(figsize=(8, 6))

            # Plot histogram with break at zero
            sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1],
                              ax=ax,
                              color="blue")

            plt.title("Sentiments from Tweets " + query)
            plt.show()
        else:
            if tweets is not None:
                if self.report_table is None:
                    self.report_table = QTableView(self)
                else:
                    self.right_layout.removeWidget(self.report_table)

                self.report_tweets_model = QStandardItemModel()
                self.report_table.setModel(self.report_tweets_model)
                # Do the resize of the columns by content
                self.report_tweets_model.setColumnCount(1)
                headers = ("Text",)
                self.report_tweets_model.setHorizontalHeaderLabels(headers)
                for i in range(len(tweets)):
                    tweet = tweets[i]
                    column_1 = QStandardItem((tweet[0]))
                    self.report_tweets_model.setItem(i, 0, column_1)

                self.report_table.resizeColumnsToContents()

                self.right_layout.addWidget(self.report_table)

                self.report_table.setGeometry(self.central_widget.geometry())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
