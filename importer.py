#!/usr/bin/python
# -*- coding: utf-8 -*-
import fileinput
import os
import sys
import re
import MySQLdb
import time
import thread
import hashlib
from datetime import datetime


def validate_norwegian_phone_number(number):
	number = re.sub("[^0-9]","",number)
	number = number.lstrip('0')
	if(len(number) == 8):
		number = '47' + number
	if len(number) == 10:
		number=number
	else:
		number=''
	if len(number) > 0:
		first_digit = number[2]
		if(first_digit != '4' and first_digit != '9'):
			number = ''
	return number

def validate_swedish_phone_number(number):
	number = re.sub("[^0-9]","",number)
	if (number[0:1]=='+'):
		tlf=number[1:]
	if len(number) > 6:
		number =number
	else:
		number =''
	number = number.lstrip('0')
	if(number[0:2] == '46' and len(number) > 9):
		print 'nothing..\n'
		#number = substr($number, 2);
	else:
		number = '46' + number
	#pattern = "(0{0,3}4610[0-9]*|0{0,3}4670[0-9]*|0{0,3}4672[0-9]*|0{0,3}4673[0-9]*|0{0,3}4676[0-9]*)"
	regex = re.compile("(0{0,3}4610[0-9]*|0{0,3}4670[0-9]*|0{0,3}4672[0-9]*|0{0,3}4673[0-9]*|0{0,3}4676[0-9]*)")
	match = regex.search(number)
	#match = re.search("pattern", number)

	if match:
		number =number
	else:
		number=''
	return number

	



t0 = time.time()

connection = MySQLdb.connect("localhost","root","toor","incent3" )
cursor = connection.cursor()
customer_id='1285'
account_user_id ='16181'
account_user_name=''
filename = 'S_AKA-BE.txt'
country ='NO'


cursor.execute ("""Select id from accounts where id=%s""",  (customer_id) )
datacusid = cursor.fetchone()
datacustomerid = str(datacusid[0])

print "data customer id "+ datacustomerid + "\n"

if datacustomerid == customer_id:
	print "Customer ID exits, good to proceed...\n"
else:
	print "Customer ID does not exits...\n"
	sys.exit()

cursor.execute ("""Select id,username from account_users where id=%s""", (account_user_id) )
dataaccout= cursor.fetchone()
dataaccount_user_id = str(dataaccout[0])

print "data Account id "+ dataaccount_user_id  + "\n"

if dataaccount_user_id == account_user_id:
	print "Account user ID exits, good to proceed...\n"
	account_user_name = str(dataaccout[1])
	print "Admin Account username ... " +  account_user_name + "\n"

else:
	print "Account User ID does exits...\n"
	sys.exit()


fgroup=open('groups.txt','ab')
fmember=open('members.txt','ab')
fmemberdb=open('membersDB.txt','ab')
fuser=open('users.txt','ab')
fuserdb=open('usersDB.txt','ab')

group=[]
groupdict = {}
memberdb=[]
members=[]
userdb=[]
users=[]

elicount=0

for line in fileinput.input([filename]):
	groupids=[]
	data = line.split(';')
	groupids = data[9:]

	for groupid in groupids:
		groupid = groupid.strip()
		groupid = groupid.replace(',',' -')
		groupid = groupid.replace('\n','')
		groupid = groupid.replace('\r','')

		if len(groupid) > 0:
			if len(group) == 0:
			 	group.append(groupid)
			 	fgroup.write(groupid  +'\n')
			else:
			 	x = 1
			 	for gr in group:
			 		if gr.strip().lower() == groupid.strip().lower():
			 			print groupid + " already exits\n"
			 			x = 3
			 			break

			 	if x == 1:
			 		print groupid + " adding...\n"
			 		group.append(groupid)
			 		#file_text = raw_input("Enter text: ")
			 		fgroup.write(groupid +'\n')
fgroup.close()

for groupname in group:
	cursor.execute ("""SELECT id FROM tags WHERE customer_id =%s AND tag_name LIKE %s """,( customer_id , groupname))
	data_tag = cursor.fetchone()

	if data_tag is not None:
		print  groupname + " Tag name exits... \n"
		print "groupid " + str(data_tag[0]) + "\n"
		groupdict.setdefault ( groupname , str(data_tag[0]) )
	else:
		print "adding to database... " + groupname + "\n"
		print "adding group to dict..\n"
		try:
			dt=datetime.utcnow()
			utime = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
			cursor.execute("""Insert into tags(tag_name,tag_order,description,customer_id,created_date,deleted_flag) values(%s,%s,%s,%s,%s,%s)""", (groupname,10,groupname,customer_id,utime,0) )
			connection.commit()
		except:
			print "Problem with data insert in group " + groupname + "\n"
			connection.rollback()
		print "Group Row id " +   str(cursor.lastrowid) + "\n"
		groupdict.setdefault ( groupname, str(cursor.lastrowid) )


