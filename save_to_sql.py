import sqlite3
import os




conn = sqlite3.connect('my.db')
cursor = conn.cursor()




def create():
    cursor.execute("""CREATE TABLE export """)






def add_line(items, link=''):
    for i in items:
        cursor.execute('''
        ALTER TABLE export ADD COLUMN ? text''', i)






