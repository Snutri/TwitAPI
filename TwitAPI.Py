import sys
import receivers
import json
from tokenize import String

from functools import partial
from PySide6.QtCore import Qt, Signal, Slot, QAbstractTableModel
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView)

state = 0
tweet_count = 10
class DataWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, data):
        super().__init__()
        self.data = data
        layout = QGridLayout()
        width = 720
        height = 360

        self.label = QLabel("Another Window")
        layout.addWidget(self.label)

        self.table = QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        layout.addWidget(self.table, 0, 1, 8 ,3)

        self.move(20, 50)
        self.setMinimumSize(width, height)
        self.setLayout(layout)


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

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
        btnData = QPushButton(f"open data window")
        layout.addWidget(btnFetch, 0, 0)
        layout.addWidget(btnLikes, 1, 0)
        layout.addWidget(btnTime, 2, 0)
        layout.addWidget(btnData, 3, 0)
        btnFetch.clicked.connect(lambda: mode_switch(1))
        btnLikes.clicked.connect(lambda: mode_switch(2))
        btnTime.clicked.connect(lambda: mode_switch(3))
        btnData.clicked.connect(lambda: show_new_window(self))
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

        ############################################
        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]
        #DataWindow(data)
        self.w = DataWindow(data)
        ############################################
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

        def show_new_window(self):
            print("opening window!")
            if self.w.isVisible():
                self.w.hide()

            else:
                self.w.show()

        
        
    #test = line_edit1.text()
    #print(test) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec())