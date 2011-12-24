import twitter
import account
import string, time, random
import multiprocessing
#str(datetime.timedelta(seconds=(time.time() - t))).split('.')[0] => Seconds to human time

'''Initialization of both twitter global access and bot's account.'''
twitter = twitter.Api()
bot = account.initialize()

'''Default variables for global use on the entire bot app.'''
MAXIMUM_PAGE = 100
SLEEP_FOLLOWING = 60 * 60 * 1           # 60 seconds times 60 minutes times N hours of sleep
SLEEP_UNFOLLOWING = 60 * 60 * 24 * 7    # Whole week of sleep
SLEEP_NEW_TWEET = 60 * 60 * 1           # 60 seconds times 60 minutes times N hours of sleep
ONE_DAY = 86400

following = 0   # Users following per day. Shouldn't pass 500
followers_limit = 0


'''Returns the User Object with the screen name of the authenticated account.'''
def get_bot_user():
  return bot.GetUser(account.GetUser())


'''Function to follow those who have recently talked about an specific topic or word.'''
'''Limit of 150 requests per hour'''
def follow_people_by_topic():
  while True:
    global following
    acum, pagination_index, accounts_per_page = 0, 1, 20
    topic_to_search = topic()
    print 'Searching topic: ' + topic_to_search
    while pagination_index <= 5:
      print 'Searching users in page ' + str(pagination_index) + '...'
      search = twitter.GetSearch(topic_to_search, None, None, 
                                 accounts_per_page, pagination_index, "es", "true", True)
      while acum < len(search):
        user = search[acum].user 
        if user.followers_count < 1000:     # Conditions as filter to follow new people
          print "Started following: " + str(user.screen_name) # + " from " + user.time_zone
          bot.CreateFriendship(user.screen_name)
        time.sleep(24)     # Patch to keep requests under 150 per hour (3600/150)
        acum += 1
      following += acum
      acum = 0
      pagination_index += 1
    print 'Following ' + str(following) + ' new users'
    if (following == 500 or following == 1000 or following == 1500):  # Users following per day. Shouldn't pass 500
      print 'Sleeping for 24 hours. Limit of following 500 per day has been reached' 
      print str(time.asctime(time.localtime()))
      time.sleep(7200)     # Sleep one day. Limit has been reached
    elif (following >= 100):
      print 'Waiting until people start to return the follow in order to unfollow' 
      print str(time.asctime(time.localtime()))
      time.sleep(1000)               #SLEEP_UNFOLLOWING
      unfollow_people()       # Need to unfollow people, in order to follow more. 
      following = 0
    #time.sleep(SLEEP_FOLLOWING)

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
  print 'UNFOLLOWING Process:\t Started'
  page, unfollowed = 0, 0
  following_limit = get_bot_user().GetFriendsCount()/MAXIMUM_PAGE   # Aproximatley 100 following users per page
  followers_limit = get_bot_user().GetFollowersCount()/MAXIMUM_PAGE
  master_users = users()        # List of all users should follow no matter what

  while page <= following_limit:
    users_bot_follows = bot.GetFriends()        # To determine the number of iterations through folowers' pages
    for user in users_bot_follows:
      if not following_bot(user) and str(user.screen_name) not in master_users:
        print "Unfollowing: " + str(user.screen_name)
        bot.DestroyFriendship(user.screen_name)
        unfollowed += 1
      time.sleep(24)     # Patch to keep requests under 150 per hour
    page += 1
  print '-' * 10
  print 'UNFOLLOWING Process:\t Finished'
  print 'People Unfollowed:\t ' + str(unfollowed)
  print '-' * 10

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
def users():
  users_list = []
  f = open('users.txt', 'r')       # Open files to make them an array
  master_users = f.readlines()
  f.close()
  
  for user in master_users:        # Removes the '\n' from file for each user
    users_list.append(user.split('\n')[0])
  
  return users_list
  

'''Function to tweet random phrases from an specific file.'''
def tweet_from_file():
  while True:
    f = open('tweets.txt', 'r')     # Open file saving tweets in read mode
    tweets = f.readlines()          # Save all lines in a list as a possible tweet
    f.close()                       # Close file to avoid any further issue

    if (len(tweets) <= 0):          # In case no more lines in file
      print 'There are no tweets to tweet on the file'
    else:
      index = random.randint(0, len(tweets)-1)
      bot.PostUpdates(tweets[index])
      print '-' * 10
      print 'TWEETING Process:\t Finished'
      print 'Tweet was:\t\t ' + tweets[index].split('\n')[0]
      print '-' * 10
      del tweets[index]

    f = open('tweets.txt', 'w')     # Reopen file to write remaining tweets
    f.writelines(tweets)
    f.close()
    
    sleep_process = SLEEP_NEW_TWEET * random.randint(1, 5)
    time.sleep(3600)     # Sleeps certain time until the next tweet


'''Bot flow'''
# Should use threads for syncronizathion and independent tasks
#follow_people_by_topic("tec")
unfollow_people()
#tweet_from_file()

#tweet_from_file.start()
#multiprocessing.Process(target=follow_people_by_topic, args=(['mexico', 'rayados'],)).start()
#multiprocessing.Process(target=follow_people_by_topic).start()
#multiprocessing.Process(target=unfollow_people).start()
#multiprocessing.Process(target=tweet_from_file).start()

