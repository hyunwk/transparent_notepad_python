import sys
from PyQt5.Qt import *
from PyQt5 import uic
from PyQt5 import *
from PyQt5.QtWidgets import QApplication
import pyautogui
from datetime import datetime
from oracleDB import *
from find import findWindow
from record_audio import record


# notepad 기본, ui 참조 : https://onedrive.live.com/?cid=eb4f2a403d81809b&id=EB4F2A403D81809B%21201640&authkey=!AGYeXcxeLR6zXQU
form_class = uic.loadUiType("C:\\Users\\ab845\\OneDrive - 인하공업전문대학\\swproject-notepad\\SW프로젝트\\notepad.ui")[0]

class selectSubject(QDialog):
    sub_name = ""
    now = datetime.now()
    sub_week = 0
    sub_date = now.strftime('%Y-%m-%d %H:%M:%S')
    sub_content = ""
    sub_image=""

    def __init__(self):
        super(selectSubject, self).__init__()
        uic.loadUi("C:\\Users\\ab845\\OneDrive - 인하공업전문대학\\swproject-notepad\\SW프로젝트\\selectSubject.ui", self)
        self.setWindowTitle("과목 선택")
        self.show()

        #db에서 subject 불러온 후 리스트에 저장
        sub_list = get_subject()
        for i in sub_list:
            self.list_subject.addItem(str(i))

        # list_subject
        self.list_subject.itemDoubleClicked.connect(self.itemDoubleClicked)
        # list_week
        self.list_week.itemDoubleClicked.connect(self.itemDoubleClicked)
        # 버튼에 기능 연결
        self.btn_add.clicked.connect(self.addListWidget)

    def itemDoubleClicked(self):
        try :
            #과목 & week 둘다 선택 시
            if(len(self.list_subject.currentItem().text()) >0):
                if(int(self.list_week.currentItem().text()) > 0):
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

        self.slider.valueChanged.connect(self.changeFunction)
        self.action_set_top_level.triggered.connect(self.setWindowTop)
        self.action_unset_top_level.triggered.connect(self.unsetWindowTop)
        self.action_hide.triggered.connect(self.hideFunction)
        self.action_unhide.triggered.connect(self.unhideFunction)
        self.action_capture.triggered.connect(self.captureFunction)

        self.action_stt.triggered.connect(self.sttFunction)
        
        data = self.textEdit.createMimeDataFromSelection()
        self.textEdit.canInsertFromMimeData(data)
        #시작시 과목 선택
        select = selectSubject()
        select.exec_()
        
        #내용 불러오기
        content = get_content(selectSubject.sub_name, selectSubject.sub_week, selectSubject.sub_date)
        self.setWindowTitle("과목 : " + selectSubject.sub_name)
        self.textEdit.setText(content)

        #생성된 노트 마지막에 커서 위치
        #self.cursor = self.plainTextEdit.textCursor()
        #self.cursor.setPosition(len(content))

        self.capture_cnt = 0

        self.setMouseTracking(True)

    def sttFunction(self):
        try:
            record()
        except Exception as ex:  # 에러 종류
            print('에러가 발생 했습니다', ex)


    #변경된 데이터 저장
    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('저장')
        msgBox.setText("변경 내용을  저장하시겠습니까?")
        msgBox.addButton('저장', QMessageBox.YesRole)  # 0
        msgBox.addButton('저장 안 함', QMessageBox.NoRole)  # 1
        msgBox.addButton('취소', QMessageBox.RejectRole)  # 2

        # 최상단 고정
        #msgBox.setWindowFlags(Qt.WindowStaysOnTopHint)
        msgBox.show()

        # 버튼 클릭 결과
        ret = msgBox.exec_()
        if ret == 0:
            self.save_file()
        else:
            return ret

    def closeEvent(self, event):
        ret = self.save_changed_data()

        if ret == 2:
            event.ignore()

    def save_file(self):
        sub_name = selectSubject.sub_name
        sub_week = selectSubject.sub_week
        sub_date = selectSubject.sub_date
        sub_image = selectSubject.sub_image

        data = self.textEdit.toPlainText()

        #선택한 주차 내용 불러오기
        content_start = data.find(sub_date) + len(sub_date) + 1
        sub_content = data[content_start:]

        tup = (sub_name, sub_week, sub_date,sub_content,sub_image)
        add_subject(tup)  # oracle db에 저장

        '''
        # data 마지막시간 기준으로 그 후 데이터 찾기
        compare_string = "==================="
        iCnt=1 
        # 주차 별 내용 담기
        for date in date_list:
            content_start = data.find(date) +len(date) + 1
            content_end = data.find(compare_string,iCnt+1) -1

            selectSubject.sub_content= data[content_start:content_end]
            print(selectSubject.sub_content)
        '''

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

        pyautogui.screenshot('D:/{}.png'.format(self.now), region=(500, 100, 1000, 700))
        print("캡쳐 완료")



app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()