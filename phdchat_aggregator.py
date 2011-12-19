"""
	PhDChat Tweet Aggregator
	Catches tweets with the #phdchat hash tag
	Coded by Steve Moss (@gawbul)
	Email: gawbul@gmail.com
	Web: http://stevemoss.ath.cx
"""

# ToDo:
# 1) Get today's tweets only
# 2) Ensure new Twitter error mechanism isn't breaking any of the results

# import modules required
from twython import Twython
import httplib2
import socks
from datetime import date, timedelta
import time
import re, sys, os, unicodedata
import paramiko

# setup the API
twitter = Twython(
	# need this to pass through the university proxy
	client_args			= {'proxy_info': httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP_NO_TUNNEL, 'slb-webcache.hull.ac.uk', 3128)},
)

# setup unicode filter
# this was the old way of filtering unicode chars
#unicode_chars = ''.join([u'\u201c', u'\u2019', u'\u2026', u'\u201d', u'\u25b8', u'\u2013', u'\u2018', u'\xa0', u'\xab', u'\xe9', u'\u0646', u'\u0635', u'\u0627', u'\u0626', u'\u062d', u'\u0648', u'\u062a', u'\u0628', u'\u062f', u'\u0644', u'\xe8'])
# new method seems to work so far
unicode_chars = ''.join(map(unichr, range(128,65535)))
unicode_chars_re = re.compile('[%s]' % re.escape(unicode_chars))


# setup link identification
# this recognises urls in the tweets
pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\f]+]*)?)", re.IGNORECASE | re.DOTALL)
pat2 = re.compile(r"#(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)

# setup the variables we need
tweet_list = []
page_num = 1

# set output filename based on date
today = date.today()
today = today.strftime("%d%m%y")
output_file = "phdchat_tweets_%s.html" % today

# set yesterdays date
# use this for getting tweets from today only
yesterday = date.today() - timedelta(1)
yesterday = yesterday.strftime("%Y-%m-%d")

# get the last tweet from yesterday, so we can get all the tweets from today only
# *** need to fix this ***
#search_results = twitter.searchTwitter(q="#phdchat", page="1", until=yesterday)
#since_id = search_results["results"][0]["id"]

# get tweets
print "Retrieving tweets..."
count = 0
next_page = 1
while next_page:
	# get search results
	# see https://dev.twitter.com/doc/get/search for query information
	search_results = twitter.searchTwitter(q="#phdchat", rpp="100", page=str(page_num))#, since_id=str(since_id))

	# simple way of catching end of all tweets
	try:
		search_results["next_page"]
	except:
		next_page = 0
	
	# get search results keys
	# print search_results.keys() gives us:
	# [u'next_page', u'completed_in', u'max_id_str', u'since_id_str', u'refresh_url', u'results', u'since_id', u'results_per_page', u'query', u'max_id', u'page']
	try:
		search_results["error"]
		next_page = 0
	except:
		results = search_results["results"]

	# get results keys
	# print results[0].keys() gives us:
	# [u'iso_language_code', u'to_user_id_str', u'text', u'from_user_id_str', u'profile_image_url', u'id', u'to_user', u'source', u'id_str', u'from_user', u'from_user_id', u'to_user_id', u'geo', u'created_at', u'metadata']
	
	#for key,value in results[0].iteritems():
	#	print str(key) + ": " + str(value)
	
	for result in results:
		# pull out values into variables
		# replace links with html code
		# turn some items into hyperlinks
		from_user = result["from_user"]
		user_link = "https://twitter.com/#!/" + from_user + "/"
		text = result["text"]
		text = unicode_chars_re.sub('', text)
		text = pat1.sub(r'\1<a href="\2" target="_blank">\2</a>', text)
		text = pat2.sub(r'\1<a href="http:/\2" target="_blank">\2</a>', text)
		text = re.sub("#phdchat", "<A HREF=\"https://twitter.com/#!/search/#phdchat\" target=\"_blank\">#phdchat</A>", text)
		tweet_id = result["id"]
		tweet_link = "https://twitter.com/#!/" + from_user + "/status/" + str(tweet_id)

		# remove any retweets (remove exact duplicates)
		if re.match("^RT.*?", text):
			continue
		
		# add html formatted tweet to tweet list for output later
		#tweet_list.append('<P>' + str(count + 1) + ': <A HREF=' + user_link + ' TARGET=_blank>@' + from_user + '</A> - ' + text + ' <A HREF=' + tweet_link + ' TARGET=_blank>' + tweet_link + '</A></P>')
		tweet_list.append('<P><A HREF=' + user_link + ' TARGET=_blank>@' + from_user + '</A> - ' + text + '</P>')
		
		# increment post count
		count += 1
	
	# increment page number
	page_num +=1

# reverse all the tweets, so they are in chronological order
tweet_list.reverse()

# open file for writing
output_path =  os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), output_file)
outfile = open(output_path, "w")

# write the html header
outfile.write("<HTML><HEAD>\n")
outfile.write("<TITLE>#phdchat tweets</TITLE></HEAD>")
outfile.write("<BODY><FONT FACE=Tahoma><H1>#phdchat tweets:</H1>")

# iterate through and write to the file
for tweet in tweet_list:
	try:
		outfile.write(str(tweet) + "\n")
	except Exception as e:
		print e
		#print re.escape(tweet)
		print tweet.encode('utf-16')
		
# write the html footer
outfile.write("<H3>" + str(count) + " tweets</H3>")
outfile.write("</FONT></BODY></HTML>")

# close the file
outfile.close()

# let user know how many tweets we have and what filename
print "Outputted %d tweets to %s" % (count, output_file)

# connect to SFTP and upload file
try:
	host = "freeside.co.uk"
	port = 22
	transport = paramiko.Transport((host, port))
	username = "removed"
	password = "removed"
	transport.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(transport)
	localpath = output_path
	remotepath = '/var/www/gawbul/phdchat/%s' % output_file
	# let user know it's going
	print "Uploading %s to %s..." % (output_file, host)
	sftp.put(localpath,remotepath)
	sftp.close()
	transport.close()
except:
	print "Failed to upload the file"
	sys.exit()
	
print "Uploaded to %s on %s" % (remotepath, host)