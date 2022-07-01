import sys
import receivers
import json
from tokenize import String

from functools import partial
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget)

state = 0
tweet_count = 10
class MainWindow(QWidget):

    num_grid_rows = 3
    def __init__(self):
        super().__init__()
        width = 720
        height = 360
        self.setWindowTitle("TwitAPI")
        self.setMinimumSize(width, height)

        layout = QGridLayout()

        #choose mode buttons
        btnFetch = QPushButton(f"Fetch tweets")
        btnLikes = QPushButton(f"Fetch likes")
        btnTime = QPushButton(f"Fetch timeline")

        layout.addWidget(btnFetch, 0, 0)
        layout.addWidget(btnLikes, 1, 0)
        layout.addWidget(btnTime, 2, 0)

        btnFetch.clicked.connect(lambda: mode_switch(1))
        btnLikes.clicked.connect(lambda: mode_switch(2))
        btnTime.clicked.connect(lambda: mode_switch(3))

        #data input code
        lbl_count = QLabel(f"number of tweets to fetch:")
        label1 = QLabel(f"User name to fetch:")
        lblBearer = QLabel(f"Bearer:")
        label2 = QLabel(f"Secret:")
        label4 = QLabel(f"Token:")
        label5 = QLabel(f"Text to send")
        line_count = QLineEdit()
        line_edit1 = QLineEdit()
        line_edit2 = QLineEdit()
        line_edit3 = QLineEdit()
        line_edit4 = QLineEdit()
        btnRun = QPushButton("Run")
        layout.addWidget(lbl_count, 0, 1)
        layout.addWidget(line_count, 1, 1)
        line_count.setText("10")
        layout.addWidget(label1, 4, 0)
        layout.addWidget(line_edit1, 4, 1)
        line_edit1.setText("elonmusk")
        layout.addWidget(lblBearer, 5, 0)
        layout.addWidget(line_edit3, 5, 1)
        layout.addWidget(label2, 6, 0)
        layout.addWidget(line_edit2, 6, 1)
        layout.addWidget(label4, 7, 0)
        layout.addWidget(line_edit4, 7, 1)
        layout.addWidget(btnRun, 8, 1)
        
        #data displayer
        small_editor = QTextEdit()
        small_editor.setPlainText("The results will be displayed here")
        layout.addWidget(small_editor, 0, 2, 8, 1)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self.setLayout(layout)
        self.show()
        line_count.textChanged.connect(lambda: save_count(line_count.text()))
        btnRun.clicked.connect(lambda: run_script(line_edit1.text(),line_edit2.text(),line_edit3.text(),line_edit4.text()))

        #the basic function to run the api scripts, where the received args are parsed into
        #the right requests and then returned as a dict, which gets turned into json!
        def run_script(user, secret, bearer, token):
            if (user == "") or (bearer == ""):
                small_editor.setPlainText("some of the fields werent filled")
                print("some of the fields werent filled ,redo")

            elif (state == 0):
                small_editor.setPlainText("no mode selected!")
                print("no mode selected")

            else:
                print(state, tweet_count, user, secret, bearer, token)
                x = f"{state}/{tweet_count}/{user}/{secret}/{bearer}/{token}"
                dict_response = receivers.api_script(state, tweet_count, user, secret, bearer, token)
                json_response = json.dumps(dict_response, indent = 4)
                small_editor.setPlainText(json_response)
            
        #active switching of the mode from the buttons, default 1 = usertweetlookup
        def mode_switch(s):
            global state
            state = s
            print(f"current state: {state}")

        #same as above but for the textfield where the amount of tweets is specified
        def save_count(s):
            global tweet_count
            print(f"count entered: {s}")
            if int(s) <= 5:
                small_editor.setPlainText("numbers below 5 will get increased to 5 due to api limitations!")
                s = 5
            tweet_count = s
            print(f"count of tweets: {tweet_count}")
            
    #test = line_edit1.text()
    #print(test) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec())