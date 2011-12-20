import account
import twitter
import string
import time
import random
import multiprocessing

'''Initialization of both twitter global access and bot's account.'''
twitter = twitter.Api()
bot = account.initialize()

'''Default variables for global use on the entire bot app.'''
MAXIMUM_PAGE = 100
BOT_ACCOUNT = "daehode"
SLEEP_NEW_TWEET = 60 * 60 * 5   # 60 seconds times 60 minutes times N hours of sleep

following = 0   #Users following per day. Shouldn't pass the 500
followers_limit = 0


'''Returns the User Object with the screen name of the authenticated account.'''
def get_bot_user():
  return bot.GetUser(BOT_ACCOUNT)


'''Function to follow those who have recently talked about an specific topic or word.'''
def follow_people_by_topic():
  acum = 0
  global following
  pagination_index = 1
  accounts_per_page = 20
  topic_to_search = "tec"
  while pagination_index <= 5:
    chicos_tec = twitter.GetSearch(topic_to_search, None, None, accounts_per_page, pagination_index, "es", "true", True)
    while acum < len(chicos_tec):
      user = chicos_tec[acum].user 
      if user.followers_count < 1000:   # Conditions as filter to follow new people
        #bot.CreateFriendship(user.screen_name)
        print "Started following: " + user.screen_name # + " from " + user.time_zone
      acum += 1
    following += acum
    acum = 0
    pagination_index += 1
  print following
  #time.sleep(60)    # 86400 for an entire day


'''Function to unfollow people who haven't returned the follow yet.'''
def unfollow_people():
  while True:
    page, unfollowed = 0, 0
    users_bot_follows = bot.GetFriends()        # To determine the number of iterations through folowers' pages
    following_limit = len(users_bot_follows)/MAXIMUM_PAGE   # Aproximatley 100 following users per page
    followers_limit = get_bot_user().GetFollowersCount()/MAXIMUM_PAGE
    print 'UNFOLLOWING Process:\t Started'
    
    while page <= following_limit:
      page = 1
      for user in users_bot_follows:
        if not following_bot(user):
          #bot.DestroyFriendship(user.screen_name)
          print "Unfollowing: " + user.screen_name
          unfollowed += 1
      page += 1
    print '-------------------'
    print 'UNFOLLOWING Process:\t Finished'
    print 'People Unfollowed:\t ' + unfollowed
    print '-------------------'
    time.sleep(3600)

def following_bot(user):
  page = 0
  while page <= followers_limit:
    for follower in bot.GetFollowers(page):
      if follower == user:
        return True
    page += 1
  return False


'''Function to tweet random phrases from an specific file.'''
def tweet_from_file():
  while True:
    f = open('tweets.txt', 'r')   # Open file saving tweets in read mode
    tweets = f.readlines()        # Save all lines in a list as a possible tweet
    f.close()                     # Close file to avoid any further issue

    index = random.randint(0, len(tweets)-1)
    #bot.PostUpdates(tweets[index])
    print '-------------------'
    print 'TWEETING Process:\t Finished'
    print 'Tweet was:\t\t ' + tweets[index].split('\n')[0]
    print '-------------------'
    del tweets[index]

    f = open('tweets.txt', 'w')   # Reopen file to write remaining tweets
    f.writelines(tweets)
    f.close()
    time.sleep(SLEEP_NEW_TWEET)


'''Bot flow'''
# Should use threads for syncronizathion
#follow_people_by_topic()
#unfollow_people()
#tweet_from_file()

#unfollow.start()
#tweet_from_f.start()
multiprocessing.Process(target=tweet_from_file).start()
multiprocessing.Process(target=unfollow_people).start()

