#!/usr/bin/env python
# coding: utf-8

#
# Logentries Python monitoring agent
# Copyright 2010,2011 Logentries, Jlizard
# Mark Lacomber <marklacomber@gmail.com>
#

VERSION = "1.0"

LE_SERVER = 'logentries.com'
LE_SERVER_API = 'api.logentries.com'
LE_SERVER_PORT = 443
USER_KEY_API = '/agent/user-key/'

import urllib, httplib, getpass, sys

def die(cause, exit_code=0):
   print cause
   sys.exit(exit_code)

try:
	import ssl
except ImportError: die( 'NOTE: Please install Python "SSL" module')

try:
  	import json
except ImportError:
	try: 
		import simplejson 
        except ImportError: die( 'NOTE: Please install Python "simplejson" package (python-simplejson) or a newer Python (2.6).')

def obtainKey():
	username = raw_input('Username: ')
	password = getpass.getpass()

	http = httplib.HTTPSConnection(LE_SERVER, LE_SERVER_PORT)

	http.request( 'POST', USER_KEY_API, urllib.urlencode( {'username':username, 'password':password}),
		{'Referer':'https://logentries.com/login/'})

	resp = http.getresponse()

	if resp.reason != "OK":
		die("Incorrect Login Details. Please Try Again")

	try:
		data = json.loads(resp.read())
	except AttributeError:
		data = simplejson.loads(resp.read())

	print data['user_key']

	http.close()


def register(host = 'AppEngine', fileName = 'AppEngine.log'):

	username = raw_input('Username: ')
	password = getpass.getpass()

	http = httplib.HTTPSConnection(LE_SERVER, LE_SERVER_PORT)

	http.request( 'POST', USER_KEY_API, urllib.urlencode( {'username':username, 'password':password}),
		{'Referer':'https://logentries.com/login/'})

	resp = http.getresponse()

	if resp.reason != "OK":
		die("Incorrect Login Details. Please Try Again")

	try:
		data = json.loads(resp.read())
	except AttributeError:
		data = simplejson.loads(resp.read())

	user_key = data['user_key']
	
	http.close()

	http = httplib.HTTPSConnection(LE_SERVER_API, LE_SERVER_PORT)

	request = "distver=hero&name=%s&distname=Debian&hostname=AppEngine&request=register&system=Linux&user_key=%s" %(host, user_key)

	http.request('POST', '/', request)

	resp = http.getresponse()

	try:
		data = json.loads(resp.read())
	except AttributeError:
		data = simplejson.loads(resp.read())

	host_key = data['host_key']

	full = "host_key=%s&name=%s&user_key=%s&request=new_log&filename=%s&follow=true&type=""" %(host_key, fileName, user_key, fileName)

	http.request('POST', '/', full)

	resp = http.getresponse()

	if resp.reason != "OK":
		die("Incorrect Details. Please Try Again")

	print resp.reason

	print "Successfully Created Host %s and Log %s" %(host, fileName)
	print "Enter the following format as location in your config file:  '%s/%s'" %(host, fileName) 


def printUsage():
	print "\nUsage: python getKey.py [options] <parameter(s)>"
	print "\nOptions:\t--key\t\t\t\tRetrieve user key"
	print "          \t--register <parameter(s)>\tCreate Host and LogFile on Logentries"
	print "		--help\t\t\t\tShow the current screen"
	print "\nParameters for  --register:"
	print "\t\t\t-h Host(Optional)\tName of Host to be created, else Default Host 'AppEngine' will be used"
	print "\t\t\t-l Log(Optional)\tName of Log to be created, else Default Log 'AppEngine.log' will be used"
	sys.exit(0)


def main():

	if len(sys.argv) < 2:
		printUsage()
	elif len(sys.argv) == 2:
		if sys.argv[1] == "--key":
			obtainKey()
		elif sys.argv[1] == "--register":
			register()
		elif sys.argv[1] == "--help" or sys.argv[1] == "help":
			printUsage()
		else:
			printUsage()
	elif len(sys.argv) == 3:
		printUsage()
	elif len(sys.argv) == 4:
		if sys.argv[2] == "-h":
			register(sys.argv[3], 'AppEngine.log')
		elif sys.argv[2] == "-l":
			register('AppEngine', sys.argv[3])
		else:
			printUsage()
	elif len(sys.argv) == 5:
		printUsage()
	elif len(sys.argv) == 6:
		if sys.argv[2] == "-h" and sys.argv[4] == "-l":
			register(sys.argv[3], sys.argv[5])
		elif sys.argv[2] == "-l" and sys.argv[4] == "-h":
			register(sys.argv[5], sys.argv[3])
		else:
			printUsage()
	else:
		printUsage() 



if __name__ == '__main__':
	main()








