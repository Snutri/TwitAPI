from multiprocessing.pool import ThreadPool
import sys
from time import sleep
import receivers
import json
import pandas as pd
import threading
import traceback
import datetime
from PySide6 import QtCore
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt, Signal, Slot, QAbstractTableModel, QRunnable, QThreadPool, QObject
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView)
state = 0
tweet_count = 10
active_status = True
# datawindow is the pop up window that is used to display a users data


class DataWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        layout = QGridLayout()
        width = 1200
        height = 700
        self.label_sort = QLabel("Sorting by:")
        self.btnTime = QPushButton("Sort by date")
        self.btnRetweets = QPushButton("Sort by retweets")
        self.btnLikes = QPushButton("Sort by likes")
        self.btnQuotes = QPushButton("Sort by quote retweets")
        self.btnID = QPushButton("Sort by tweet ID")
        self.btnReplies = QPushButton("Sort by replies")
        self.table = QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        layout.addWidget(self.btnTime, 2, 0)
        layout.addWidget(self.btnRetweets, 3, 0)
        layout.addWidget(self.btnLikes, 4, 0)
        layout.addWidget(self.btnQuotes, 5, 0)
        layout.addWidget(self.btnID, 6, 0)
        layout.addWidget(self.table, 2, 8, 6, 8)
        self.btnTime.clicked.connect(lambda: sort_by_input(self, 1, data))
        self.btnRetweets.clicked.connect(lambda: sort_by_input(self, 2, data))
        self.btnLikes.clicked.connect(lambda: sort_by_input(self, 3, data))
        self.btnQuotes.clicked.connect(lambda: sort_by_input(self, 4, data))
        self.btnID.clicked.connect(lambda: sort_by_input(self, 5, data))
        self.btnReplies.clicked.connect(lambda: sort_by_input(self, 6, data))
        self.setMinimumSize(width, height)
        self.setLayout(layout)

# data sorter for the dataframe, easily expandable based on input


def sort_by_input(self, input, data):
    match input:
        case 1:
            data.sort_values(by=['created_at'], ascending=False,
                             inplace=True, ignore_index=True)
            self.update()
            self.model.layoutChanged.emit()
            return
        case 2:
            data.sort_values(by=['retweets'], ascending=False,
                             inplace=True, ignore_index=True)
            # print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return
        case 3:
            data.sort_values(by=['likes'], ascending=False,
                             inplace=True, ignore_index=True)
            # print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return
        case 4:
            data.sort_values(by=['quotes'], ascending=False,
                             inplace=True, ignore_index=True)
            # print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return
        case 5:
            data.sort_values(by=['id'], ascending=False,
                             inplace=True, ignore_index=True)
            # print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return
        case 6:
            data.sort_values(by=['replies'], ascending=False,
                             inplace=True, ignore_index=True)
            # print(data.retweets.to_string(index=False))
            self.update()
            self.model.layoutChanged.emit()
            return
    return

