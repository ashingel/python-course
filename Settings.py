from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QToolTip, QWidget, QGroupBox, QGridLayout, QLabel, QTextEdit, QPushButton, \
    QVBoxLayout, QDesktopWidget, QRadioButton


class Settings(QMainWindow):

    def __init__(self, *__args):
        super().__init__(*__args)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(350, 350, 450, 220)
        self.setWindowTitle('Add Record')
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip("This is a tooltip")

        central_widget = QWidget(self)

        self.groupBox = QGroupBox("Sentiments Analysis Settings")
        self.group_box_bottom = QGroupBox()

        layout = QGridLayout(central_widget)

        self.default_model_rb = QRadioButton("Use default sentiments model")
        self.custom_model_rb = QRadioButton("Use custom sentiments model")
        save_button = QPushButton("Save Settings")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_clicked)
        save_button.clicked.connect(self.save_settings_clicked)

        layout.addWidget(self.default_model_rb, 0, 0)
        layout.addWidget(self.custom_model_rb, 1, 0)

        bottom_widget = QWidget(self)
        bottom_layout = QGridLayout(bottom_widget)
        bottom_widget.setLayout(bottom_layout)

        self.bottom_layout.addWidget(save_button, 1, 0)
        self.bottom_layout.addWidget(cancel_button, 2, 0)

        self.groupBox.setLayout(bottom_layout)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(self.groupBox)
        window_layout.addWidget(self.group_box_bottom)

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
        column_one = self.column_one_edit.toPlainText()
        column_two = self.column_two_edit.toPlainText()
        insert_sql = "INSERT INTO database_one (column_one,column_two) VALUES('{}','{}')".format(column_one, column_two)
        self.destroy()
