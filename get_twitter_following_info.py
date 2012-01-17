# imports
import sys, os, time
import twitter

##############################################################
# ToDo: Fix progress file and twitter ids file unsync issues #
##############################################################

# set start time
start_time = time.time()

# check args for auto unfollow (-a) any other stuff is ignored
auto_unfollow = 0
args = sys.argv[1:]
if "-a" in args:
	auto_unfollow = 1
else:
	auto_unfollow = 0

# create api instance
api = twitter.Api(	consumer_key='', 
			consumer_secret='', 
			access_token_key='', 
			access_token_secret='')

# verify credentials
try:
	verify_user = api.VerifyCredentials()
except:
	print "Couldn't verify the developer credentials"

# verified okay
print "%s (%s) verified" % (verify_user.name, verify_user.screen_name)

# set variables
date = time.time()
six_months = 15724800
three_months = six_months / 2
one_year = six_months * 2

# get list of ids im following
# if already go id list then use the file
if os.path.exists("twitter_ids.txt"):
	listfile = open("twitter_ids.txt", "r")
	user_ids = listfile.readlines()
	listfile.close()
else:
	# otherwise we retrieve them from twitter
	try:
		user_ids = api.GetFriendIDs(user="gawbul")["ids"]
		# write to file
		listfile = open("twitter_ids.txt", "w")
		for id in user_ids:
			listfile.write(str(id) + "\n")
		listfile.close()
	except:
		print "Couldn't retrieve Twitter following IDs"

# let user know how many we retrieved
print "Retrieved %s user IDs" % len(user_ids)

# check if this is a new run or if we have a progress file
if os.path.exists("progress_id.txt"):
	progressfile = open("progress_id.txt", "r")
	progress = progressfile.readline().strip()
	progressfile.close()
else:
	progress = 1

# traverse user ids
count = 1
total = len(user_ids)
for id in user_ids:
	# which id
	print "[%s %s of %s]\r" % (id, count, total),
	# check if we have already started
	if count < progress:
		count += 1
		continue
	# get user object
	try:
		user = api.GetUser(id)
	except:
		print "Error at [%s %s of %s]\r" % (id, count, total),
		# save state
		progressfile = open("progress_id.txt", "w")
		progressfile.write(str(count) + "\n")
		progressfile.close()
		break
	# get latest tweet
	status = user.status
	# check status received okay - sometimes it doesn't (server load?)
	if not status:
		count += 1
		continue
	# check date of status
	status_date = status.created_at_in_seconds
	if status_date < (date - six_months):
		# print details to screen so we can unfollow them manually if auto unfollow not set
		print "User %s (%s) with id %s last tweeted at %s" % (user.name, user.screen_name, user.id, status.created_at)
		if auto_unfollow:
			# unfollow user
			api.DestroyFriendship(user.id)
		else:
			pass
	count += 1

# how many removed?
total_removed = count - progress

print "Removed %s friends" % total_removed
end_time = time.time()
total_time = end_time - start_time
print "Finished in %s seconds" % total_time