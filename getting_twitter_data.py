# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 08:06:08 2018

@author: KARIS
"""

import json
from tweepy import API
from tweepy import OAuthHandler

#authentication
#consumer key ,  consumer secret ,  access token , access secretrecieved from apps.twitter.com
def get_twitter_auth():
    
    
    ckey ='8PCpsYopUpwLovotBC2dduTRQ'
    csecret = 'BXYWhOPVzN9kJscSMFy0JKY86rYGneXB8TyM38pAGq7iq9onhq'
    atoken = '2491698797-plmnGcmj39ammb9ttNLleQLo6JUf4GYcJaPfHik'
    asecret = 'V9jdpuyoa8sffYowWf02XJZQYKM39cddx6jkgVsPtgxrS'
    
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken , asecret)

    return auth


#client as instance of twitter.api to be used for interaction with twitter
def get_twitter_client():
    """Setup Twitter API client.
    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client

from tweepy import Cursor 

client = get_twitter_client()


#reading names from human and bot list
user_list = df[1]

user_main=[]

for i in user_list:
    user_main.append(i.strip('@')) 

for user in user_main: 
    #creating jsonl files
    fname = "{}.jsonl".format(user)
    
    with open(fname , 'w') as f:
        try:
            for page in Cursor(client.user_timeline ,  screen_name = user,
                               count = 200).pages(1):
                for status in page:
                    f.write(json.dumps(status._json)+"\n")
                    
        except Exception as e:
            print(e, user)