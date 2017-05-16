# -*- coding: utf-8 -*-
import fileinput
import os
import sys
import re

ins = open("S_KAT.txt", "r" )
#for mline in fileinput.input(['schools.txt']):

#synlist=[]
fop=open('KAT.txt','ab')

for mline in ins:
        data = mline.split(';')
        firstname = data[2]
        lastname = data[3]
        email = data[4]
        emailx=''
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
                emailx=''
        else:
                emailx=email
        mobile = data[7]
        groupids = data[9:]
        mobile = mobile.replace('-','')
        mobile = mobile.replace(' ','')
        mobile = mobile.strip()
        
        if len(mobile) > 0:
                mobile = '46' + mobile[1:]
                synlist = mobile +  ';' + firstname + ';' + lastname + ';' + emailx + ';' + ';;;;' + ','.join(groupids) 
                fop.write(synlist)
        print(synlist)
fop.close()
