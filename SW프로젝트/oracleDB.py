import cx_Oracle
import os
os.putenv('NLS_LANG', '.UTF8')

con1 = cx_Oracle.connect('SYSTEM/AB8488454@localhost:1521/ORCL')
cursor = con1.cursor()

#program 시작시 과목 출력 db
cursor.execute('select sub_name from notepad')

sub_list =[] #sub_name 리스트

for row in cursor:
    if row not in sub_list: # 중복 제거
        sub_list.append(row)

cursor.close()
con1.close()
