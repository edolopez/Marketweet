'''
Copyright (c) 2011, Eduardo Lopez | https://github.com/edolopez/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import twitter
import account
import multiprocessing
import string, time, random, datetime, codecs

'''Initialization of both twitter global access and bot's account.'''
twitter = twitter.Api()
bot = account.initialize()

'''Default variables for global use on the entire bot app.'''
MAXIMUM_PAGE = 100
SLEEP_FOLLOWING = 60 * 60 * 1           # 60 seconds times 60 minutes times N hours of sleep
SLEEP_UNFOLLOWING = 60 * 60 * 24 * 7    # Whole week of sleep
SLEEP_NEW_TWEET = 60 * 60               # 60 seconds times 60 minutes times N hours of sleep
ONE_DAY = 86400

following = 0   # Users following per day. Shouldn't pass 500
followers_limit = 0
following_limit = 0


'''Returns the User Object with the screen name of the authenticated account.'''
def get_bot_user():
  return bot.GetUser(account.GetUser())


'''Function to follow those who have recently talked about an specific topic or word.'''
'''Limit of 150 requests per hour'''
def follow_people_by_topic():
  while True:
    global following
    acum, friends, pagination_index, accounts_per_page, t = 0, 0, 1, 20, time.time()
    topic_to_search = topic()
    followed_users = users('followed.txt')
    
    f = codecs.open('replies.txt', "r", "utf-8")     # Open file saving replies in read mode
    replies = f.readlines()          # Save all lines in a list as a possible reply
    f.close()                       # Close file to avoid any further issue
    
    print '--' * 15
    print 'Searching topic: ' + topic_to_search
    print '--' * 15
    while pagination_index <= 5:
      print 'Searching users in page ' + str(pagination_index) + '...'
      search = twitter.GetSearch(topic_to_search, None, None, 
                                 accounts_per_page, pagination_index, "es", "true", True)
      while acum < len(search):
        user = search[acum].user 
        # Conditions as filter to follow new people
        if user.followers_count < 1000 and str(user.screen_name) not in followed_users:
          print "Started following: " + str(user.screen_name)
          bot.CreateFriendship(user.screen_name)
          
          # Reply to new friend
          index = random.randint(0, len(replies)-1)
          bot.PostUpdates('@' + user.screen_name + ' ' + replies[index])
          
          followed_users.append(str(user.screen_name))      # Add the new user followed to list
          friends += 1     # Real number of people being followed
        time.sleep(30)     # Patch to keep requests under 150 per hour (3600/150)
        acum += 1
      following += acum
      acum = 0
      pagination_index += 1
    print '--' * 15
    print 'Following ' + str(friends) + ' new users. (' + str(following) + ' total requests)'
    print 'Time taken: ' + str(datetime.timedelta(seconds=(time.time() - t))).split('.')[0]
    print '--' * 15
    users_list = []
    f = open('followed.txt', 'w')     # Reopen file to write remaining tweets
    for user in followed_users:       # Removes the '\n' from file for each user
      users_list.append(user + '\n')  # Adds '\n' to each user to save them again on file
    f.writelines(users_list)          # Write users followed with \n for each
    f.close()
    if (following >= 2000):    # Reached the limit imposed by twitter
      print 'Waiting until people start to return the follow in order to unfollow' 
      print str(time.asctime(time.localtime()))
      time.sleep(SLEEP_UNFOLLOWING)
      unfollow_people()       # Need to unfollow people, in order to follow more. 
      following = 0
    else:
      print 'Sleeping for 7 hours keeping a rationale behavior.' 
      print str(time.asctime(time.localtime()))
      time.sleep(25200)       # Keep a rationale behavior while following (waits 7 hours)

'''Returns the last line from the file specified for topics to search'''
def topic():
  f = open('topics.txt', 'r')       # Open files to make them an array
  topics = f.readlines()
  f.close()

  topic_line = topics.pop()         # Pops last line of the file
  topics.insert(0, topic_line)      # Inserts line to the file again
  
  f = open('topics.txt', 'w')       # Reopen file to write topics again
  f.writelines(topics)
  f.close()  
  return topic_line.split('\n')[0]  # Remove the jump line at the end of the line
  

