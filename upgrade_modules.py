#!/usr/bin/env python
"""
A Python script to upgrade all install Python modules
Coded by Steve Moss (gawbul [at] gmail [dot] com)
http://about.me/gawbul
"""

# import required modules
from pip.util import get_installed_distributions
import xmlrpclib

# setup pypi xmlrpc proxy
pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

# traverse installed distributions
for dist in get_installed_distributions(local_only=True):
	# check for available packages
	available = pypi.package_releases(dist.project_name)
	# check by capitalising pkg name, if not found in first instance
	if not available:
		available = pypi.package_releases(dist.project_name.capitalize())
	# check by converting to lowercase
	if not available:
		available = pypi.package_releases(dist.project_name.capitalize())
	
	# if still not available then let user know no release
	if not available:
		msg = 'no releases at pypi'
	# if release versions are different then report as available
	elif available[0] >= dist.version:
		msg = '{} available'.format(available[0])
	# otherwise report as up to date
	else:
		msg = 'up to date'

	# build pkg_info string
	pkg_info = '{dist.project_name} => {dist.version}'.format(dist=dist)
	
	# print formatted display
	print '{pkg_info:40} {msg}'.format(pkg_info=pkg_info, msg=msg)