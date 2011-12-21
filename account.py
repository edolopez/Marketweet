import os, sys
import time
import datetime

import simplejson
import twitter

USERNAME = "daehode"

def GetUser():
  return USERNAME

def initialize():
    #edohead:
    api = twitter.Api(consumer_key='KHahmK2ghrLmobPvQbu7AQ', 
                            consumer_secret='JPMP4IaOPoGGQxmYaAazPnm69QpLldTydk66FxjysE', 
                            access_token_key='437043500-IebOdmdxjSC3FlmkWB2foJZzvsIvxsfybsXo5QIl',
                            access_token_secret='7JyRTpkaebI5XW4ya38hIN1aEeJ6GQHVf2sC6uw4c', 
                            debugHTTP=False)

    #print api.VerifyCredentials()

    return api


    #since_id = None
    # try:
    #     print '-+'*10, 'polling Public Timeline'
    #     for status in api.GetPublicTimeline(since_id=since_id):
    #         item = status.AsDict()
    #         print item
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Friends Timeline'
    #     for status in api.GetFriendsTimeline(retweets=False):
    #         item = status.AsDict()
    #         print item
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Home Timeline'
    #     for status in api.GetFriendsTimeline(retweets=True):
    #         item = status.AsDict()
    #         print item
    # finally:
    #     print '*'*50
    
    #try:
    #    print '-+'*10, 'User Timeline'
    #    for status in api.GetUserTimeline():
    #        item = status.AsDict()
    #        print item
    #finally:
    #    print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Favorites'
    #     for status in api.GetFavorites():
    #         item = status.AsDict()
    #         print item
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Mentions'
    #     for status in api.GetMentions():
    #         item = status.AsDict()
    #         print item
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Retweets by User'
    #     for status in api.GetUserRetweets():
    #         item = status.AsDict()
    #         print item
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Lists'
    #     for status in api.GetLists('manta'):
    #         item = status.AsDict()
    #         print item
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Post Test'
    #     api.PostUpdate('Testing oAuth from command line %s' % time.time())
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Post Test - unicode'
    #     s = '\xE3\x81\x82' * 10
    #     api.PostUpdate('%s %s' % (s, time.time()))
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'Post Test - unicode'
    #     s = '\u1490'
    #     api.PostUpdate('%s %s' % (s, time.time()))
    # finally:
    #     print '*'*50
    # try:
    #     print '-+'*10, 'Post Test - unicode'
    #     # make sure input encoding param is set
    #     s = u'\u3042' * 10
    #     api.PostUpdate(u'%s %s' % (s, time.time()))
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'destroy friendship link'
    #     print api.DestroyFriendship("coda").AsDict()
    # finally:
    #     print '*'*50
    # 
    # try:
    #     print '-+'*10, 'create friendship link'
    #     print api.CreateFriendship("coda").AsDict()
    # finally:
    #     print '*'*50



