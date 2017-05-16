from soapthread import *
import time
import fileinput
import os
import re
import thread
import smtplib
import base64

t0 = time.time()
synlist=[]
print "---opening IMSdataSAP.txt---\n"
print "Sit back and relax, bot is starting up...\n"
for line in fileinput.input(['IMSdataSAP.txt']):
    synid =line.split(';')
    if len(synid[0].strip()) > 0:
        if synid[0].find("itsla") == -1 and synid[0].find('#') == -1:
            print'Adding - ' + synid[0] + '\n'   
            synlist.append(synid[0])
        else:
            print 'Found itsla! avoiding... '+ synid[0] + '\n'

threads=[]
mycon =0
print 'big list size.... ' + str(len(synlist)) + '\n'

print 'Please wait... Engine is warming up...\n'
while 1==1:
    #break #take it out
    print '\n' + str(mycon) + ' -starting new bulk...\n'
    i=0
    for item in synlist:
        i += 1
        if i >= mycon and i < mycon+50:
            x = myThread(item)
            threads.append(x)
            x.start()

    for t in threads:
        t.join()

    mycon += 50

    if mycon > len(synlist):
        break

print "Exiting the main thread.. Time " + str(time.time()-t0) + '\n'
print "Finising the heavy import... \n"
print 'Failure checking... \n'

#-------------hitting until its defeated--------------
userpromt=0

while 3==3:
    #break #take it out man
    userpromt += 1
    if userpromt > 2:
        print "\nsome data are really stubborn to pull out\n"
        print "Bot is feeling dizzy...\n"
        get = raw_input("Do you want to break the loop [Yes/No]... ")
        get =get.lower()
        if get.startswith("y"):
            break
        
    print "Start filtering data...\n"
    print "Starting... \n"
    psynlist=[]
    gsynlist=[]
    filterlist=[]
    print "Deleting the files...\n"
    try:
        if os.path.isfile('IMSP.txt'):
            os.remove('IMSP.txt')
    except IOError as e:
        print "IMSP file does not exist\n"
    try:
        if os.path.isfile('IMSG.txt'):
            os.remove('IMSG.txt')
    except IOError as e:
        print "IMSG file does not exist\n"
    try:
        if os.path.isfile('IMSM.txt'):
            os.remove('IMSM.txt')
    except IOError as e:
        print "IMSM file does not exist\n"
        
    fop=open('IMSP.txt','ab')
    fog=open('IMSG.txt','ab')
    fom=open('IMSM.txt','ab')
    print "Opening the files...\n"

    for pline in fileinput.input(['IMSdataSAP.txt']):
        psynid =pline.split(';')
        if len(psynid[0].strip()) >0 :
            psynlist.append(psynid[0])
            fop.write(psynid[0] + '\n')


    fop.close()
    print 'Listed persons synids... '+  str(len(psynlist)) + '\n'

    for gline in fileinput.input(['group.txt']):
        gsynid =gline.split(';')
        if len(gsynid[0].strip()) > 0 :
            if (gsynid[0].lower().find('warning') == -1) and (gsynid[0].lower().find('stack') == -1) and (gsynid[0].lower().find('timememoryfunctionlocation') == -1) and (gsynid[0].lower().find('main') == -1):
                gsynlist.append(gsynid[0])
                fog.write(gsynid[0] + '\n')

    fog.close()
    print 'listed successfull synids...(included junks too) ' + str(len(gsynlist)) + '\n'
    print '\n--------------------------------\n'

    diff = list(set(psynlist) - set(gsynlist))
    print 'Printing filtered bulk....\n'
    print "Found some data losses...\n"
    print diff
    print '\n'

    for mlist in diff:
        if len(mlist.strip()) >0:
            if mlist.find("itsla") == -1 and mlist.find('#') == -1:
                print "lost data synid - " +  mlist + '\n'
                filterlist.append(mlist)
            fom.write(mlist + ';' + '\r\n')
    fom.close()

    print "Measuring the lost data size " + str(len(filterlist)) + '\n'
    if len(filterlist) == 0:
        print'----- breaking out the main loop in filtering process---\n'
        print 'hooha exiting the automation bot...\n'
        break

    filterthreads=[]
    counting =0
    

    while 1==1:
        print '\n' + str(counting) + ' -Starting new bulk... \n'
        fi=0
        for filteritem in filterlist:
            fi += 1
            if fi >= counting and fi < counting+50:
                fx = myThread(filteritem)
                filterthreads.append(fx)
                fx.start()

        for ft in filterthreads:
            ft.join()

        counting +=50

        if counting > len(filterlist):
            break

        print "\nleaving threads...\n"
        
        

