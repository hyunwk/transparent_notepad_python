import cx_Oracle
import os


#get_content 를 위한 리스트
sub_list = [] # sub_name 리스트
date_list = []  # date_name 리스트
week_list = []  # week_name 리스트
content_list = []  # content_name 리스트

content_exists=False

#시작시 과목 list 출력
def get_subject():
    os.putenv('NLS_LANG', '.UTF8')
    #con1 = cx_Oracle.connect('SYSTEM/AB8488454@192.168.35.177:1521/ORCL')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    #program 시작시 과목 출력 db
    cursor.execute('select sub_name from notepad')

    #과목 리스트 db에서 가져옴
    for row in cursor:
        if str(row).strip('()/\',') not in sub_list: # 중복 제거
            sub_list.append(str(row).strip('()/\',')) # 양식 정리

    cursor.close()
    con1.close()
    return sub_list

#과목 내용 불러오기
def get_content(sub_name, sub_week,sub_date):
    os.putenv('NLS_LANG', '.UTF8')
    # con1 = cx_Oracle.connect('SYSTEM/AB8488454@192.168.35.177:1521/ORCL')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    cursor.execute("SELECT * FROM notepad order by sub_week ")

    try:
        for row in cursor:
            #1. 과목 존재 시
            if( row[0] == sub_name):
                # 2. 과목, 주차 존재 시
                if(row[1] == sub_week):
                    global content_exists
                    content_exists = True
                    cursor1 = con1.cursor()
                    query = "UPDATE NOTEPAD SET sub_date = to_char((:3)) " \
                            "where sub_name = to_char((:1)) and sub_week = to_number((:2))"
                    tup=(sub_name, sub_week, sub_date)

                    cursor1.execute(query, tup)
                    con1.commit()
                    week_list.append(sub_week)
                    date_list.append(sub_date)
                    content_list.append(row[3])
                    continue


                week_list.append(row[1])
                date_list.append(row[2])
                content_list.append(row[3])

        #내용 담을 변수
        content_notepad= ""

        for i in range(len(week_list)):
            content_notepad += "===================\n"\
                              + str(week_list[i]).strip('[]/\'') + "주차 - " \
                               + str(date_list[i]).strip("[]/\''") +"\n"\
                               + str(content_list[i]).strip('[]/\'') +"\n\n"

        # 3.선택한 과목명과 주차가 이미 존재하지 않을 시
        if(not content_exists):
            content_notepad += "===================\n"
            content_notepad += str(sub_week) + "주차 - " + sub_date + "\n"

    except Exception as ex:
        con1.rollback()
        print("에러가 발생했습니다. :",ex)

    cursor.close()
    con1.close()

    return content_notepad

#과목 내용 저장하기
def add_content(tup):
    os.putenv('NLS_LANG', '.UTF8')
    # con1 = cx_Oracle.connect('SYSTEM/AB8488454@192.168.35.177:1521/ORCL')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()
    global content_exists
    tup1=tup[:2]
    try:
        # 1.같은 과목, 주차 선택 경우
        if(content_exists):
            query = "delete from notepad where sub_name = (:1) and sub_week = (:2)"
            cursor.execute(query,tup1)

        # 2. 주차 다른 경우 #3. 새로운 과목 선택
        query = "INSERT INTO NOTEPAD VALUES (:1,:2,:3,:4)"
        cursor.execute(query,tup)
        con1.commit()

    except Exception as ex:  # 에러 종류
        con1.rollback()
        print('에러가 발생 했습니다', ex)

    cursor.close()
    con1.close()