print "Finished processing Groups... \n"
time.sleep(2)
print "Starting to process Members (users)...\n"


print "fetching members details from database...\n"
try:
	cursor.execute ("""SELECT id,first_name,last_name,phone,customer_id,description,email,custom_field3  FROM users WHERE customer_id =%s""", (customer_id) )
	member_result = cursor.fetchall()

	for row in member_result:
		print str(row[0]) +  " member adding...\n"
		memberdb.append(str(row[0]))
		fmemberdb.write(str(row[0]) + ';' +  str(row[1]) + ';'+ str(row[2]) + ';'+ str(row[3])  + ';' + str(row[4]) + ';'+ str(row[5]) + ';'+ str(row[6])  + ';' + str(row[7]) + '\n')
except:
	print "Error: unable to fecth member data \n"

fmemberdb.close()

time.sleep(2)
print "Starting to process users (Account users)...\n"


print "fetching user details from database...\n"
try:
	cursor.execute ("""SELECT id, username,password,first_name,last_name,phone,customer_id,description,email FROM account_users WHERE customer_id =%s""", (customer_id) )
	user_result = cursor.fetchall()

	for row in user_result:
		print str(row[0]) +  " user adding...\n"
		userdb.append(str(row[0]))
		fuserdb.write(str(row[0]) + ';' +  str(row[1]) + ';'+ str(row[2]) + ';'+ str(row[3])  + ';' + str(row[4]) + ';'+ str(row[5]) + ';'+ str(row[6])  + ';' + str(row[7]) + ';' +  str(row[8]) +  '\n')
except:
	print "Error: unable to fecth user data \n"

fuserdb.close()
time.sleep(2)

