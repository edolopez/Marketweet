Marketweet
====================
Marketweet is a bot for twitter coded in python, totally for marketing puposes. It is relying on the twitter module developed by the Python-Twitter Developers group http://code.google.com/p/python-twitter/ 

With Marketweet you can:

* Post new tweets from a file in random moments. 
* Follow users based on specific keywords.
* Unfollow those users who haven't returned the follow in certain time.
* To keep following those users who haven't returned the follow, considered as potential for your timeline and credibility. 

Dependencies
---------------------
To start using Marketweet you need to install some dependencies: 

Simplejson: http://cheeseshop.python.org/pypi/simplejson 
Httplib2: http://code.google.com/p/httplib2/ 
OAuth2: http://github.com/simplegeo/python-oauth2

The OAuth2 module can be added into the Marketweet project dragging and dropping the main folder. 

Twitter Module: http://code.google.com/p/python-twitter/
Documentation of the twitter module: http://static.unto.net/python-twitter/0.5/doc/twitter.html

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
                                        
If you don't have the credentials for your account, you can easily set up them here https://dev.twitter.com/ signing in with your corresponding account.

### ircBot.py

Next, you can modify if you want the ircBot.py file. Everything can be modified, but if you like the logic of the processes about to execute, the main section you may want to modify is where all constants are initialized:

    '''Default variables for global use on the entire bot app.'''
    MAXIMUM_PAGE = 100
    SLEEP_FOLLOWING = 60 * 60 * 1           # 60 seconds times 60 minutes times N hours of sleep
    SLEEP_UNFOLLOWING = 60 * 60 * 24 * 7    # Whole week of sleep
    SLEEP_NEW_TWEET = 60 * 60 * 1 
    ONE_DAY = 86400
    
These variables are used in all places where the time.sleep(CONSTANT) is used to sleep processes and keep the account as another user in the twitter world. It is needed because:

* 150 requests to the API per hour are allowed.
* You can follow 500 users per day, otherwise your account will be closed.
* You cannot follow more than 2000 users, if the difference between followers and following is more than 2000 http://twittnotes.com/2009/03/2000-following-limit-on-twitter.html 

### twitter.py

Finally, and according to the last points highlighted, the twitter.py module from the Python-Twitter Developers was modified in order to keep the processes running, no matter whether an error ocurred or a technical problem appeared during the requests throught the API. Here's the modified sections to accomplish this:

The  _ParseAndCheckTwitter method:

    def _ParseAndCheckTwitter(self, json):
    """Try and parse the JSON returned from Twitter and return
    an empty dictionary if there is any error. This is a purely
    defensive check because during some Twitter network outages
    it will return an HTML failwhale page."""
    try:
      data = simplejson.loads(json)
      self._CheckForTwitterError(data)
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
    """Raises a TwitterError if twitter returns an error message.

    Args:
      data:
        A python dict created from the Twitter json response

    Raises:
      TwitterError wrapping the twitter error message if one exists.
    """
    # Twitter errors are relatively unlikely, so it is faster
    # to check first, rather than try and catch the exception
    if 'error' in data:
      #raise TwitterError(data['error'])
      print TwitterError(data['error'])
      
As you can see, instead raising the error catched, it is only printed, so the application since its execution is never stopped. 

You can return this to its original functionality commenting the print lines and uncommenting the raise lines. Also, yo need to remove the line where the data variable is set to a new hash '{}'. 

Running
---------------------
Marketweet uses the multiprocessing module, which allow you have multiple processes running on the backend. In this case, the Tweeting and Following processes both are running all the time. These read certain files to update what they are doing, making easy the bot's administration, and allowing to keep running the bot without stoping it for minimum modifications. These files are:

* tweets.txt: A list of tweets, where each has at most 140 characters and is tweetead after a certain time.
* topics.txt: The list of keywords the bot should rely to follow people. Topics can be as long as you want, separate by a line break. 
* users.txt: The list of users the bot can ignore and keep following even they haven't returned the follow. 

To run Marketweet, just type in terminal

    python ircBot.py

License
---------------------
