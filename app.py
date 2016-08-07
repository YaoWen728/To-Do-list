#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response
import MySQLdb
import json
from flask_httpauth import HTTPBasicAuth
import sys
import logging
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()

############### Checking password

@auth.get_password
def get_password(Username):
	sys.stderr.write('Password ...')
	print ('Password ...')

	connection = MySQLdb.connect(host='localhost',user='n1q52',passwd='H9zhy72rA',db='n1q52', use_unicode=True, charset='utf8')
	cursor = connection.cursor(MySQLdb.cursors.DictCursor)
	sql = "CALL getUser('%s')" %(Username)
	
	try:
		cursor.execute(sql)
	except:
	# 	Things messed up
		abort(404)

	row = cursor.fetchone()
	print str(row)
	UPassword = row['UserPassword']

	cursor.close()
	connection.close()
	
	if UPassword != '' :
		return UPassword
		
	return None
		
#@auth.error_handler
def bad_authentication():
	return make_response(jsonify({'error':'Bad username or password.'}), 403)
	
@app.errorhandler(405)
def unauthorized(error):
	return make_response(jsonify({'error':'You have no authority to view this page.'}), 405)

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)


###### Get all the list and things to do for a user.

@app.route('/', methods=['GET'])
def index():
	sys.stderr.write('Testing...\n')
	logging.info('Testing....')
	return jsonify({'message': 'Hello'})


@app.route('/todo/list', methods=['GET'])
@auth.login_required
def get_List():
	logging.info('To do ....')
	sys.stderr.write('To do...')
	connection = MySQLdb.connect(host='localhost',user='n1q52',passwd='H9zhy72rA',db='n1q52', use_unicode=True, charset='utf8')
	cursor = connection.cursor(MySQLdb.cursors.DictCursor)
	sql = "CALL getList('%s');"%(str(auth.username()))

	print "Executing SQL procedure: %s"%(sql)
	
	try:
		cursor.execute(sql)
	except:
	# 	Things messed up
		abort(404)

	set = cursor.fetchall()
	print str(set)
	print type(set)
	
	for row in set:
		row['DueOn'] = str(row['DueOn'])
		row['WriteOn'] = str(row['WriteOn'])

	cursor.close()
	connection.close()
	return jsonify({'ListTable': set})

###### Get all the things to do given a the name of the list.	
@app.route('/todo/<string:User_Name>/<string:List_Name>', methods=['GET'])
@auth.login_required
def get_Content(User_Name, List_Name):
	if str(auth.username()) != User_Name:
		abort(405)

	connection = MySQLdb.connect(host='localhost',user='n1q52',passwd='H9zhy72rA',db='n1q52', use_unicode=True, charset='utf8')
	cursor = connection.cursor(MySQLdb.cursors.DictCursor)
	sql = "CALL getContent('%s', '%s')"%(User_Name, List_Name)
	try:
		cursor.execute(sql)
	except:
	# 	Things messed up
		abort(404)

	set = cursor.fetchall()
	print str(set)
	print type(set)

	for row in set:
		row['DueOn'] = str(row['DueOn'])
		row['WriteOn'] = str(row['WriteOn'])


	cursor.close()
	connection.close()
	return jsonify({'ListTable': set})


@app.route('/todo/entry', methods=['POST'])
@auth.login_required
def Insert_Content():
	print "Insert content into list:"
	print json.dumps(request.json)
	
	username = request.json.get('UserName');
	
	print str(auth.username()).lower()
	print str(username).lower()
	
	if str(auth.username()).lower() != str(username).lower():
		abort(405)
	
	listName = request.json.get('ListName',);
	content = request.json.get('Content',);
	writeOn = request.json.get('WriteOn',);
	dueOn = request.json.get('DueOn');

	connection = MySQLdb.connect(host='localhost',user='n1q52',passwd='H9zhy72rA',db='n1q52', use_unicode=True, charset='utf8')
	cursor = connection.cursor()
	sql = "CALL InsertContent('%s', '%s', '%s', '%s', '%s');"%(str(auth.username()), listName, content, writeOn, dueOn)
	print sql
	
	try:
		cursor.execute(sql)

	except:
	# 	Things messed up
		abort(500)

	set = cursor.fetchall()
	connection.commit()
	cursor.close()
	connection.close()

	return make_response(jsonify( { 'error': 'success' } ), 201)

####################### Delete a row

@app.route('/todo/<string:User_Name>/<int:ListID>', methods=['DELETE'])
@auth.login_required
def Delete_Content(User_Name,ListID):

	if str(auth.username()) != User_Name:
		abort(405)
		
	connection = MySQLdb.connect(host='localhost',user='n1q52',passwd='H9zhy72rA',db='n1q52', use_unicode=True, charset='utf8')
	cursor = connection.cursor(MySQLdb.cursors.DictCursor)
	sql = "CALL DeleteContent('%s',%d)"%(User_Name,ListID)
	
	print sql
	
	try:
		status = cursor.execute(sql)
	except:
		abort(404)
	
	set = cursor.fetchall()
	connection.commit()
	cursor.close()
	connection.close()
	
	print str(set)
	
	return jsonify({'Successful': 'True'})


#############################################################################
# xxxx= last 4 digits of your studentid+1024
if __name__ == "__main__":
	#logging.basicConfig(filename='todo.log',level=logging.DEBUG)
	app.run(host="info3103.cs.unb.ca", port=3752, debug=True)
