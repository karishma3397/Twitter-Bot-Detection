#importing libraries
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import glob
import pandas as pd
from datetime import datetime
from dateutil.parser import parse



#taking only that accounts which are recent users[humans]
def is_recent_user(user_df):
    
    recent_year = []
    for i in user_df["created_at"]:
        recent_year.append(str(i).split()[0].split("-")[0])
    if recent_year.count('2018')>50:
        return True
    else:
        return False    
    
    
#lexical diversity of tweets
def lexical_diversity(user_df):
    total =""
    for i in range(0,user_df.shape[0]):
        text = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',' ',str(user_df['text'][i]))
        
        text = text.lower()
        text = text.split()
        #print(text)
        ps = PorterStemmer()
        text = [ps.stem(word) for word in text if not word in set(stopwords.words('english'))]
        text = ' '.join(text)
        total = total+text+ " "
        
    tot_word_count=len(total.split())
    unique_word_count =len(set(total.split()))
        #lexical_diversity1 = float(unique_word_count/tot_word_count)
        #print ("word count=",tot_word_count,"unique count=",unique_word_count,"lexical=",lexical_diversity1)
    if tot_word_count == 0 :
        return "nan"
    else:
        lexical_diversity1 = float(unique_word_count/tot_word_count)
        return lexical_diversity1

#checking minimum tweets
def check_min_tweet(user_df):
    if user_df.shape[0] == 200:
        return True
    else:
        return False
    
def friends_count(user_df):
    return user_df["user"][0]["friends_count"]
         
def followers_count(user_df):
    return user_df["user"][0]["followers_count"]


#tweeting device
def source(user_df):
    source = []
    for i in user_df["source"]:
        source.append(str(i))
    return max(set(source))
 
    

#tweet frequency
def avgDailyTweets(user_df):
	#list of average daily tweet rates
    DailyTweetCount = list()
    count = 0
    currentDate = None
    dates = user_df["created_at"]
    dates = []
    for i in user_df["created_at"]:
        dates.append(str(i).split()[0])
        
        ##for j in list(set(k)):
          #  print(j , k.count(j))
	#iterate over each tweet date
    for date in dates:
		#if the date hasn't changed then increate the
		#tweet frequency. Otherwise, if the date is different
		#store the tweet frequency and reset the frequency counter
        if currentDate == None:
            currentDate = date
            count = count + 1
        elif date == currentDate:
            count = count + 1
        else:
            DailyTweetCount.append(count)
            count = 1
            currentDate = date

	#add the last tweet frequency if it hasn't been added yet
    if len(DailyTweetCount) != len(set(dates)):
        DailyTweetCount.append(count)

	#compute the average or return 0 (avoiding divide by 0 error)
    if len(set(dates)) != 0:
        return(sum(DailyTweetCount)/float(len(set(dates))))
    else:
        return 0   

def verified_account(user_df):
    return user_df["user"][0]["verified"]
    
def status_to_age_ratio(user_df):
    status = user_df["user"][0]["statuses_count"]
    account_created_date =parse(user_df["user"][0]["created_at"]).date()
    total_days = (datetime.utcnow().date() - account_created_date).days
    if total_days>0:
        return status/total_days
    else:
        return 0


def listed_count(user_df):
    return user_df["user"][0]["listed_count"]


def url_count(user_df):
    count = 0
    for i in range(0,user_df.shape[0]):
        for url in user_df["entities"][i]["urls"]:
            if url is not None:
                if 'url' in url:
                    count+=1
    return count
def account_reputation(user_df):
    if (user_df["user"][0]["followers_count"] + user_df["user"][0]["friends_count"]) > 0:
        return user_df["user"][0]["friends_count"]/(user_df["user"][0]["followers_count"] + user_df["user"][0]["friends_count"])
    else:
        return None
bot_users = glob.glob("*.jsonl")
#main dataframe
count = 0
main_df = main_df.iloc[:1715,:]
#main_df = pd.DataFrame(columns=['user_name','lexical_diversity','friends_count','followers_count','listed_count','url_count','status_to_age_ratio','tweet_freq','account_reputation','source','is_bot'])
for file in bot_users:
    with open("kc.jsonl", 'r') as f:
        user_name = "kc.jsonl".strip('.jsonl')
        user_df = pd.read_json(f , lines = True)
        if check_min_tweet(user_df) == True and is_recent_user(user_df) == True:
            main_df = main_df.append({"user_name" : user_name}, ignore_index = True)
            main_df['lexical_diversity'][ main_df["user_name"]==user_name] = lexical_diversity(user_df)
            main_df['friends_count'][ main_df["user_name"]==user_name]=friends_count(user_df)
            main_df['followers_count'][ main_df["user_name"]==user_name]=followers_count(user_df)
            main_df['tweet_freq'][ main_df["user_name"]==user_name]=avgDailyTweets(user_df)
            main_df['source'][ main_df["user_name"]==user_name]=source(user_df)
            main_df['account_reputation'][ main_df["user_name"]==user_name]=account_reputation(user_df)
            main_df['url_count'][ main_df["user_name"]==user_name]=url_count(user_df)
            main_df['listed_count'][ main_df["user_name"]==user_name]=listed_count(user_df)
            main_df['status_to_age_ratio'][ main_df["user_name"]==user_name]=status_to_age_ratio(user_df)
            main_df["is_bot"][0:2092] = 1
            count+=1
            print( count)
main_df.to_csv("main_df_final2.csv")