'''Function to unfollow people who haven't returned the follow yet.'''
def unfollow_people():
  print '--' * 15
  print 'UNFOLLOWING Process:\t Started'
  global followers_limit
  page, unfollowed, t = 0, 0, time.time()
  following_limit = get_bot_user().GetFriendsCount()/MAXIMUM_PAGE   # Aproximatley 100 following users per page
  followers_limit = get_bot_user().GetFollowersCount()/MAXIMUM_PAGE
  master_users = users('users.txt')        # List of all users should follow no matter what

  while page <= following_limit:
    users_bot_follows = bot.GetFriends()        # To determine the number of iterations through following pages
    for user in users_bot_follows:
      if not following_bot(user) and str(user.screen_name) not in master_users:
        print "Unfollowing: " + str(user.screen_name)
        bot.DestroyFriendship(user.screen_name)
        unfollowed += 1
      time.sleep(24)     # Patch to keep requests under 150 per hour
    page += 1
  print '--' * 15
  print 'UNFOLLOWING Process:\t Finished'
  print 'People Unfollowed:\t ' + str(unfollowed)
  print 'Time taken: ' + str(datetime.timedelta(seconds=(time.time() - t))).split('.')[0]
  print '--' * 15

'''Function returning true if the user received as parameter is following the bot. Otherwise return false.'''
def following_bot(user):
  page = 0
  while page <= followers_limit:
    for follower in bot.GetFollowers(page):
      if follower == user:
        return True
    page += 1
  return False

'''Returns a list of users that should be followed even if the don't follow back'''
def users(_file):
  users_list = []
  f = open(_file, 'r')       # Open files to make them an array
  master_users = f.readlines()
  f.close()
  
  for user in master_users:        # Removes the '\n' from file for each user
    users_list.append(user.split('\n')[0])
  
  return users_list
  
  
'''Funtion that follows those users following the account, but not followed yet'''
def follow_people_not_followed():
  print 'FOLLOWING THE UNFOLLOWED Process: Started'
  page, new_following, t = 0, 0, time.time()
  global following_limit
  followers_limit = get_bot_user().GetFollowersCount()/MAXIMUM_PAGE
  following_limit = get_bot_user().GetFriendsCount()/MAXIMUM_PAGE
  
  while page <= followers_limit:
    bot_followers = bot.GetFollowers(page)  # To determine the number of iterations through followers' pages
    for user in bot_followers:
      if not bot_is_following(user):
        print "Following: " + str(user.screen_name)
        bot.CreateFriendship(user.screen_name)
        new_following += 1
      time.sleep(24)     # Patch to keep requests under 150 per hour
    page += 1
  print '--' * 15
  print 'FOLLOWING THE UNFOLLOWED Process: Finished'
  print 'People Following:\t\t  ' + str(new_following)
  print 'Time taken: ' + str(datetime.timedelta(seconds=(time.time() - t))).split('.')[0]
  print '--' * 15

'''Returns True if the current account is following the user as parameter, otherwise returns False '''
def bot_is_following(user):
  page = 0
  while page <= following_limit:
    for following_user in bot.GetFriends():
      if following_user == user:
        return True
    page += 1
  return False

'''Function to tweet random phrases from an specific file.'''
def tweet_from_file():
  while True:
    f = open('tweets.txt', 'r')     # Open file saving tweets in read mode
    tweets = f.readlines()          # Save all lines in a list as a possible tweet
    f.close()                       # Close file to avoid any further issue

    if (len(tweets) <= 0):          # In case no more lines in file
      print '---> There are no tweets to tweet on the file <---'
    else:
      index = random.randint(0, len(tweets)-1)
      bot.PostUpdates(tweets[index])
      print '--' * 15
      print 'TWEETING Process:\t Finished'
      print 'Tweet was:\t\t ' + tweets[index].split('\n')[0]
      print '--' * 15
      del tweets[index]

    f = open('tweets.txt', 'w')     # Reopen file to write remaining tweets
    f.writelines(tweets)
    f.close()
    
    sleep_process = SLEEP_NEW_TWEET * random.randint(6, 18)
    print 'Hours for next tweet: ' + str(datetime.timedelta(seconds=(sleep_process))).split(':')[0]
    time.sleep(sleep_process)     # Sleeps certain time until the next tweet


'''Bot flow'''
# Should use threads for syncronizathion and independent tasks
multiprocessing.Process(target=follow_people_by_topic).start()
#multiprocessing.Process(target=follow_people_not_followed).start()
#multiprocessing.Process(target=tweet_from_file).start()

