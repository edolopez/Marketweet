Marketweet
====================
Marketweet is a bot for twitter totally for marketing puposes coded in python, relying on the twitter module developed by the Python-Twitter Developers group. 

With Marketweet you can:

* Post new tweets from a file in random moments. 
* Follow users based on specific keywords.
* Unfollow those users who haven't returned the follow in certain time.
* To not unfollow those specified users, considered as potential for your timeline and credibility. 

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
