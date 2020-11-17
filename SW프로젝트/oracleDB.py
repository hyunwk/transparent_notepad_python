import cx_Oracle
import os

def get_subject():
    os.putenv('NLS_LANG', '.UTF8')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()
    #program 시작시 과목 출력 db
    cursor.execute('select sub_name from notepad')

    sub_list =[] #sub_name 리스트

    for row in cursor:
        if row not in sub_list: # 중복 제거
            a=str(row).strip('()/\',')
            sub_list.append(a)

    cursor.close()
    con1.close()
    return sub_list

#get_content 를 위한 리스트
date_list = []  # date_name 리스트
week_list = []  # week_name 리스트
content_list = []  # content_name 리스트

def get_content(sub_name, sub_week,sub_date):
    os.putenv('NLS_LANG', '.UTF8')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    cursor.execute("SELECT * FROM notepad")
    is_exist = False
    try:
        for row in cursor:
            if( row[0] == sub_name): #과목명 같을 경우
                if(row[1] == sub_week): # week 다를 경우
                    is_exist = True

                week_list.append(row[1])
                date_list.append(row[2])
                content_list.append(row[3])

        content_notepad = sub_name + "\n===================\n"
        for i in range(len(week_list)):
            content_notepad += str(week_list[i]).strip('[]/\'') + "주차 - " \
                               + str(date_list[i]).strip("[]/\''") +"\n\n"\
                               + str(content_list[i]).strip('[]/\'') +"\n\n\n"
        if(not is_exist):
            content_notepad += "===================\n"
            content_notepad += str(sub_week) + "주차 - " + sub_date + "\n"

    except Exception as ex:
        print("에러가 발생했습니다. :",ex)

    cursor.close()
    con1.close()

    return content_notepad

def add_subject(tup):
    os.putenv('NLS_LANG', '.UTF8')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    try :
        query = "INSERT INTO NOTEPAD VALUES (:1,:2,:3,:4)"
        cursor.execute(query,tup)
        con1.commit()

    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)

    cursor.close()
    con1.close()

