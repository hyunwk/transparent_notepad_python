import sys
from PyQt5.Qt import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import pyautogui
import datetime

from oracleDB import sub_list

form_class = uic.loadUiType("C:\\Users\\ab845\\OneDrive - 인하공업전문대학\\20-2\\SW프로젝트\\PyQT\\SW프로젝트\\notepad.ui")[0]

class findWindow(QDialog):
    def __init__(self, parent):  # parent로 종속적으로 만듬.ex) parent가 꺼지면 같이 꺼지도록
        super(findWindow, self).__init__(parent)
        uic.loadUi("C:\\Users\\ab845\\OneDrive - 인하공업전문대학\\20-2\\SW프로젝트\\PyQT\\SW프로젝트\\find.ui", self)
        self.show()

        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit
        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancel.clicked.connect(self.close)

    def findNext(self):
        print('find')
        self.setCursor(9, 12)

        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        print(pattern, text)

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

class selectSubject(QDialog):
    def __init__(self):
        super(selectSubject, self).__init__()
        uic.loadUi("C:\\Users\\ab845\\OneDrive - 인하공업전문대학\\20-2\\SW프로젝트\\PyQT\\SW프로젝트\\selectSubject.ui", self)
        self.setWindowTitle("과목 선택")
        self.show()
        for i in sub_list:
            self.list_subject.addItem(str(i))
            print(i)
        # list_subject
        self.list_subject.itemDoubleClicked.connect(self.itemDoubleClicked)
        # list_week
        self.list_week.itemDoubleClicked.connect(self.itemDoubleClicked)
        # 버튼에 기능 연결
        self.btn_add.clicked.connect(self.addListWidget)

    def itemDoubleClicked(self):
        try :
            #과목 & week 둘다 선택 시
            if(len(self.list_subject.currentItem().text()) & len(self.list_week.currentItem().text())):
                self.sub_name = self.list_subject.currentItem().text()
                self.sub_week = self.list_week.currentItem().text()

                selectSubject.close(self)

        except Exception as ex:  # 에러 종류
            print('에러가 발생 했습니다', ex)

    # 항목을 추가, 삽입하는 함수들
    def addListWidget(self):
        self.addItemText = self.txt_addItem.text()
        self.list_subject.addItem(self.addItemText)
        self.txt_addItem.setText("")

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_open.triggered.connect(self.openFunction)
        self.action_save.triggered.connect(self.saveFunction)
        self.action_saveas.triggered.connect(self.saveAsFunction)
        self.action_close.triggered.connect(self.close)

        self.action_undo.triggered.connect(self.undoFunction)
        self.action_cut.triggered.connect(self.cutFunction)
        self.action_copy.triggered.connect(self.copyFunction)
        self.action_paste.triggered.connect(self.pasteFunction)

        self.action_find.triggered.connect(self.findFunction)

        self.slider.valueChanged.connect(self.changeFunction)
        self.action_set_top_level.triggered.connect(self.setWindowTop)
        self.action_unset_top_level.triggered.connect(self.unsetWindowTop)
        self.action_hide.triggered.connect(self.hideFunction)
        self.action_unhide.triggered.connect(self.unhideFunction)
        self.action_capture.triggered.connect(self.captureFunction)

        #시작시 과목 선택
        select = selectSubject()
        select.exec_()

        self.opened = False
        self.opened_file_path = '제목 없음'
        self.capture_cnt = 0

        self.setMouseTracking(True)

    def ischanged(self):
        # 열린 적 없을 시
        if not self.opened:
            print('not changed')
            if self.plainTextEdit.toPlainText().strip():  # 열린적은 없는데 에디터 내용이 있으면
                return True
            return False

        # 열린 적 있을 시
        current_data = self.plainTextEdit.toPlainText()  # 현재 데이터

        with open(self.opened_file_path, encoding='UTF8') as f:  # 파일에 저장된 데이터
            file_data = f.read()

        if current_data == file_data:  # 열린적이 있고 변경사항이 없으면
            return False
        else:  # 열린적이 있고 변경사항이 있으면
            return True

    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('저장')
        msgBox.setText("변경 내용을 {}에 저장하시겠습니까?".format(self.opened_file_path))
        msgBox.addButton('저장', QMessageBox.YesRole)  # 0
        msgBox.addButton('저장 안 함', QMessageBox.NoRole)  # 1
        msgBox.addButton('취소', QMessageBox.RejectRole)  # 2

        # 최상단 고정
        msgBox.setWindowFlags(Qt.WindowStaysOnTopHint)
        msgBox.show()

        # 버튼 클릭 결과
        ret = msgBox.exec_()
        if ret == 0:
            self.saveFunction()
        else:
            return ret

    def closeEvent(self, event):
        if self.ischanged():  # 열린적이 있고 변경사항이 있으면 열린적은 없는데 에디터 내용이 있으면
            ret = self.save_changed_data()

            if ret == 2:
                event.ignore()

    def save_file(self, fname):
        data = self.plainTextEdit.toPlainText()

        with open(fname, 'w', encoding='UTF8') as f:
            f.write(data)

        self.opened = True
        self.opened_file_path = fname

        print("save {}!!".format(fname))

    def open_file(self, fname):
        with open(fname, encoding='UTF8') as f:
            data = f.read()

        self.plainTextEdit.setPlainText(data)

        self.opened = True
        self.opened_file_path = fname

        print("open {}!!".format(fname))

    def openFunction(self):
        if self.ischanged():  # 열린적이 있고 변경사항이 있으면 열린적은 없는데 에디터 내용이 있으면
            ret = self.save_changed_data()

        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            self.open_file(fname[0])

    def saveFunction(self):
        if self.opened:
            self.save_file(self.opened_file_path)
        else:
            self.saveAsFunction()

    def saveAsFunction(self):
        fname = QFileDialog.getSaveFileName(self)
        if fname[0]:
            self.save_file(fname[0])

    def undoFunction(self):
        self.plainTextEdit.undo()

    def cutFunction(self):
        self.plainTextEdit.cut()

    def copyFunction(self):
        self.plainTextEdit.copy()

    def pasteFunction(self):
        self.plainTextEdit.paste()

    def findFunction(self):
        findWindow(self)

    def changeFunction(self):
        opacity_value = self.slider.value() * 0.01
        self.setWindowOpacity(opacity_value)

    def setWindowTop(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def unsetWindowTop(self):
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.show()

    def hideFunction(self):
        self.hide()

    def unhideFunction(self):
        # 수정 필요
        self.show()

    def captureFunction(self):

        self.tempNow = datetime.datetime.now()
        self.now = self.tempNow.strftime('%m-%d-%H-%M-%S')
        #firstMouseX, firstMouseY = pyautogui.position()
        #lastMouseX, lastMouseY = pyautogui.position()

        pyautogui.screenshot('D:/{}.png'.format(self.now), region=(500, 100, 1000, 700))
        print("캡쳐 완료")

    #DB 연동 - 과목 - 1주차,2주차 이런식으로
    # BUT 과목 선택 시 모든 주차 오픈 및 이어붙이기
    # 사진은 어떻게??

app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()