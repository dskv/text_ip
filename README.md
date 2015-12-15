text_ip
======

Send a sms/text message using google voice to your phone when device (raspberry pi) boots and is assigned an ip address.

The scrypt uses Google voice, so go set that up if you need to at www.google.com/voice

To have the scrypt run automatically on boot add following command:
	sudo nano /etc/rc.local
	
edit the rc.local file

\#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
  python /home/pi/Desktop/sms_ip/get_ip.py 	#<--ADD THIS LINE
fi
exit 0



Also dont forget to edit the 'user_info.txt' file with your personal information


Errors:

gVoice needs to be installed, do the following if errors come up.

#Command line Google Voice:

#required tools:
sudo apt-get install python python-simplejson python-setuptools
sudo easy_install simplejson

# if gvoice was installed previously, then uninstall it:
sudo rm -r /usr/local/lib/python2.7/dist-packages/googlevoice
sudo rm /usr/local/lib/python2.7/dist-packages/pygooglevoice*

#download pygooglevoice:
wget http://pygooglevoice.googlecode.com/files/pygooglevoice-0.5.tar.gz
tar -xf pygooglevoice-0.5.tar.gz
cd pygooglevoice

# edit settings.py to match correct Google Voice URL on line # 22:
nano googlevoice/settings.py

#correct URL:
LOGIN = 'https://accounts.google.com/ServiceLogin?service=grandcentral'
#you may check if URL is linking to Google Voice login page in browser.
#save and quit settings.py

#install gvoice:
sudo python setup.py install

#Login and make call for the first time:
gvoice # enter login email/pwd
  gvoice> call #follow prompts and make a call
  gvoice>send_sms # or s to send sms
  gvoice>exit #quit gvoice
#end