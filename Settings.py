from configparser import RawConfigParser

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QToolTip, QWidget, QGroupBox, QGridLayout, QLabel, QTextEdit, QPushButton, \
    QVBoxLayout, QDesktopWidget, QRadioButton, QLayout, QHBoxLayout, QLineEdit


class Settings(QMainWindow):

    def __init__(self, *__args):
        super().__init__(*__args)
        self.init_ui()

    def init_ui(self):
        self.config = RawConfigParser()
        self.config.read("././resources/application.properties")

        self.sentiments_config = dict(self.config.items('Sentiments Settings'))

        self.setGeometry(350, 350, 250, 150)
        self.setWindowTitle('System settings')
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip("This is a tooltip")

        central_widget = QWidget(self)

        self.sentiments_groupBox = QGroupBox("Sentiments Analysis Settings")
        sentiments_layout = QGridLayout()

        self.default_model_rb = QRadioButton("Use default sentiments model")
        self.custom_model_rb = QRadioButton("Use custom sentiments model")

        selected_model = self.sentiments_config["sentiments.model"]

        if selected_model == "default":
            self.default_model_rb.setChecked(True)
        else:
            self.custom_model_rb.setChecked(True)

        self.tweets_number = self.sentiments_config["tweets.to.download"]

        label = QLabel("Tweets to download")
        self.edit = QLineEdit()
        self.edit.setText(str(self.tweets_number))

        sentiments_layout.addWidget(self.default_model_rb, 0, 0)
        sentiments_layout.addWidget(self.custom_model_rb, 1, 0)
        sentiments_layout.addWidget(label, 3, 0)
        sentiments_layout.addWidget(self.edit, 3, 1)

        self.sentiments_groupBox.setLayout(sentiments_layout)

        save_button = QPushButton("Save Settings")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_clicked)
        save_button.clicked.connect(self.save_settings_clicked)

        bottom_widget = QWidget(self)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_widget.setLayout(bottom_layout)
        bottom_layout.addWidget(save_button)
        bottom_layout.addWidget(cancel_button)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(self.sentiments_groupBox)
        window_layout.addWidget(bottom_widget)

        central_widget.setLayout(window_layout)

        self.setCentralWidget(central_widget)

        self.center()

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

    def save_settings_clicked(self):
        try:
            if self.default_model_rb.isChecked():
                self.config.set('Sentiments Settings', "sentiments.model", "default")
            else:
                self.config.set('Sentiments Settings', "sentiments.model", "custom")
            self.config.set('Sentiments Settings', "tweets.to.download", str(self.edit.text()))
            with open("././resources/application.properties", "r+") as config_file:
                self.config.write(config_file)
        except Exception as ex:
            print(ex)

        self.destroy()