print "\nExiting the filter threads... Time " + str(time.time()-t0) + '\n'
print '\nstart eliminating process....\n'
print '\nVery customized for Katedralskolan....\n'
biglist=[]
fo=open("groupeliminate.txt","ab")
for line in fileinput.input(["group.txt"]):
    synid = line.split(';')
    if len(synid[0])>=0:
        if len(synid) > 2:
            if synid[2] == 'Katedralskolan':
                fo.write(';'.join(synid[0:]))
            else:
                darpul=synid[0] + ';' + synid[1]
                chk=1
                for item in synid:
                    item = item.replace('#','')
                    item = item.replace("\r","")
                    item = item.replace("\n","")
                    if item == 'Katedralskolan':
                        chk = 3
                    else:
                        print item + ' not in the list '+ '\n'
                    if chk == 3:
                        darpul += ';' + item
                        print 'Adding \n'
                darpul += '#'
                fo.write(darpul +  '\r\n' )   

fo.close()
print '\nFinishing the eliminating process....\n'

print '\n\nfinalizing.....\n\n'
print '\n\nmerging txts....\n\n'
print 'matix...\n'
time.sleep(2)
synlist={}
gsynlist={}
biglist=[]
fo=open("IMS.txt","ab")
for line in fileinput.input(["IMSdataSAP.txt"]):
    synid = line.split(';')
    if len(synid[0])>0:
        synlist[synid[0]] = synid[1:]
        #fo.write(';'.join(synlist[synid[0]]))
        #synlist.append(synid[0])
        #print synid[0] + "\n"        
#fo.close()
print synlist

for gline in fileinput.input(["groupeliminate.txt"]):
    gsynid = gline.split(';')
    if len(gsynid[0])>0:
        gsynlist[gsynid[0]] = gsynid[1:]

print gsynlist


for key in synlist:
    chk =1
    for gkey in gsynlist:
        if key == gkey:
            biglist.append(key + ";" + ';'.join(synlist[key])  + ';'.join(gsynlist[key]))
            chk=3
    if chk == 1:
        biglist.append(key + ";" + ';'.join(synlist[key]) )

#print biglist

for milo in biglist:
    print milo + '\n'
    milo = milo.replace("\r","")
    milo = milo.replace("\n","")
    milo = milo.replace("#","")
    fo.write(milo + '\r\n')

fo.close()

print "\n\nfinalizing the whole process.... \n\n"
print "\nTerminating.... \n"
print "\nTotal Time.... " + str(time.time()-t0)
print "\nSending mail..."
time.sleep(1)
filename = "IMS.txt"

# Read a file and encode it into base64 format
fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)  # base64

sender = 'saran_save@yahoo.com'
reciever = 'sarangan12@gmail.com'

marker = "AUNIQUEMARKER"

body ="""
This is an automated email to send an attachement of IMS import.
"""
# Define the main headers.
part1 = """From: From IMSBot <saran_save@yahoo.com>
To: To saran <sarangan12@gmail.com>
Subject: IMS import
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)
message = part1 + part2 + part3

smtpObj = smtplib.SMTP('smtp.mail.yahoo.com',587)
smtpObj.ehlo()
#smtpObj.starttls()
smtpObj.login("saran_save@yahoo.com","chandraamma")
smtpObj.sendmail(sender, reciever, message)
smtpObj.quit()
print "\nSuccessfully sent email\n"
print "\n\nsee you...\n\n"
            
        
        


    
