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

def get_content(sub_name):
    os.putenv('NLS_LANG', '.UTF8')
    con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
    cursor = con1.cursor()

    content_notepad = ""
    date_list = []  # date_name 리스트
    week_list = []  # week_name 리스트
    content_list = []  # content_name 리스트

    query_name = "select sub_name from notepad"
    query_date = "select sub_date from notepad"
    query_week = "select sub_week from notepad"
    query_content = "select sub_content from notepad"

    cursor.execute(query_name)
    for row in cursor:
        str(row) == sub_name

    cursor.execute(query_date)
    for row in cursor:
        length = len(row)
        date_list.append(list(row))

    cursor.execute(query_week)
    for row in cursor:
        week_list.append(list(row))

    cursor.execute(query_content)
    for row in cursor:
        content_list.append(list(row))
    content_notepad="===================\n"

    for i in range(length):
        content_notepad += str(week_list[i]).strip('[]/\'') + "주차 - " \
                           + str(date_list[i]).strip("[]/\''") +"\n\n"
        content_notepad += str(content_list[i]).strip('[]/\'') +"\n\n\n"

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

