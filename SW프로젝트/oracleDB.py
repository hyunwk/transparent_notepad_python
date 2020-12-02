import cx_Oracle
import os

#get_content 를 위한 리스트
date_list = []  # date_name 리스트
week_list = []  # week_name 리스트
content_list = []  # content_name 리스트

#시작시 과목 출력 함수
def get_subject():
    os.putenv('NLS_LANG', '.UTF8')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    #program 시작시 과목 출력 db
    cursor.execute('select sub_name from notepad')

    # sub_name 리스트
    sub_list =[]

    #과목 리스트 db에서 가져옴
    for row in cursor:
        if str(row).strip('()/\',') not in sub_list: # 중복 제거
            sub_list.append(str(row).strip('()/\',')) # 양식 정리

    cursor.close()
    con1.close()
    return sub_list

#선택한 과목 내용 출력
def get_content(sub_name, sub_week,sub_date):
    os.putenv('NLS_LANG', '.UTF8')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    cursor.execute("SELECT * FROM notepad order by sub_week ")
    is_exist = False

    try:
        for row in cursor:
            if( row[0] == sub_name): #선택한 과목명과 db의 과목명이 같을 경우

                if(row[1] == sub_week): #선택한 과목명과 주차가 이미 존재할 시
                    is_exist = True

                else:
                    week_list.append(row[1])
                    date_list.append(row[2])
                    content_list.append(row[3])

        content_notepad= ""

        for i in range(len(week_list)):
            content_notepad += "===================\n"\
                              + str(week_list[i]).strip('[]/\'') + "주차 - " \
                               + str(date_list[i]).strip("[]/\''") +"\n"\
                               + str(content_list[i]).strip('[]/\'') +"\n\n"

        # 선택한 과목명과 주차가 이미 존재하지 않을 시
        if(not is_exist):
            content_notepad += "===================\n"
            content_notepad += str(sub_week) + "주차 - " + sub_date + "\n"

    except Exception as ex:
        print("에러가 발생했습니다. :",ex)

    cursor.close()
    con1.close()

    return content_notepad

#저장 후 db에 추가/수정
def add_subject(tup):
    os.putenv('NLS_LANG', '.UTF8')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    cursor.execute("SELECT * FROM notepad order by sub_week ")
    try:
        for row in cursor:
            #과목명이 같은 경우
            if( row[0] == tup[0]):

                #과목명 같고 주차 같은경우
                if (get_content().is_exsit):  # sub_content 저장 후 다시 저장 할때
                    query = "UPDATE NOTEPAD SET sub_content =(:4),sub_image=(:5) " \
                            "where sub_name = (:1) and sub_week = (:2)"
                    cursor.execute(query,tup)
                    con1.commit()
                    cursor.close()
                    con1.close()
                    return

                #과목명 같고 주차 다른경우
                else :
                    query = "INSERT INTO NOTEPAD VALUES (:1,:2,:3,:4,:5)"
                    cursor.execute(query,tup)
                    con1.commit()
                    cursor.close()
                    con1.close()
                    return

        #과목명 다른 경우 / db가 없을 경우
        query = "INSERT INTO NOTEPAD VALUES (:1,:2,:3,:4,:5)"
        cursor.execute(query, tup)
        con1.commit()

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)


    cursor.close()
    con1.close()

