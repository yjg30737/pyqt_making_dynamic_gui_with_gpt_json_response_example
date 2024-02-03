from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QScrollArea, QWidget, QLabel, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt

class ScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent)
        self.__initUi()

    def __initUi(self):
        lay = QVBoxLayout()
        lay.setAlignment(Qt.AlignTop)
        self.__widget = QWidget()
        self.__widget.setLayout(lay)
        self.setWidget(self.__widget)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

    def set_widgets(self, descriptions: dict):
        lay = self.__widget.layout()
        descriptions = descriptions.get('Description', '')
        if descriptions:
            for key, value in descriptions.items():
                title_lbl = QLabel(key)
                title_lbl.setFont(QFont('Arial', 14, QFont.Bold))
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setFrameShadow(QFrame.Sunken)
                description_lbl = QLabel(str(value))
                lay.addWidget(title_lbl)
                lay.addWidget(description_lbl)
                lay.addWidget(sep)

    def remove_widgets(self):
        lay = self.__widget.layout()
        if lay:
            for i in range(lay.count()-1, -1, -1):
                lay.itemAt(i).widget().deleteLater()


