import sqlite3 as lite
import sys
con = lite.connect('sensorsData.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS MOTION_stat")
    cur.execute("CREATE TABLE MOTION_stat(timestamp DATETIME, stat NUMERIC)")
