import mysql.connector
from mysql.connector import errorcode


try:
  conn = mysql.connector.connect(
    host="localhost",
    user="",
    passwd="",
    database=""
  )

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Usuario ou senha inválidos")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database inexistente")
  else:
    print(err)  

cursor = conn.cursor()