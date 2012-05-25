# module imports
import urllib
import json
import sys
import time
import re

# setup RIL api key, username and password
ril_key = '' # change to your RIL key
ril_user = '' # change to your RIL username
ril_pass = '' # change to your RIL password
ril_get_url = 'https://readitlaterlist.com/v2/get'

# setup proxy support
proxy = {'https' : ''} # change to reflect your required proxy server address 
url_params = urllib.urlencode({'username':ril_user, 'password':ril_pass, 'apikey':ril_key, 'tags':1})
url_handle = urllib.urlopen(ril_get_url, url_params, proxies=proxy)

# get the json
if (url_handle.getcode() != 200):
	print "Error: Received return code %s" % url_handle.getcode()
	sys.exit()
else:
	print "Retrieving RIL data..."
	data = url_handle.read()

# dump data to file
filename = 'readitlater_list.txt'
filehandle = open(filename, "w")
filehandle.write(data + "\n")
filehandle.close()

# deserialise the json to a python dict
json_data = json.loads(data)

# check the json structure
#print json_data.keys()

# how many list items do we have?
print "Processed %d items" % len(json_data['list'].keys())

#******* check for duplicates *******#

# go through all list items and push title to array if state is unread
list_titles = []
list_ids = json_data['list'].keys()
for item in list_ids:
	item = item.decode('utf8')
	title = json_data['list'][item]['title']
	state = json_data['list'][item]['state']
	try:
		tags = json_data['list'][item]['tags']
	except:
		tags = ""
	list_titles.append(re.sub('[\W]+', '', title.lower()))
	#print (re.sub('[\W]+', '', title.lower()))
	if (title == ""):
		print json_data['list'][item]

# count all titles
count = 0
for title in list_titles:
	title_count = list_titles.count(title)
	if (title_count > 1):
		print "Found %s %d times" % (title, title_count)
		count += 1

print "Found %d duplicate items" % count