# base for the table model that hosts the data passed, called by datawindow


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
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
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())
        width = 280
        height = 400
        self.setWindowTitle("TwitAPI")
        self.setMinimumSize(width, height)
        layout = QGridLayout()
        self.w = DataWindow
        onlyInt = QIntValidator()
        # choose mode buttons
        btnFetch = QPushButton("Fetch tweets")
        btnFetch.clicked.connect(lambda: mode_switch(1))
        btnLikes = QPushButton("Fetch images")
        btnLikes.clicked.connect(lambda: mode_switch(2))
        btnTime = QPushButton("Fetch timeline")
        btnTime.clicked.connect(lambda: mode_switch(3))
        btnData = QPushButton("open data window")
        btnData.clicked.connect(
            lambda: show_new_window(self, line_user))
        line_user = QLineEdit()
        layout.addWidget(btnFetch, 0, 0)
        layout.addWidget(btnLikes, 1, 0)
        layout.addWidget(btnTime, 2, 0)
        layout.addWidget(btnData, 3, 0)
        layout.addWidget(line_user, 3, 1)
        line_user.setPlaceholderText("username to open data from")
        # data input code
        lbl_count = QLabel("number of tweets to fetch:")
        label1 = QLabel("User name to fetch:")
        lblBearer = QLabel("Bearer:")
        line_count = QLineEdit()
        line_edit1 = QLineEdit()
        line_edit2 = QLineEdit()
        line_bearer = QLineEdit()
        line_bearer.setPlaceholderText("Set your bearer here")
        line_edit4 = QLineEdit()

        btnRun = QPushButton("Run")
        btnClear = QPushButton("Clear log")
        layout.addWidget(lbl_count, 0, 1)
        layout.addWidget(line_count, 1, 1)
        line_count.setText("5")
        line_count.setValidator(onlyInt)
        layout.addWidget(label1, 4, 0)
        layout.addWidget(line_edit1, 4, 1)
        # default user for the fetch
        line_edit1.setText("")
        layout.addWidget(lblBearer, 5, 0)
        line_bearer.setText("")
        layout.addWidget(line_bearer, 5, 1)
        layout.addWidget(btnRun, 8, 1)
        layout.addWidget(btnClear, 8, 0)
        small_editor = QTextEdit()
        small_editor.setPlainText("The results will be displayed here")
        layout.addWidget(small_editor, 10, 0, 3, 3)
        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 10)
        layout.setColumnStretch(3, 20)
        layout.setColumnStretch(4, 20)

        # takes the elements and sets/shows
        self.setLayout(layout)
        self.show()
        print(active_status)

        line_count.textChanged.connect(
            lambda: save_count(line_count.text()))

        btnRun.clicked.connect(lambda: thread_starter(self, line_edit1.text(),
                                                              line_edit2.text(), line_bearer.text(),
                                                              line_edit4.text()))

        # clears the text of the small editor
        btnClear.clicked.connect(lambda: small_editor.setPlainText(""))


        def mode_switch(s):
            global state
            state = s
            print(f"current state: {state}")

        # catches tweet fetch below a certain point and turns it to minimum value
        def save_count(s):
            global tweet_count
            print(f"count entered: {s}")
            if int(s) <= 9:
                small_editor.setPlainText(
                    "numbers below 10 will get increased to 10 due to api limitations!")
                s = 10
            tweet_count = s

        def update_textbox(text):
            small_editor.append(text)
            small_editor.update()

        # the basic function to run the api scripts, where the received args are parsed into
        # the right requests and then returned as a dict, which gets turned into json!
        def thread_starter(self, user, secret, bearer, token):
            worker = Worker(run_script, self, user,
                            secret, bearer, token)
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)
            self.threadpool.start(worker)


    # basis of running the api scripts, checks for faults in args given
        def run_script(self, user, secret, bearer, token, p_call, r_call):
            global active_status
            if (user == "") or (bearer == ""):
                self.small_editor.append("some of the fields werent filled")
                print("some of the fields werent filled ,redo")
            # notfies of the missing mode selection
            elif (state == 0):
                update_textbox(self, "no mode selected!")
                print("no mode selected")
            else:
                # passes the args to the receivers,
                # albeit some of it is just placeholder and could
                # be done by passing the args in a simple way

                receivers.api_script(state, tweet_count, user,
                                     secret, bearer, token, p_call, r_call)


    # opens data window with specified persons tweets
        def show_new_window(self, line_user):
            try:
                with open(f'{line_user.text()}-TimeLine.json', encoding="utf-8") as file:
                    datax = json.load(file)
                    list(datax)
                    # points to the data part of the json,
                    # due to the multiple array json twitter uses
                    df_nested_list = pd.json_normalize(datax, record_path=['data'])
                    list(df_nested_list)
                    # handily renaming the variables given, as they are nested and
                    # would display parent names
                    df_nested_list.rename(columns={
                        "public_metrics.retweet_count": "retweets",
                        "public_metrics.reply_count": "replies",
                        "public_metrics.like_count": "likes",
                        "public_metrics.quote_count": "quotes",
                        "attachments.media_keys": "media"}, inplace=True)
                    self.w = DataWindow(df_nested_list)
                    self.w.show()
                    print("opening window!")
            except FileNotFoundError:
                MainWindow.small_editor.append(
                    "No user was specified or the name had a typo")
    
    
    
    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)
        MainWindow.update_textbox(s)

    def thread_complete(self):
        thread_identity = threading.get_ident()
        print(f"Thread [{thread_identity}] closing")
    


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        self.kwargs['r_call'] = self.signals.result
        self.kwargs['p_call'] = self.signals.progress

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec())
