from optparse import Values
import requests
from requests_oauthlib import OAuth1Session
import os
import json
from savers import SendToFile, SendToTerminal, SendToArchive, SendToImages
from dotenv import load_dotenv 
load_dotenv()
import time
#consumer_key = os.getenv("APIKey")
#consumer_secret = os.getenv("APIKeySecret")
#bearer_token = os.getenv("BearerToken")

#def UserLikeLookUp(USER_ID, TwtCount):
#    url = f"https://api.twitter.com/2/users/{USER_ID}/liked_tweets?max_results={TwtCount}"
#    json_response = connect_to_endpoint(url)
#    SendToTerminal(json_response)
#    #SendToArchive(json_response, USER_ID, "Userlikes")
#    return json_response
#
#def UserTweetLookUp(USER_ID, user, TwtCount):
#    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results={TwtCount}"
#    json_response = connect_to_endpoint(url)
#    #SendToTerminal(json_response)
#    SendToArchive(json_response, "Tweets", user)
#    return json_response

#def TweetLikerLookUp(TWEET_ID):
#    url = "https://api.twitter.com/2/tweets/{}/liking_users".format(TWEET_ID)
#    json_response = connect_to_endpoint(url)
#    SendToTerminal(json_response)
#    return json_response

#------------------------------------------------------------------------
def image_handler(user):
    #fetching images from users timeline json
    with open(f'{user}-TimeLine.json', 'r', encoding='utf-8') as j:
        tweets = json.loads(j.read())
        if not tweets:
            print("empty list of tweets")
        x = "fill"
        i = 0
        try:
            path = f"{user}_images"
            os.mkdir(path)
            print("Directory " , path ,  " Created ") 
        except FileExistsError:
            print("Directory " , path ,  " already exists")
        while x != "":
            try:
                MUrl = tweets["includes"]["media"][i].get('url')
                MKey = tweets["includes"]["media"][i].get('media_key')
                SendToImages(path, MUrl, MKey)
                print(f"saving image: {MUrl}")
                i += 1
            except:
                print("reached end of tweets")
                break

        print("all images downloaded")


def user_timeline_fetch(USER_ID, user, TwtCount):
    query = "&expansions=attachments.media_keys&tweet.fields=created_at,public_metrics&media.fields=url&exclude=retweets,replies"
    type = "TimeLine"
    url_formatter(USER_ID, user, TwtCount, query, type)
    return

def image_searcher(USER_ID, user, TwtCount):
    query = "&expansions=attachments.media_keys&media.fields=url&exclude=retweets,replies"
    type = "Images"
    print("doing image tweet fetch now!")
    url_formatter(USER_ID, user, TwtCount, query, type)
    return

def url_formatter(USER_ID, user, TwtCount, query, type):
    next_token = ""
    h = 100
    TwtCount = int(TwtCount)
    while TwtCount > 0:
            time.sleep(1)
            #case where its the first search, and has more than 100 tweets
            if (TwtCount > h) and (next_token == ""):
                next_token = tweet_puller(USER_ID, user, h, next_token, query, type)
                TwtCount -= h
            #case where its the first search, and has less than 100 tweets
            elif (TwtCount < h) and (next_token == ""):
                next_token = tweet_puller(USER_ID, user, TwtCount, next_token, query, type)
                print("all wanted tweets read, finishing fetch!")
                return 1
            #case where there is a next token, and theres more than 100 tweets remaining
            elif int(TwtCount) > h:
                next_token = tweet_puller(USER_ID, user, h, next_token, query, type)
                TwtCount -= h
            #case where there is less than 100 tweets remaining and no token, or something messed up
            else:
                tweet_puller (USER_ID, user, TwtCount, next_token, query, type)
                next_token = ""
                print("all wanted tweets read, finishing fetch!")
                return 


def tweet_puller (USER_ID, user, max_results, next_token, query, type):
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results={max_results}{query}"
    if (next_token != ""):
        url += f"&pagination_token={next_token}"
    json_response = connect_to_endpoint(url)
    SendToArchive(json_response, type, user,)
    try:
        next_token = json_response["meta"]["next_token"]
        print(next_token)
    except KeyError:
        print("no next token returned")
        return
    return next_token


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "SnutrisTwitAPI"
    return r

def look_up_user(u):
    # a method to look up a user by their username, returning their id
    ux = f"https://api.twitter.com/2/users/by/username/{u}"
    json_response = connect_to_endpoint(ux)
    userID = json_response["data"]["id"]
    #print(userID)
    return userID

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def api_script(state, tweet_count, user, secret, bearer, token):
    global bearer_token
    bearer_token = str(bearer)
    #print("---------------------------------------")
    #UserLikeLookUp(look_up_user("usernamehere"), "5")
    #TweetLikerLookUp("useridhere")
    match state:
        case 1:
            s = user_timeline_fetch(look_up_user(user), user, f"{tweet_count}")
            return s
        case 2:
            s = image_handler(user)
            return s
        case 3:
            s = user_timeline_fetch(look_up_user(user), user, f"{tweet_count}")
            return s
            


if __name__ == "__main__":
    api_script()