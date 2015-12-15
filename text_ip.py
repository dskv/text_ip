#!/usr/bin/python
"""

Author: Dan Kay
This repo is located at: https://github.com/dskv/
Sends current internal and external IP on boot to your phone SMS/Text message. Works with wireless.

"""

from googlevoice import Voice
import re
import os
import subprocess
import urllib
import sys


v = Voice()

def main():
	ver = get_os()
	int_ip = get_internal_ip(ver)
	ext_ip = get_external_ip()
	text = 'Raspberry Pi: \n\n' + 'Internal: ' + int_ip + '\n' + 'External: ' + ext_ip 
	print text
	send_text(text)

def get_os():
	# Determine which OS distribution the system is running
	version = os.uname()[0]
	return version

def get_internal_ip(version):
	if version == 'Darwin': #I cant test for Darwin, edits might need to be made here
		int_ip = subprocess.check_output(['/sbin/ifconfig','en0'])
		int_ip = re.search('inet ([\d\.]*)', int_ip)
	else:
		int_ip = 'none'	

	if version == 'Linux':
		int_ip = subprocess.check_output(['/sbin/ifconfig','wlan0'])
		int_ip = re.search('inet addr:([\d\.]*)', int_ip)
		if int_ip:
			int_ip = int_ip.group(1)
		else:
			print 'No wireless connection, trying LAN connection.'
			int_ip = subprocess.check_output(['/sbin/ifconfig','eth0'])
			int_ip = re.search('inet addr:([\d\.]*)', int_ip)		
			int_ip = int_ip.group(1)
	else:
		int_ip = 'none'
	
	return int_ip

def get_external_ip():
	url = 'http://myexternalip.com/raw'
	#do a bit of error handling if you are only working on Internal LAN connection
	try:
		ext_ip = urllib.urlopen(url).read()
	except IOError:
		print 'External URL IOError error.'
		ext_ip = 'NONE'
	except:
		print 'External URL except error.'
		ext_ip = 'NONE'
	return ext_ip	

def send_text(text):
	# Reads a file 'user_info.txt' that you create with your login information. Of course you can ass your information directly here.
	# example user_info.txt file:
	# USERID@gmail.com
	# YOUR_PASSWORD
	# 01234567890
	try:	#do a bit of error handling for people that dont read the README files
		user_info = open('/home/pi/Desktop/text_ip/user_info.txt', 'r')
	except:
		print 'No user_info.txt\n'
		print 'Create user_info.txt file and add the user info:'
		print 'USERID@gmail.com'
		print 'YOURPASSWORD'
		print 'TELEPHONE#\n'
		sys.exit('Unable to get loging information. Scrypt exited')
		
	user_name = user_info.readline() #read line one
	user_pass = user_info.readline() #read line two
	user_tele = user_info.readline() #read line three
	user_info.close()
	v.login(user_name, user_pass)
	v.send_sms(user_tele, text)
	v.logout()

if __name__ == "__main__": main()