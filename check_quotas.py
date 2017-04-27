#!/usr/bin/python2

#import os
import subprocess


PIPE=subprocess.PIPE
p = subprocess.Popen('repquota  -u /home', shell=True, stdout=PIPE, stderr=subprocess.STDOUT)

info =  p.stdout.read()
print info

allstring = info.split('\n')
n = list(allstring)

#print(n)
marker = 1

for i in n:
    if marker > 5:
        print(marker)
#        print(i)
#        r=i.replace(' ',' ')
        spl = i.split()
        try:
            spl
            if spl[3] != "0":
                print(spl[0],spl[2],spl[3])
                percent = int(round((float(spl[2]) / float(spl[3])) * 100))
                print('percent = '+str(percent)+' %')
        except:
            spl = None
    marker = marker + 1
