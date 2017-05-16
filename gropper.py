# -*- coding: utf-8 -*-
import fileinput
import os
import sys
import re

ins = open("S_KAT.txt", "r" )
#for mline in fileinput.input(['schools.txt']):

#synlist=[]
fop=open('grops.txt','ab')
group=[]

for mline in ins:
    groupids=[]
    data = mline.split(';')
    groupids = data[9:]
    #print groupids

    for groupid in groupids:
        groupid = groupid.strip()
        groupid = groupid.replace(',','')
        groupid = groupid.replace('\n','')
        groupid = groupid.replace('\r','')
        #print groupid

        if len(group) == 0:
            group.append(groupid)
            fop.write(groupid +';'+ '10'+ ';'+ groupid +';' +'\n')
        else:
            x = 1
            for gr in group:
                if gr == groupid:
                    print groupid + " already exits\n"
                    x = 3

            if x == 1:
                print groupid + " adding...\n"
                group.append(groupid)
                fop.write(groupid +';'+ '10'+ ';'+ groupid +';' +'\n')
fop.close()
