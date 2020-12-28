from flask import Flask

app = Flask(__name__)
@app.route("/")
def hello():
	return "Welcome to Python Flask!"


if __name__ == "__main__":
	app.run()




####!/usr/bin/python
#### -*- coding: UTF-8 -*-
###
###import sqlite3
###import cgi
###import sys
###import json
###
###
###def output(content):
###	sys.stdout.write('Content-Type: text/plain\n\n')
###	sys.stdout.write(content)
###
###
###form = cgi.FieldStorage()
###
###fail = 0
###try:
###	myData = str(form['myData'].value)
###except:
###	fail = 1
###else:
###	if myData == "":
###		fail = 1
###
###if fail == 1:
###	output('Who are you?')
###	raise SystemExit
###
####db_filename = '/cgi-bin/PhyComb.db'
####conn = sqlite3.connect(db_filename)
####curs = conn.cursor()
####query_phyComb = "SELECT * from %s" %myData
####curs.execute(query_phyComb)
####rows = curs.fetchall()
####print (rows)
####conn.close()
###
####output('row[0],row[1],row[2] - ' + row[0] + row[1] + row[2])
###output('Output mydata ' + myData)
###
###
####output(json.dumps(pythonObject)) # sends the Python variable content to javascript as JSON
####pyObject = json.loads(jsonString) # now you can use the data in Python
###
###