for line in fileinput.input([filename]):
	data = line.split(';')

	firstname = data[2]
	lastname = data[3]
	email = data[4]
	emailx=''
	if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
		emailx=''
	else:
		emailx=email


	mobile = data[7]
	mobile2 = data[6]

	desc = data[8].strip()

	username = data[1].strip()


	groupids = data[9:]
	groupids = [w.replace(',', ' -') for w in groupids]
	mobile = mobile.replace('-','')
	mobile = mobile.replace(' ','')
	mobile = mobile.strip()

	mobile2 = mobile2.replace('-','')
	mobile2 = mobile2.replace(' ','')
	mobile2 = mobile2.strip()

	mobilex=''

	exgroupids = data[9:]


	if len(mobile.strip()) > 0:
		#if mobile[0] == '4' or mobile[0] == '9':
		#	mobile = '47' + mobile
		#	if len(mobile) == 10:
		if country == 'NO':
			mobilex =  validate_norwegian_phone_number(mobile);
		elif country == 'SE':
			mobilex =  validate_swedish_phone_number(mobile);

	else:
		if len(mobile2.strip()) > 0:
			if country == 'NO':
				mobilex =  validate_norwegian_phone_number(mobile2);
			elif country == 'SE':
				mobilex =  validate_swedish_phone_number(mobile2);

			#if mobile2[0] == '4' or mobile2[0] == '9':
			#	mobile2 = '47' + mobile2
			#	if len(mobile2) == 10:
			#		mobilex = mobile2

	print "Mobile number......... " +  mobilex + "\n"


	if 1==1:

		print "Mobile number valid... \n"

		if len(desc) > 0 :

			print desc + " sepration seems good...\n"


			#if desc.lower() == 'Student'.lower():
			#if desc.lower() in ('Student'.lower() , 'Learner'.lower()): 
			if len(mobilex.strip()) > 0:

				print "Procesing Student (this includes everyone to add inside the member database... \n"

				synlist = mobilex +  ';' + firstname + ';' + lastname + ';' + emailx + ';' + desc +  ';;;' + username +';' + ','.join(groupids)
				fmember.write(synlist)
				print(synlist)

				print "Procesing members checking...\n"
				memberid=''

				cursor.execute ("""SELECT id FROM users WHERE customer_id =%s AND phone =%s""", (customer_id , mobilex) )
				data_member = cursor.fetchone()

				if data_member is None:
					if len(username) > 0:
						print "Accessing second choice for member username..."+ username +"\n"
						cursor.execute ("""SELECT id FROM users WHERE customer_id =%s AND custom_field3=%s""", (customer_id , username) )
						data_member2 = cursor.fetchone()

				if data_member is not None:
					print  str(data_member[0]) + " Member already exits... Updating...\n"
					members.append(str(data_member[0]))
					memberid= str(data_member[0])
					

					try:
						cursor.execute("""Update users set first_name=%s ,last_name=%s ,description=%s ,email=%s ,custom_field3=%s where customer_id=%s and id=%s""", (firstname,lastname, desc, emailx, username ,customer_id , memberid  ) )
						connection.commit()
					except:
						print "Problem with data update in member " + mobilex + "\n"
						connection.rollback()

				elif data_member2 is not None:

					print  str(data_member2[0]) + " Member already exits(2)... Updating...\n"
					members.append(str(data_member2[0]))
					memberid= str(data_member2[0])
					

					try:
						cursor.execute("""Update users set first_name=%s ,last_name=%s ,description=%s ,email=%s ,phone=%s where customer_id=%s and id=%s""", (firstname,lastname, desc, emailx, mobilex ,customer_id , memberid  ) )
						connection.commit()
					except:
						print "Problem with data update in member " + mobilex + "\n"
						connection.rollback()
			
				else:
					print "Inserting members database... \n"
					try:
						dt=datetime.utcnow()
						utime = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
						cursor.execute ("""Insert into users(first_name,last_name,phone,customer_id,description,email,custom_field3,active_flag,created_date,deleted_flag) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(firstname ,lastname,mobilex,customer_id,desc,emailx,username,1,utime,0)  )
						connection.commit()
					except:
						print "Problem with data insert in member " + mobilex + "\n"
						connection.rollback()
					members.append(str(cursor.lastrowid))
					print "Member Row id " +   str(cursor.lastrowid) + "\n"
					memberid= str(cursor.lastrowid)

				print "members tag relationship processing...\n"

				try:
					print "deleting user tag relationship... " + str(memberid) + "\n"
					cursor.execute("""delete from user_tag_relationships where user_id =%s""" , (str(memberid))  )
					connection.commit()
				except:
					print "Problem with data delete in member " + str(memberid) + "\n"
					connection.rollback()


				for mgroupid in exgroupids:
					mgroupid = mgroupid.strip()
					mgroupid = mgroupid.replace(',',' -')
					mgroupid = mgroupid.replace('\n','')
					mgroupid = mgroupid.replace('\r','')
					if len(mgroupid) > 0:
						vartag_id =  groupdict.get(mgroupid)
						tag_id = str(vartag_id)
						print "process tag "+ mgroupid + "\n"
						print  tag_id + " tag id \n"

						try:
							cursor.execute("""Insert into user_tag_relationships(user_id,tag_id) values (%s,%s)""", (str(memberid) , tag_id) )
							connection.commit()
							print "Inserting members tag relationship..." +  str(memberid) + "\n"
						except:
							print "Problem with data insert in member tag relationship " + str(memberid) + "\n"
							connection.rollback()
			else:
				elicount += 1
			#elif desc.lower() == 'Staff'.lower():or desc.lower() == 'Administrator'.lower()
			if desc.lower() in ('Staff'.lower() , 'Administrator'.lower()):  
				print "Procesing Staff...\n"

				synlist = mobilex +  ';' + firstname + ';' + lastname + ';' + emailx + ';' + desc +  ';;;' + username +';' + ','.join(groupids)
				fuser.write(synlist)
				print(synlist)

				print "Procesing staff checking...\n"
				userid=''

				cursor.execute ("""SELECT id FROM account_users WHERE customer_id =%s AND username =%s """, (customer_id , account_user_name +':'+username ) )
				data_user = cursor.fetchone()


				if data_user is not None:
					print  str(data_user[0]) + " account user already exits... Updating...\n"
					users.append(str(data_user[0]))
					userid= str(data_user[0])

					try:
						cursor.execute("""Update account_users set first_name=%s , last_name=%s ,description=%s ,email=%s ,phone=%s where customer_id=%s and id=%s""",  (firstname ,lastname , desc , emailx , mobilex ,customer_id , userid ) )
						connection.commit()
					except:
						print "Problem with data update in user " + username + "\n"
						connection.rollback()

				else:
					print "Inserting users database... \n"
					try:
						cursor.execute ("""Insert into account_users(username,password,customer_id,first_name,last_name,superuser_flag,description,email,phone,active_flag) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """ ,(account_user_name + ':'+ username , hashlib.md5('123456').hexdigest() , customer_id ,  firstname , lastname ,0, desc , emailx , mobilex ,1) )
						connection.commit()
					except:
						print "Problem with data insert in user " + username + "\n"
						connection.rollback()
					users.append(str(cursor.lastrowid))
					print 'fuck\n'
					print "user Row id " +   str(cursor.lastrowid) + "\n"
					userid= str(cursor.lastrowid)

				print "user tag relationship processing...\n"

				try:
					print "deleting user tag relationship... " + str(userid) + "\n"
					cursor.execute("""delete from account_user_tag_relationships where account_user_id =%s""" , (str(userid)) )
					connection.commit()
				except:
					print "Problem with data delete in user " + str(userid) + "\n"
					connection.rollback()


				for ugroupid in exgroupids:
					ugroupid = ugroupid.strip()
					ugroupid = ugroupid.replace(',',' -')
					ugroupid = ugroupid.replace('\n','')
					ugroupid = ugroupid.replace('\r','')
					if len(ugroupid) > 0:
						vartag_id =  groupdict.get(ugroupid)
						tag_id = str(vartag_id)
						print "process tag "+ ugroupid + "\n"
						print  tag_id + " tag id \n"

						try:
							cursor.execute("""Insert into account_user_tag_relationships(account_user_id,tag_id) values (%s,%s)""" ,(str(userid) ,tag_id) )
							connection.commit()
							print "Inserting users tag relationship..." +  str(userid) + "\n"
						except:
							print "Problem with data insert in user tag relationship " + str(userid) + "\n"
							connection.rollback()
		else:
			print "Eliminating members... "
			elicount =elicount +1


fmember.close()
fuser.close()

print "Differcing member details...\n"

#diffmember = list(set(memberdb) - set(members))

#print diffmember

print "Careful... we are going to delete members here... \n"
for dmem in memberdb:

	if dmem in members:
		print str(dmem) + " find member in lastest csv file... \n"
	else:
		try:
			cursor.execute("""delete from users where id =%s""" ,  (str(dmem)) )
			connection.commit()
			print "Deleting users userid..." +  str(dmem) + "\n"
			cursor.execute("""delete from user_tag_relationships where user_id =%s""" ,  (str(dmem)) )
			connection.commit()
			print "Deleting user tag relationship userid..." +  str(dmem) + "\n"
		
		except:
			print "Problem with data delete in member " + str(dmem) + "\n"
			connection.rollback()
print "Deleted corrosponding data from member,member tag details...\n"



print "Differcing user details...\n"

#diffuser = list(set(userdb) - set(users))

#print diffuser

print "Careful... we are going to delete users here... \n"
for dusr in userdb:

	if str(dusr) != account_user_id:

		if dusr in users:
			print str(dusr) + " find user in lastest csv file...\n"
		else:
			try:
				cursor.execute("""delete from account_users where superuser_flag= 0 and id =%s""",(str(dusr)) )
				connection.commit()
				print "Deleting users userid..." +  str(dusr) + "\n"
				cursor.execute("""delete from account_user_tag_relationships where account_user_id =%s""", (str(dusr)) )
				connection.commit()
				print "Deleting user tag relationship userid..." +  str(dusr) + "\n"
			except:
				print "Problem with data delete in user " + str(dusr) + "\n"
				connection.rollback()

print "Deleted corrosponding data from user,user tag details...\n"

print "Summary.... \n"

print "Total Members from database... " + str(len(memberdb)) + "\n"
print "Total Inserted Members from file... " + str(len(members)) + "\n"

print "Total differcing members... " + str( len(members) - len(memberdb) )+ "\n"

print "Total users from database... " + str(len(userdb) )+ "\n"
print "Total Inserted users from file... " + str(len(users) )+ "\n"

print "Total differcing users... " +str( len(users) - len(userdb)) + "\n"

print "Total eliminated persons from file... " +str(elicount) +"\n"





print "Finished importing...Total Process Time >> " +  str(time.time()-t0)

connection.close()
