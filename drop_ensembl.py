#!/usr/bin/env python

'''
drop_ensembl.py
A script to drop the previous EnsEMBL release MySQL data from your local SQL server
Coded by Steve Moss
gawbul@gmail.com
27th February 2012
'''

# imports
from time import time, strftime
import getpass
import os, sys, shutil
import MySQLdb
from colorama import Fore, Style, init
init(autoreset=True) # automatically reset colorama styles etc

# setup some variables
# variables for MySQL connection
sql_host = 'localhost'
sql_port = '3306'
sql_user = 'root'
sql_pass = getpass.getpass(Fore.CYAN + Style.BRIGHT + "\nPlease enter your MySQL password:" + Fore.RESET)

# not remove list
na_dbs = ("information_schema", "mysql", "performance_schema", "test", "wikidb", "wordpress")

# other variables
data_dir = '/Volumes/DATA/current_mysql'

# start time
start_time = time()

'''
DATA dir removal stuff here
'''
print Style.BRIGHT + "\nRemoving DATA directory file listings...\n"

# get all files in folder and remove them
for file in os.listdir(data_dir):
	path = os.path.join(data_dir, file)
	if os.path.isfile(path):
		os.unlink(path)
	else:
		shutil.rmtree(path)

"""
MySQL data drop here
"""
print Style.BRIGHT + "\nDeleteing MySQL databases...\n"

# connect to database
connection = MySQLdb.connect(host=sql_host, port=int(sql_port), user=sql_user, passwd=sql_pass)
cursor = connection.cursor()
cursor.execute("SHOW DATABASES;")
databases = cursor.fetchall()
# iterate over databases and drop in turn
for db in databases:
	# make sure don't remove databases we want to keep
	if not db[0] in na_dbs:
		cursor.execute("DROP DATABASE IF EXISTS " + db[0])
		print "Dropped %s" % db[0]
cursor.close()
	
# end time
end_time = time()

# calculate time taken
total_time = end_time - start_time
days, remainder = divmod(total_time, 86400)
hours, remainder = divmod(remainder, 3600)
minutes, seconds = divmod(remainder, 60)
print Fore.YELLOW + Style.BRIGHT + 'Finished in: %d days %d hrs %d mins %d secs' % (days, hours, minutes, seconds)