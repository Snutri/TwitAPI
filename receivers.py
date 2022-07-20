from optparse import Values
from requests_oauthlib import OAuth1Session
import requests
import os
import json
from savers import SendToFile, SendToTerminal, SendToArchive
from dotenv import load_dotenv 
load_dotenv()

#consumer_key = os.getenv("APIKey")
#consumer_secret = os.getenv("APIKeySecret")
#bearer_token = os.getenv("BearerToken")


def UserLikeLookUp(USER_ID, TwtCount):
    url = f"https://api.twitter.com/2/users/{USER_ID}/liked_tweets?max_results={TwtCount}"
    json_response = connect_to_endpoint(url)
    SendToTerminal(json_response)
    #SendToArchive(json_response, USER_ID, "Userlikes")
    return json_response

def UserTweetLookUp(USER_ID, user, TwtCount):
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results={TwtCount}"
    json_response = connect_to_endpoint(url)
    #SendToTerminal(json_response)
    SendToArchive(json_response, "Tweets", user)
    return json_response

#def TweetLikerLookUp(TWEET_ID):
#    url = "https://api.twitter.com/2/tweets/{}/liking_users".format(TWEET_ID)
#    json_response = connect_to_endpoint(url)
#    SendToTerminal(json_response)
#    return json_response

def UserTimelineLookUp(USER_ID, user, TwtCount):
    #url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={USER_ID}&count={TwtCount}"
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results={TwtCount}&tweet.fields=created_at,attachments,public_metrics&exclude=retweets,replies"
    json_response = connect_to_endpoint(url)
    #SendToTerminal(json_response)
    try:
        x = json_response["meta"]["next_token"]
        print(x)
    except:
        print("something happened with next token")
    
    SendToArchive(json_response, "TimeLine", user,)
    return json_response

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "SnutrisTwitAPI"
    return r

def lookupuser(u):
    # a method to look up a user by their username, returning their id
    ux = f"https://api.twitter.com/2/users/by/username/{u}"
    json_response = connect_to_endpoint(ux)
    userID = json_response["data"]["id"]
    print(userID)
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
    print("---------------------------------------")
    #UserLikeLookUp(lookupuser("usernamehere"), "5")
    #TweetLikerLookUp("useridhere")
    match state:
        case 1:
            s = UserTweetLookUp(lookupuser(user), user, f"{tweet_count}")
            return s
        case 2:
            s = UserLikeLookUp(lookupuser(user), f"{tweet_count}")
            return s
        case 3:
            s = UserTimelineLookUp(lookupuser(user), user, f"{tweet_count}")
            return s

            


if __name__ == "__main__":
    api_script()