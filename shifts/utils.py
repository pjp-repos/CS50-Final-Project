from django.db import connection
import datetime

def stampCheck(user,day):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO shifts_firestampcheck (user,day,status) VALUES ( %s,%s,%s)", [user,day,False])

def timeEvaluation(user,day):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO shifts_firesp (user,day,status) VALUES ( %s,%s,%s)", [user,day,False])

def deleteRow(table,id):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM shifts_{table} WHERE id={id}")

def dateValidate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False
  