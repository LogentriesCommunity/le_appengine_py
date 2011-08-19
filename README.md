Logging To Logentries from Google AppEngine using Python
========================================================

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
you will need to download the getKey.py script on github which is necessary for getting your user-key.
This user-key is required for each of the steps listed below and is referred to below simply as key.

Once you have downloaded the script run it as follows `python getKey.rb --key`.  It will prompt you for
your login credentials and then print out your user-key to be used below.

In-Process Logging
------------------

To Enable In-Process logging in your app, you must first import both logging and le in your main file for the app,
like so:

        import logging, le

and then add the following lines to your app's main definition in chosen main file:

        if len(logging.getLogger('').handlers) <= 1:
           logging.getLogger('').addHandler(le.InProcess(key, location))

You will notice the two parameters above called key and location.

  - Key is your unique password to the site and must be kept secret.
  - Location is the name of your host on logentries followed by the name of the log, e.g 'localhost/test.log'

Once this is done properly, you can use the python logging module as normal and it will log to Logentries also.
For example:  

            logging.info("informational message")
            logging.warn("warning message")
            logging.crit("critical message")

Push-Queue Logging
------------------

To Enable Push-Queue logging in your app, you must first import both logging and le in your main file for the app,
like so:

         import logging, le
         from google.appengine.api import urlfetch # urlfetch is also imported from appengine api

and then add the following lines to your main definition in the file:

         if len(logging.getLogger('').handlers) <= 1:
                logging.getLogger('').addHandler(le.PushQueue(key, location))

You will notice the two parameters above called key and location.

  - Key is your unique password to the site and must be kept secret.
  - Location is the name of your host on logentries followed by the name of the log, e.g 'localhost/test.log'

Then you must add the worker url which will handle the background logging.

In your app.yaml add:

         handlers:
         - url: /worker
           script: main.py
           login: admin 

'login: admin' ensures that the worker url can only be accessed by the administator

The main.py file mentioned above relates to your main file for the app. The following lines must be 
inserted in that main file. These define the class for the worker url page.

    class MyWorker(webapp.RequestHandler):

       def post(self):
          rpc = urlfetch.create_rpc()
          msg = self.request.get('msg')
          addr = self.request.get('addr')
          urlfetch.make_fetch_call(rpc, addr, payload = msg, method=urlfetch.PUT)


Then in your webapp.WSGIApplication(...) definition in the main file add the following:

          ('/worker', MyWorker)

If you chose a different url for your worker in the app.yaml setup, be sure to change that here also, as this
connects that url to the class defined above.

Once this is done, you can use the python logging module as normal and it will log to Logentries also.
For example:

           logging.info("informational message")
           logging.warn("warning message")
           logging.crit("critical message")


Pull-Queue Logging
------------------

To Enable Pull-Queue Logging on your app, you must first import both logging and le in your main file for the app,
like so:

         import logging, le

and then add the following lines to your main definition in the file:

         if len(logging.getLogger('').handlers) <= 1:
                logging.getLogger('').addHandler(le.PullQueue(key, location))

You will notice the two parameters above called key and location.

  - Key is your unique password to the site and must be kept secret.
  - Location is the name of your host on logentries followed by the name of the log, e.g 'localhost/test.log'

Create a file called backends.yaml with the following contents:

         backends:
         - name: worker
           class: B1
           instances: 1
           start: backend.py


Create a file called queue.yaml with the following contents:

        queue:
        - name: pull-queue
          mode: pull
          acl:
          - user_email: "put_your_email_here"
  

Once this is done, you can use the python logging module as normal and it will log to Logentries also.
For example:

          logging.info("informational message")
          logging.warn("warning message")
          logging.crit("critical message")

