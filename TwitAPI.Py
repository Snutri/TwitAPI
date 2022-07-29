import sys
import receivers
import json
import pandas as pd
from tokenize import String
from collections.abc import MutableMapping
from flatdict import FlatDict

from functools import partial
from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal, Slot, QAbstractTableModel
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView)
state = 0
tweet_count = 10
class DataWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        layout = QGridLayout()
        width = 1200
        height = 700

        self.label_sort = QLabel("Sorting by:")
        self.btnTime = QPushButton(f"Sort by date")
        self.btnRetweets = QPushButton(f"Sort by retweets")
        self.btnLikes = QPushButton(f"Sort by likes")
        self.btnQuotes = QPushButton(f"Sort by quote retweets")
        self.btnID = QPushButton(f"Sort by tweet ID")
        self.btnReplies = QPushButton(f"Sort by replies")

        self.table = QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        #layout.addWidget(self.label_sort, 1, 0)
        layout.addWidget(self.btnTime, 2, 0)
        layout.addWidget(self.btnRetweets, 3, 0)
        layout.addWidget(self.btnLikes, 4, 0)
        layout.addWidget(self.btnQuotes, 5, 0)
        layout.addWidget(self.btnID, 6, 0)

        layout.addWidget(self.table, 2, 8, 6 ,8)
        self.btnTime.clicked.connect(lambda: sortbyinput(self, 1, data))
        self.btnRetweets.clicked.connect(lambda: sortbyinput(self, 2, data))
        self.btnLikes.clicked.connect(lambda: sortbyinput(self, 3, data))
        self.btnQuotes.clicked.connect(lambda: sortbyinput(self, 4, data))
        self.btnID.clicked.connect(lambda: sortbyinput(self, 5, data))
        self.btnReplies.clicked.connect(lambda: sortbyinput(self, 6, data))
        self.setMinimumSize(width, height)
        self.setLayout(layout)
        

def sortbyinput(self, input, data):
    match input:
        case 1:
            data.sort_values(by=['created_at'], ascending=False, inplace=True, ignore_index=True)
            self.update()
            self.model.layoutChanged.emit()
            return 
        case 2:
            data.sort_values(by=['retweets'], ascending=False, inplace=True, ignore_index=True)
            #print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return
        case 3:
            data.sort_values(by=['likes'], ascending=False, inplace=True, ignore_index=True)
            #print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return 
        case 4:
            data.sort_values(by=['quotes'], ascending=False, inplace=True, ignore_index=True)
            #print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return 
        case 5:
            data.sort_values(by=['id'], ascending=False, inplace=True, ignore_index=True)
            #print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return 
        case 6:
            data.sort_values(by=['replies'], ascending=False, inplace=True, ignore_index=True)
            #print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return 
    return


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class MainWindow(QWidget):

    num_grid_rows = 3
    def __init__(self):
        super().__init__()
        width = 720
        height = 400
        self.setWindowTitle("TwitAPI")
        self.setMinimumSize(width, height)
        layout = QGridLayout()
        self.w = DataWindow
        #choose mode buttons
        btnFetch = QPushButton(f"Fetch tweets")
        btnFetch.clicked.connect(lambda: mode_switch(1))
        btnLikes = QPushButton(f"Fetch likes")
        btnLikes.clicked.connect(lambda: mode_switch(2))
        btnTime = QPushButton(f"Fetch timeline")
        btnTime.clicked.connect(lambda: mode_switch(3))
        btnData = QPushButton(f"open data window")
        btnData.clicked.connect(lambda: show_new_window(self))
        line_user = QLineEdit()
        layout.addWidget(btnFetch, 0, 0)
        layout.addWidget(btnLikes, 1, 0)
        layout.addWidget(btnTime, 2, 0)
        layout.addWidget(btnData, 3, 0)
        layout.addWidget(line_user, 3, 1)
        line_user.setPlaceholderText("username to open data from") 
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
        line_bearer = QLineEdit()
        line_bearer.setPlaceholderText("Set your bearer here")
        line_edit4 = QLineEdit()
        
        btnRun = QPushButton("Run")
        layout.addWidget(lbl_count, 0, 1)
        layout.addWidget(line_count, 1, 1)
        line_count.setText("5")
        layout.addWidget(label1, 4, 0)
        layout.addWidget(line_edit1, 4, 1)
        line_edit1.setText("elonmusk")
        layout.addWidget(lblBearer, 5, 0)
        line_bearer.setText("")
        layout.addWidget(line_bearer, 5, 1)
        layout.addWidget(label2, 6, 0)
        layout.addWidget(line_edit2, 6, 1)
        layout.addWidget(label4, 7, 0)
        layout.addWidget(line_edit4, 7, 1)
        layout.addWidget(btnRun, 8, 1)
        
        #data displayer
        small_editor = QTextEdit()
        small_editor.setPlainText("The results will be displayed here")
        layout.addWidget(small_editor, 10, 0, 3, 3)
        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)

        self.setLayout(layout)
        self.show()

        ############################################
        data = []
        #DataWindow(data)
        
        ############################################
        line_count.textChanged.connect(lambda: save_count(line_count.text()))
        btnRun.clicked.connect(lambda: run_script(line_edit1.text(),line_edit2.text(),line_bearer.text(),line_edit4.text()))
        TweetList = []
        #dataframe()
        #try:
        #    print(f'{line_user.text()}-TimeLine.json')
        #    datax = json.load(open(f'elonmusk-TimeLine.json'))
        #    list(datax)
        #    df_nested_list = pd.json_normalize(datax, record_path =['data'])
        #    list(df_nested_list)
        #    #print(df_nested_list)
        #    df_nested_list.rename(columns = {"public_metrics.retweet_count":"retweets", "public_metrics.reply_count":"replies", "public_metrics.like_count":"likes", "public_metrics.quote_count":"quotes", "attachments.media_keys":"media"}, inplace = True)
        #    self.w = DataWindow(df_nested_list)
        #except:
        #    print("data was unavailable")
        
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
                #print(state, tweet_count, user, secret, bearer, token)
                x = f"{state}/{tweet_count}/{user}/{secret}/{bearer}/{token}"
                dict_response = receivers.api_script(state, tweet_count, user, secret, bearer, token)
                #dictToCsv(dict_response)
                json_response = json.dumps(dict_response, indent = 4)
                #DataWindow(data)
                #small_editor.setPlainText(json_response)
                #output = flatten(dict_response)
                #json.dumps(output)
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
            if int(s) <= 9:
                small_editor.setPlainText("numbers below 10 will get increased to 10 due to api limitations!")
                s = 10
            tweet_count = s
            print(f"count of tweets: {tweet_count}")

        #opens data window with specified persons tweets w
        def show_new_window(self):
            datax = json.load(open(f'{line_user.text()}-TimeLine.json'))
            list(datax)
            df_nested_list = pd.json_normalize(datax, record_path =['data'])
            list(df_nested_list)
            #print(df_nested_list)
            df_nested_list.rename(columns = {"public_metrics.retweet_count":"retweets", "public_metrics.reply_count":"replies", "public_metrics.like_count":"likes", "public_metrics.quote_count":"quotes", "attachments.media_keys":"media"}, inplace = True)
            self.w = DataWindow(df_nested_list)
            self.w.show()
            print("opening window!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec())