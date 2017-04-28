#!/usr/bin/python2

#import os
import subprocess
import smtplib
from email.mime.text import MIMEText
import emailsettings
from emailsettings import *


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
                    packageinfo = int(round(((float(spl[3]) / 1024) / 1024), 1))
                    message = "\n Quota for user "+spl[0]+" is "+str(limitinfo)+" Gb ("+str(percent)+" %) and disk limit can be overloaded. The disk qouta of this package is "+str(packageinfo)+" Gb\n\n Please contact with Hosting support to increase your limit or clear your backups"
                    print(message)

                    msg = MIMEText(message)
                    msg['Subject'] = 'Limit for backup user %s in %s' % (spl[0], BKPSERVERNAME)
                    msg['From'] = EMAILFROM
                    msg['To'] = EMAILTO
                    
                    # Send the message via our own SMTP server, but don't include the
                    # envelope header.
                    s = smtplib.SMTP('localhost')
                    s.sendmail(msg['From'], msg['To'], msg.as_string())
                    s.quit()

        except:
            spl = None
    marker = marker + 1
