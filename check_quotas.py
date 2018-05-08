#!/usr/bin/python2

import os
import subprocess
import smtplib
import re
from email.mime.text import MIMEText
import emailsettings
from emailsettings import *

FILEPATH = os.path.dirname(os.path.realpath(__file__))

PIPE=subprocess.PIPE
p = subprocess.Popen('repquota  -u /home', shell=True, executable='/bin/bash', stdout=PIPE, stderr=subprocess.STDOUT)

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
                #print(spl[0],spl[2],spl[3])
                percent = int(round((float(spl[2]) / float(spl[3])) * 100))
                #print('percent = '+str(percent)+' %')
                if percent > 80:
                    limitinfo = round(((float(spl[2]) / 1024) / 1024), 2)
#                    print('limitinfo = '+str(limitinfo)+' Gb')
                    packageinfo = int(round(((float(spl[3]) / 1024) / 1024), 1))
                    quotauser = spl[0]
                    message = "\n Quota for user "+str(quotauser)+" is "+str(limitinfo)+" Gb ("+str(percent)+" %) and disk limit can be overloaded. The disk qouta of this package is "+str(packageinfo)+" Gb\n\n Please contact with Hosting support to increase your limit or clear your backups"
                    print("----------\n"+message+"\n----------\n")

                    msg = MIMEText(message)
                    msg['Subject'] = 'Limit for backup user %s in %s' % (spl[0], BKPSERVERNAME)
                    msg['From'] = EMAILFROM
                    msg['To'] = EMAILTO

                    # Send the message via our own SMTP server, but don't include the
                    # envelope header.
                    s = smtplib.SMTP('localhost')
                    s.sendmail(msg['From'], msg['To'], msg.as_string())
                    s.quit()

                    with open(USERSFILE) as f:
                        lines = f.readlines()
                        lines[1:-1]
                        for line in lines[1:-1]:
                            # prepare check_quotauser and userdomain for comparison
                            userspl = line.split("|")
                            user_firstname = userspl[4].strip()
                            userdomain = userspl[2].strip().lower().split(' ')[0]
                            package_name = userspl[7].strip()
                            user_email = userspl[3].strip()
                            #print(userdomain.lower(),userspl[3].strip(),userspl[4].strip(),userspl[7].strip())
                            check_quotauser = quotauser.replace("server.","")
                            #print('check user = %s, mcs_user = %s' % (check_quotauser, userdomain))
			    if "holbi" in userspl[3].strip():
                                continue

                            if check_quotauser == userdomain:
                                #print("33333333333!!!!!!!!!!!!!!!!!!")
                                messageopen = open(FILEPATH+'/mail_template.tpl','r').read()
                                messagetext = messageopen.format(V1 = MAIL_VALUE1, V2 = MAIL_VALUE2, V3 = MAIL_VALUE3, U1 = MAIL_URL1, U2 = MAIL_URL2, U3 = MAIL_URL3)
                                #print(messagetext)
                                #print("4444!!!!!!!!!!!!!!!!!!")
                                messagetext = re.sub('%s','{}',messagetext)
                                #messageuser = messagetext % (userspl[4].strip(), packageinfo, userspl[7].strip(), userdomain, percent)
                                messageuser = messagetext.format(user_firstname, packageinfo, package_name, userdomain, percent)
                                print("----------\n"+messageuser+"\n----------\n")
                                print("email = "+user_email)
                                msg_user = MIMEText(messageuser)
                                msg_user['Subject'] = '[{0}] Backup Warning: {1}'.format(MAIL_VALUE2,spl[0])
                                #user_email = 'test@test.com'
                                msg_user['To'] = user_email
                                msg_user['Bcc'] = EMAILTO
                                msg_toaddr = [ msg_user['To'], msg_user['Bcc'] ]
                                s_user = smtplib.SMTP('localhost')
                                s_user.sendmail(msg['From'], msg_toaddr, msg_user.as_string())
                                s_user.quit()
                                messageopen.close()
                                break
                    ## Send the message via our own SMTP server, but don't include the
                    ## envelope header.
                    #s = smtplib.SMTP('localhost')
                    #s.sendmail(msg['From'], msg['To'], msg.as_string())
                    #s.quit()
        except:
            spl = None
    marker = marker + 1
