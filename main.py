import os
import sys

# Get the absolute path of the current script file

script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QSplitter, QSizePolicy, QSpacerItem, QHBoxLayout, QPushButton, \
    QLineEdit, QTableWidgetItem
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from scrollArea import ScrollArea
from addDelListWidget import AddDelListWidget
from apiWidget import ApiWidget
from script import GPTJsonWrapper

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    generatedFinished = pyqtSignal(dict)

    def __init__(self, wrapper):
        super(Thread, self).__init__()
        self.__wrapper = wrapper

    def run(self):
        try:
            self.generatedFinished.emit(self.__wrapper.get_data())
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__wrapper = GPTJsonWrapper()

    def __initUi(self):
        self.setWindowTitle('PyQt GPT JSON response example with QTableWidget')

        apiWidget = ApiWidget()

        topicLbl = QLabel('Topic')
        self.__topicLineEdit = QLineEdit()
        self.__topicLineEdit.setText('Games')

        lay = QHBoxLayout()
        lay.addWidget(topicLbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(self.__topicLineEdit)
        lay.setContentsMargins(0, 0, 0, 0)

        topicWidget = QWidget()
        topicWidget.setLayout(lay)

        rowWidget = AddDelListWidget('Items')

        self.__rowListWidget = rowWidget.getListWidget()
        self.__rowListWidget.addItems(['Dark Souls', 'Minecraft', 'Metal Slug 2', 'Tekken 3'])

        lay = QVBoxLayout()
        lay.addWidget(topicWidget)
        lay.addWidget(rowWidget)
        lay.setContentsMargins(0, 0, 2, 0)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        self.__scrollArea = ScrollArea()

        lay = QVBoxLayout()
        lay.addWidget(QLabel('Result'))
        lay.addWidget(self.__scrollArea)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        self.__splitter = QSplitter()
        self.__splitter.addWidget(leftWidget)
        self.__splitter.addWidget(rightWidget)
        self.__splitter.setHandleWidth(1)
        self.__splitter.setChildrenCollapsible(False)
        self.__splitter.setSizes([500, 500])
        self.__splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")

        self.__runBtn = QPushButton('Run')
        self.__runBtn.clicked.connect(self.__run)

        self.__splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(apiWidget)
        lay.addWidget(self.__splitter)
        lay.addWidget(self.__runBtn)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        apiWidget.aiEnabled.connect(self.__aiEnabled)

        f = apiWidget.isAiEnabled()
        self.__splitter.setEnabled(f)
        if f:
            self.__wrapper.set_api(apiWidget.getApiKey())

    def __aiEnabled(self, f, api_key):
        self.__splitter.setEnabled(f)
        if f:
            self.__wrapper = GPTJsonWrapper(api_key=api_key)
        else:
            self.__wrapper = GPTJsonWrapper(api_key=api_key)
        self.__wrapper.set_api(api_key)

    def __run(self):
        topic = self.__topicLineEdit.text().strip()
        rows = [self.__rowListWidget.item(i).text() for i in range(self.__rowListWidget.count())]

        self.__wrapper.set_topic(topic)
        self.__wrapper.set_rows(rows)

        self.__t = Thread(self.__wrapper)
        self.__t.started.connect(self.__started)
        self.__t.finished.connect(self.__finished)
        self.__t.generatedFinished.connect(self.__generatedFinished)
        self.__t.start()

    def __started(self):
        self.__scrollArea.remove_widgets()
        self.__runBtn.setEnabled(False)

    def __finished(self):
        self.__runBtn.setEnabled(True)

    def __generatedFinished(self, result: dict):
        self.__scrollArea.set_widgets(result)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())