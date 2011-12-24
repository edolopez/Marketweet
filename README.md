Marketweet
====================
Marketweet is a bot for twitter coded in python, totally for marketing puposes. It is relying on the twitter module developed by the [Python-Twitter Developers group](http://code.google.com/p/python-twitter/) 

With Marketweet you can:

* Post new tweets from a file in random moments. 
* Follow users based on specific keywords.
* Unfollow those users who haven't returned the follow in certain time.
* To keep following those users who haven't returned the follow, considered as potential for your timeline and credibility. 

It is developed to be used on Linux OS. 

Dependencies
---------------------
To start using Marketweet you need to install some dependencies: 

* [Simplejson:](http://cheeseshop.python.org/pypi/simplejson) Can be installed through terminal
* [Httplib2:](http://code.google.com/p/httplib2/) Can be installed through terminal
* [OAuth2:](http://github.com/simplegeo/python-oauth2) Can be added into the Marketweet project dragging and dropping the main folder oauth2.

For the __Twitter Module__ developed by the Python-Twitter Developers group, you can directly download the entire project, or use the essential files posted here with the actual Marketweet project. Some lines have been adapted to Marketweet's functionality, so I suggest you to use the twitter module posted here. In case you want the newest version of the Twitter Module, please adapt it as discussed in the **Setup** section **twitter.py** header. 

For an explicit explanation of what the Twitter module does, you can see the documentation [here](http://static.unto.net/python-twitter/0.5/doc/twitter.html).

Setup
---------------------
You need to modify some files to start using the Marketweet application.

### account.py

First of all, the account.py need to have all credentials and information about the account you are going to use and authenticate.

    USERNAME = "username"
    ...
    ...
    api = twitter.Api(consumer_key='consumer_key', 
                      consumer_secret='consumer_secret', 
                      access_token_key='access_token_key',
                      access_token_secret='access_token_secret', 
                      debugHTTP=False)
                                        
If you don't have the credentials for your account, you can easily set up them [here](https://dev.twitter.com/), signing in with your corresponding account.

### ircBot.py (optional)

Next, you can modify if you want the ircBot.py file. Everything can be modified, but if you like the logic of the processes about to execute, the main section you may want to modify is where all constants are initialized:

    '''Default variables for global use on the entire bot app.'''
    MAXIMUM_PAGE = 100
    SLEEP_FOLLOWING = 60 * 60 * 1           # 60 seconds times 60 minutes times N hours of sleep
    SLEEP_UNFOLLOWING = 60 * 60 * 24 * 7    # Whole week of sleep
    SLEEP_NEW_TWEET = 60 * 60 * 1 
    ONE_DAY = 86400
    
These variables are used in all places where the time.sleep(CONSTANT) is used to sleep processes and keep the account as another user in the twitter world. It is needed because:

* 150 requests per hour using the API are allowed.
* You can follow 500 users per day, otherwise your account will be closed.
* You cannot follow more than 2000 users, if the difference between followers and following is more than 2000 http://twittnotes.com/2009/03/2000-following-limit-on-twitter.html 

### twitter.py (optional)

Finally, and according to the last points highlighted, the twitter.py module from the Python-Twitter Developers was modified in order to keep the processes running, no matter whether an error ocurred or a technical problem appeared during the requests throught the API. Here's the modified sections to accomplish this:

The  _ParseAndCheckTwitter method:

    def _ParseAndCheckTwitter(self, json):
    ...
    except ValueError:
      if "<title>Twitter / Over capacity</title>" in json:
        #raise TwitterError("Capacity Error")
        print TwitterError("Capacity Error")
      if "<title>Twitter / Error</title>" in json:
        #raise TwitterError("Technical Error")
        print TwitterError("Technical Error")
      #raise TwitterError("json decoding")
      print TwitterError("json decoding")
      data = {}     # As the program is never stopped, we need to return something at least

      return data
    
The _CheckForTwitterError method:

    def _CheckForTwitterError(self, data):
    ...
    if 'error' in data:
      #raise TwitterError(data['error'])
      print TwitterError(data['error'])
      
As you can see, instead raising the error catched, it is only printed, so the application since its execution is never stopped. 

You can return this to its original functionality commenting the print lines and uncommenting the raise lines. Also, yo need to remove the line where the data variable is set to a new hash '{}'. 

Running
---------------------
Marketweet uses the multiprocessing module, which allow you have multiple processes running on the backend. In this case, the Tweeting and Following processes both are running all the time. These read certain files to update what they are doing, making easy the bot's administration, and allowing to keep running the bot without stoping it for minimum modifications. The files that should be created are:

* __tweets.txt__: A list of tweets, where each has at most 140 characters and is tweetead after a certain time, separated by a line break. 
* __topics.txt__: The list of keywords the bot should rely to follow people. Topics can be as long as you want, separated by a line break. 
* __users.txt__: The list of users the bot can ignore and keep following even they haven't returned the follow, separated by a line break.  

To run Marketweet, just type in terminal

    python ircBot.py

License
---------------------
MIT License. Copyright 2011, Eduardo López | https://github.com/edolopez/
