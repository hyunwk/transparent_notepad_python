from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore

class findWindow(QDialog):
    def __init__(self, parent):  # parent로 종속적으로 만듬.ex) parent가 꺼지면 같이 꺼지도록
        super(findWindow, self).__init__(parent)
        uic.loadUi("C:\\Users\\ab845\\OneDrive - 인하공업전문대학\\swproject-notepad\\SW프로젝트\\find.ui", self)
        self.show()
        try:
            self.parent = parent
            self.cursor = parent.plainTextEdit.textCursor()
            self.pe = parent.plainTextEdit

            self.pushButton_findnext.clicked.connect(self.findNext)
            self.pushButton_cancel.clicked.connect(self.close)

            self.radioButton_down.clicked.connect(self.updown_radio_button)
            self.radioButton_up.clicked.connect(self.updown_radio_button)
            self.up_down = "down"
        except Exception as ex:  # 에러 종류
            print('에러가 발생 했습니다', ex)

    def updown_radio_button(self):
        if self.radioButton_up.isChecked():
            self.up_down = "up"
        elif self.radioButton_down.isChecked():
            self.up_down = "down"

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSenesitive.isChecked():
            cs = QtCore.Qt.CaseSensitive  # 민감하다.
        else:
            cs = QtCore.Qt.CaseInsensitive  # 민감하지 않다.

        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()

        if self.up_down == "down":
            index = reg.indexIn(text, pos)  # 검색 하기!
        else:
            pos -= len(pattern) + 1
            index = reg.lastIndexIn(text, pos)
        print(index, pos)

        if (index != -1) and (pos > -1):  # 검색된 결과가 있다면...
            self.setCursor(index, len(pattern) + index)
        else:
            self.notFoundMsg(pattern)

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def setCursor(self, start, end):
        print(self.cursor.selectionStart(), self.cursor.selectionEnd())
        self.cursor.setPosition(start)  # 앞에 커서 찍고
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)  # 뒤로 커서를 움직인다
        self.pe.setTextCursor(self.cursor)
        print()

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('메모장')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton('확인', QMessageBox.YesRole)
        ret = msgBox.exec_()