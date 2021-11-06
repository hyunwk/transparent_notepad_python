import sys
from PyQt5.Qt import *
from PyQt5 import Qt, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import pyautogui
from datetime import datetime
import oracleDB as db
from find import findWindow

# notepad 기본, ui 참조 : https://onedrive.live.com/?cid=eb4f2a403d81809b&id=EB4F2A403D81809B%21201640&authkey=!AGYeXcxeLR6zXQU

form_class = uic.loadUiType("notepad.ui")[0]

now = datetime.now()
temp = now.strftime('%Y-%m-%d %H:%M:%S')
sub_date = temp

class selectSubject(QDialog):
    sub_name = ""
    sub_week = 0
    sub_content = ""

    def __init__(self):
        super(selectSubject, self).__init__()
        uic.loadUi("selectSubject.ui", self)
        self.setWindowTitle("과목 선택")
        self.show()

        sub_list = db.get_subject()

        #과목 list에 저장
        for i in sub_list:
            self.list_subject.addItem(str(i))

        # list_subject
        self.list_subject.itemDoubleClicked.connect(self.itemDoubleClicked)
        # list_week
        self.list_week.itemDoubleClicked.connect(self.itemDoubleClicked)
        # 버튼에 기능 연결
        self.btn_add.clicked.connect(self.addListWidget)

    def itemDoubleClicked(self):
        try:
            # 과목 & week 둘다 선택 시
            if (len(self.list_subject.currentItem().text()) > 0):
                if (int(self.list_week.currentItem().text()) > 0):
                    selectSubject.sub_name = str(self.list_subject.currentItem().text())
                    selectSubject.sub_week = int(self.list_week.currentItem().text())

                    selectSubject.close(self)

        except Exception as ex:  # 에러 종류
            print('에러가 발생 했습니다', ex)

    # 과목 추가
    def addListWidget(self):
        self.sub_name = self.txt_addItem.text()
        self.list_subject.addItem(self.sub_name)
        self.txt_addItem.setText("")

class Font(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 font dialog - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Open PyQt5 Font Dialog', self)
        button.setToolTip('font dialog')
        button.move(50, 50)

        self.show()

    def openFontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            return font

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_save.triggered.connect(self.save_file)
        self.action_close.triggered.connect(self.close)

        self.action_undo.triggered.connect(self.undoFunction)
        self.action_cut.triggered.connect(self.cutFunction)
        self.action_copy.triggered.connect(self.copyFunction)
        self.action_paste.triggered.connect(self.pasteFunction)
        self.action_find.triggered.connect(self.findFunction)
        self.action_set_font.triggered.connect(self.fontFunction)

        self.slider.valueChanged.connect(self.changeFunction)
        self.action_set_top_level.triggered.connect(self.setWindowTop)
        self.action_unset_top_level.triggered.connect(self.unsetWindowTop)
        self.action_hide_frame.triggered.connect(self.hideFunction)
        self.action_capture.triggered.connect(self.captureFunction)

        data = self.textEdit.createMimeDataFromSelection()
        self.textEdit.canInsertFromMimeData(data)
        # 시작시 과목 선택
        select = selectSubject()
        select.exec_()

        # 내용 불러오기
        content = db.get_content(selectSubject.sub_name, selectSubject.sub_week, sub_date)
        self.setWindowTitle("과목 : " + selectSubject.sub_name)
        self.textEdit.setText(content)

        self.opened = False

        self.capture_cnt = 0

        self.setMouseTracking(True)

        self.saved = False

    #font 설정
    def fontFunction(self):
        try:
            font_info = Font.openFontDialog(self)
            self.textEdit.setFont(font_info)
        except Exception as ex:
            print("에러가 발생했습니다. :", ex)

    # 변경된 데이터 저장
    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('저장')
        msgBox.setText("변경 내용을  저장하시겠습니까?")
        msgBox.addButton('저장', QMessageBox.YesRole)  # 0
        msgBox.addButton('저장 안 함', QMessageBox.NoRole)  # 1
        msgBox.addButton('취소', QMessageBox.RejectRole)  # 2

        # 최상단 고정
        # msgBox.setWindowFlags(Qt.WindowStaysOnTopHint)
        msgBox.show()

        # 버튼 클릭 결과
        ret = msgBox.exec_()
        if ret == 0:
            self.save_file()
        else:
            return ret

    #x 버튼 클릭 or 끝내기 메뉴 클릭 시
    def closeEvent(self, event):
        if not self.saved:
            ret = self.save_changed_data()

        self.saved=False;

        if ret == 2:
            event.ignore()

        #pyqt 종료 코드 필요
        QCoreApplication.instance().quit

    def save_file(self):
        #과목선택시 선택한 정보
        sub_name = selectSubject.sub_name
        sub_week = selectSubject.sub_week

        data = self.textEdit.toPlainText()
        data=data.ljust(10)

        # 새로운 내용 insert
        content_start = data.find(sub_date) + len(sub_date) + 1
        sub_content = data[content_start:]

        # 존재하는 내용 update
        if db.content_exists:
            content_end = sub_content.find('===================')
            sub_content = sub_content[:content_end]

        # oracle db에 저장
        tup = (sub_name, sub_week, sub_date, sub_content)
        db.add_content(tup)

        self.saved = True

    def undoFunction(self):
        self.textEdit.undo()

    def cutFunction(self):
        self.textEdit.cut()
    
    def copyFunction(self):
        self.textEdit.copy()

    def pasteFunction(self):
        self.textEdit.paste()

    def findFunction(self):
        findWindow(self)

    def changeFunction(self):
        opacity_value = self.slider.value() * 0.01
        self.setWindowOpacity(opacity_value)

    def setWindowTop(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def unsetWindowTop(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
        self.show()

    def hideFunction(self):
        self.showMinimized()

    def captureFunction(self):
        self.tempNow = datetime.datetime.now()
        self.now = self.tempNow.strftime('%m-%d-%H-%M-%S')

        pyautogui.screenshot('D:/{}.png'.format(self.now), region=(500, 100, 1000, 700))
        print("캡쳐 완료")

app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()