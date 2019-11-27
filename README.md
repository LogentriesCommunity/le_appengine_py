Logging To Logentries from Google AppEngine using Python
========================================================

*This plug in will no longer be officially supported or maintained by Logentries.<br>*

Logentries currently provides 3 methods of logging to our servers.

In-Process Logging, Push-Queue Logging and Pull-Queue Logging.

--------------------------------------------------------------

In-Process Logging may have a performance impact and is advised for development only. 
It is limited by App Engine's urlfetch api quotas. (1 api call per log)
 
Push-Queue Logging has minimal impact on performance and is advised for low log volume 
production systems, however it too is limited by App Engine's push-queue quotas. 
This method is suitable for a system logging no more than 100,000 logs a day using a 
free account or 20,000,000 logs a day using a paid account.

Pull-Queue Logging has no impact on performance and is advised for high log volume 
production systems. It is not limited by App Engine quotas and is suited to systems
that expect high logging volumes.

-----------------------------------------------------------------------------------

Before implementing your chosen option, you need to create an account on Logentries. Once you have done this,
you will need to obtain your account-key which is necessary for each of the configrations below.

This is achieved by clicking Account in the top left corner of the Logentries UI and display account-key on the right.

You can set up a host and log file on Logentries via the UI:

In-Process Logging
------------------

To Enable In-Process logging in your app, you must add logentries.py to your directoy, it is available on here
at  
	https://github.com/logentries/le_appengine_py/raw/master/Downloads/In-Process.zip

Now if you don't already have an appengine_config.py simply create one in your app's directory.

Add the following lines to this config file:

	import logentries

	logentries.init('LOGENTRIES_ACCOUNT_KEY', 'LOGENTRIES_LOCATION')

You will notice the two parameters above called key and location.

  - Account-Key is your unique account-key to the site and must be kept secret. As mentioned earlier this key is
  obtained from the Logentries UI.
  
  - Location is the name of your host on logentries followed by the name of the log, e.g 'hostname/logname'
  Running `python register.py` will set up the following default   `AppEngine/AppEngine.log` 

For example:  

            logging.info("informational message")
            logging.warn("warning message")
            logging.crit("critical message")

Push-Queue Logging
------------------

To Enable Push-Queue logging in your app, you must add logentries.py to your app's directory,  
It is available at  
	https://github.com/logentries/le_appengine_py/raw/master/Downloads/Push-Queue.zip

In your app.yaml, add the following section under handlers:

	- url: /logentriesworker
  	  script: logentries.py

Add the follwoing to your WSGIApplication url mapping:

	('/logentriesworker', logentries.LogentriesWorker)

If you don't already have an appengine_config.py file in your app, simplys create a new file by that name.

In this file add the following lines:

         import logentries
         
         logentries.init('LOGENTRIES_ACCOUNT_KEY', 'LOGENTRIES_LOCATION')

You will notice the two parameters above called key and location.

  - Account-Key is your unique account-key to the site and must be kept secret. As mentioned earlier this key is
  obtained from the Logentries UI.
  
  - Location is the name of your host on logentries followed by the name of the log, e.g 'hostname/logname'
  Running `python register.py` will set up the following default   `AppEngine/AppEngine.log`  

Create a file called queue.yaml if you don't already have one and enter the following lines:

	queue:
	- name: logentries-push-queue
  	  rate: 5/s
  	  retry_parameters:
    	    task_retry_limit: 1
    	    task_age_limit: 10s
  
Once this is done properly, simply import logging in the files you wish to log from and use the python 
logging module as normal for it to log to Logentries also.

For example:  

            logging.info("informational message")
            logging.warn("warning message")
            logging.crit("critical message")


Pull-Queue Logging
------------------

To Enable Pull-Queue Logging on your app, you must add 2 files to your app's directory,  
logentriesbackend.py and logentries.py available at  
	https://github.com/logentries/le_appengine_py/raw/master/Downloads/Pull-Queue.zip

If you don't already have an appengine_config.py file in your app, simply create a new file by that name.

In this file add the following lines:

         import logentries
         
         logentries.init('LOGENTRIES_ACCOUNT_KEY', 'LOGENTRIES_LOCATION')

You will notice the two parameters above called key and location.

  - Account-Key is your unique account-key to the site and must be kept secret. As mentioned earlier this key is
  obtained from the Logentries UI.
  
  - Location is the name of your host on logentries followed by the name of the log, e.g 'hostname/logname'
  Running `python register.py` will set up the following default   `AppEngine/AppEngine.log` 

Create a file called backends.yaml with the following contents:

         backends:
         - name: logentriesworker
           class: B1
           instances: 1
           start: logentriesbackend.py


Create a file called queue.yaml with the following contents:

        queue:
        - name: logentries-pull-queue
          mode: pull
          acl:
          - user_email: "put_your_email_here"
  

Once this is done properly, simply import logging in the files you wish to log from and use the python 
logging module as normal for it to log to Logentries also.

For example:  

            logging.info("informational message")
            logging.warn("warning message")
            logging.crit("critical message")
