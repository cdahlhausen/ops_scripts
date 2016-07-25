#!/usr/bin/env python

# Please don't judge this code. It's not good I know.
# I ignored PEP8 for this.
import smtplib
import os
import socket
import statvfs
import sys
from time import localtime, strftime

#Get servers hostname
SRV = str(socket.gethostname())

# Mail CONFIGURATION
SERVER = "localhost"
PORT = '25' # If left blank port 25 is assumed.
SEND_FROM = "ops@aptrust.org"
SEND_TO = "ops@aptrust.org"

# Locations to monitor
MON0='/'
#MON1=''
#MON2=''
MON_ARRAY = (MON0)
# Limit in MiB
LIMIT=2000;
# END OF CONFIG

#Define current Time as Fri, 04 Mar 2011 08:47:10
TIME = strftime("%a, %d %b %Y %H:%M:%S", localtime())


for disk in MON_ARRAY:
	MONITOR = os.statvfs(str(disk))
	SPACE_LEFT=(MONITOR.f_bavail * MONITOR.f_frsize) / 1048576 #MiB

	if (SPACE_LEFT < LIMIT):
		STATUS = "- is NOT OK on "
		MSG = ("{}  {} has only {}MB left on {}").format(TIME, SRV, SPACE_LEFT,disk)
		smtpserver = smtplib.SMTP(SERVER, PORT)
		smtpserver.ehlo(SRV)

		# Uncomment smtpserver.starttls if server using TLS
#		smtpserver.starttls()
		# Uncomment smtpserver.login() if login is required
		#smtpserver.login('', '')

		HEADER = 'To:' + str(SEND_TO) + '\n' + 'From: ' + str(SEND_FROM) + '\n' + 'Subject:Alert - Low disk space on ' + SRV + '\n'
		MAIL = HEADER + str(MSG)

		smtpserver.sendmail(SEND_FROM, SEND_TO, MAIL)
		smtpserver.close()

	elif (SPACE_LEFT > LIMIT):
		sys.exit(0)
	else:
		print """
		A serious problem detected with the script.
		Please check what mount points you monitor and check that
		they are in the MON_ARRAY aswell.
		"""
