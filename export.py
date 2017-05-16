#!/usr/bin/python
# -*- coding: utf-8 -*-
import fileinput
import os
import sys
import re
import MySQLdb
import time
import thread
import codecs
import zipfile
from datetime import datetime


def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))


connection = MySQLdb.connect("incent3.mysql.domeneshop.no","incent3","jgi7VLPG","incent3" ,charset="utf8", use_unicode=True)
cursor = connection.cursor()

directory = 'files'

if not os.path.exists(directory):
    os.makedirs(directory)


print "fetching customers details...\n"

#try:
cursor.execute("""select * from accounts""")
accounts_result = cursor.fetchall()

for row in accounts_result:
	

	# row[0] is customer id 
	customer_id = str(row[0])
	customer = row[1]

	print customer_id +" --- " +  customer + "\n"

	# get tags for customer 
	cursor.execute("""select id,tag_name,tag_order,description from tags where customer_id=%s""", (customer_id) )
	tags_resultset = cursor.fetchall()

	ftags= open('files/'+ customer + '_tags.txt', 'ab')

	print "starting to write tags - " + customer +  '\n'

	for tags_row in tags_resultset:
		tempstr = tags_row[1] + ';' +  str(tags_row[2]) +  ';' +  tags_row[3] +  ';\n'
		ftags.write(tempstr.encode('utf-8'))
	ftags.close()


	print "starting to write account_users - " + customer +  '\n'

	
	# get account users
	cursor.execute("""select * from account_users where customer_id=%s""", (customer_id))
	account_users = cursor.fetchall()
		
	faccuser=open( 'files/'+ customer + '_account_users.txt','ab' )
	#faccuser =  codecs.open(row[1] + '_account_users.txt' , "w", "utf-8")

	for acc_row in account_users:
		tempaccstr =acc_row[1] + ';' + acc_row[2] + ';'+ acc_row[4] +';' +acc_row[5] + ';' + acc_row[9] + ';' + acc_row[8] + ';' +acc_row[7] + ';' 
		#txt = unicode(tempstr, "utf-8") acc_row[0] is account user id
		account_usr_id = acc_row[0];

		cursor.execute("""select tags.tag_name from account_user_tag_relationships inner join tags on account_user_tag_relationships.tag_id = tags.id where account_user_tag_relationships.account_user_id=%s""", (account_usr_id))
		acc_tag_rl= cursor.fetchall()
		tempacctagrl=''

		if acc_tag_rl is not None:
			for acc_tag_row in acc_tag_rl:
				tempacctagrl += acc_tag_row[0] + ','

		tempstr =  tempaccstr  + tempacctagrl + '\n'

		faccuser.write(tempstr.encode('utf-8') )
	faccuser.close()



	print "starting to write users - " + customer +  '\n'


	# get account users
	cursor.execute("""select * from users where customer_id=%s""", (customer_id))
	users_resultset = cursor.fetchall()
		
	fuser=open( 'files/'+ customer + '_users.txt','ab' )
	#faccuser =  codecs.open(row[1] + '_account_users.txt' , "w", "utf-8")

	for usr_row in users_resultset:
		tempusrstr =str(usr_row[4]) + ';' + str(usr_row[2])+ ';'+ str(usr_row[3]) +';' + str(usr_row[7]) + ';' + str(usr_row[6]) + ';' + str(usr_row[8]) + ';' + str( usr_row[9]) + ';' +  str(usr_row[10]) + ';'
		#txt = unicode(tempstr, "utf-8") acc_row[0] is account user id
		usr_id = usr_row[0];

		cursor.execute("""select tags.tag_name from user_tag_relationships inner join tags on user_tag_relationships.tag_id = tags.id where user_tag_relationships.user_id=%s""", (usr_id))
		usr_tag_rl= cursor.fetchall()
		tempusrtagrl=''

		if usr_tag_rl is not None:
			for usr_tag_row in usr_tag_rl:
				tempusrtagrl += usr_tag_row[0] + ','

		tempstr =  tempusrstr  + tempusrtagrl + '\n'

		fuser.write(tempstr.encode('utf-8') )
	fuser.close()


	print "Keywords upload...\n"

	# get tags for customer 
	cursor.execute("""SELECT keywords.id, keywords.keyword FROM keywords where keywords.customer_id=%s""", (customer_id) )
	keyword_resultset = cursor.fetchall()

	fkeywords= open('files/'+ customer + '_keywords.txt', 'ab')

	print "starting to write keywords - " + customer +  '\n'

	for keyword_row in keyword_resultset:
		keyword_id = str(keyword_row[0])
		tempkeywordstr =  keyword_row[1].replace(' ',';') + ';'

		cursor.execute("""select keyword_action_fields.name , keyword_action_fields.value from keyword_action inner join keyword_action_fields on keyword_action.id =keyword_action_fields.keyword_action_id where keyword_action_fields.name='MAIL_TO' and keyword_action.keyword_id=%s""",keyword_id )
		keyword_emails = cursor.fetchone()

		if keyword_emails is not None:
			tempkeywordstr += str(keyword_emails[1])

		cursor.execute("""select keyword_action_fields.name , keyword_action_fields.value from keyword_action inner join keyword_action_fields on keyword_action.id =keyword_action_fields.keyword_action_id where keyword_action_fields.name='SMS_TO' and keyword_action.keyword_id=%s""",keyword_id )
		keyword_phones = cursor.fetchone()

		if keyword_phones is not None:
			tempkeywordstr += str(keyword_phones[1])

		fkeywords.write(tempstr.encode('utf-8'))
	fkeywords.close()



		
	print "Finishing " +customer + "\n"


zip = zipfile.ZipFile('files.zip', 'w')
zipdir('files/', zip)
zip.close()

print "End...\n"

#except:
#	print "Error: unable to fetch details \n"
