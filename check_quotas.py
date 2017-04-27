#!/usr/bin/python2

#import os
import subprocess


PIPE=subprocess.PIPE
p = subprocess.Popen('repquota  -u /home', shell=True, stdout=PIPE, stderr=subprocess.STDOUT)

info =  p.stdout.read()
print info

allstring = info.split('\n')
n = list(allstring)

marker = 1

for i in n:
    if marker > 5:
#        print(marker)
#        r=i.replace(' ',' ')
        spl = i.split()
        try:
            spl
            if spl[3] != "0":
                print(spl[0],spl[2],spl[3])
                percent = int(round((float(spl[2]) / float(spl[3])) * 100))
                print('percent = '+str(percent)+' %')
                if percent > 90:
                    limitinfo = round(((float(spl[2]) / 1024) / 1024), 2)
#                    print('limitinfo = '+str(limitinfo)+' Gb')
                    print("quota for user "+spl[0]+" exceeded "+str(limitinfo)+" Gb ("+str(percent)+" %) and disk limit can be overloaded. Please contact with Hosting support to increase your limit or clear your backups")
        except:
            spl = None
    marker = marker + 1
