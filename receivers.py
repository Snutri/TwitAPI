from optparse import Values
import threading
import requests
from requests_oauthlib import OAuth1Session
import os
import json
from savers import SendToFile, SendToTerminal, SendToArchive, SendToImages
from dotenv import load_dotenv 
load_dotenv()
from time import sleep

def image_handler(user, p_call, r_call):
    #fetching images from users timeline json
    with open(f'{user}-TimeLine.json', 'r', encoding='utf-8') as j:
        tweets = json.loads(j.read())
        if not tweets:
            print("empty list of tweets")
        i = 0
        try:
            path = f"{user}_images"
            os.mkdir(path)
            print("Directory " , path ,  " Created ") 
        except FileExistsError:
            print("Directory " , path ,  " already exists")
        while True:
            try:
                MUrl = tweets["includes"]["media"][i].get('url')
                MKey = tweets["includes"]["media"][i].get('media_key')
                SendToImages(path, MUrl, MKey)
                r_call.emit(f"saving image: {MUrl}")
                i += 1
                
            except:
                r_call.emit("Reached end of tweets")
                break

        print("all images downloaded")


def user_timeline_fetch(USER_ID, user, tweet_count, p_call, r_call):
    query = "&expansions=attachments.media_keys&tweet.fields=created_at,public_metrics&media.fields=url&exclude=retweets,replies"
    request_type = "TimeLine"
    thread_identity= threading.get_ident()
    r_call.emit(f"thread:[{thread_identity}] is pulling tweets from: [{user}]")
    url_formatter(USER_ID, user, tweet_count, query, request_type, p_call, r_call)
    return

def image_searcher(USER_ID, user, tweet_count, p_call, r_call):
    query = "&expansions=attachments.media_keys&media.fields=url&exclude=retweets,replies"
    request_type = "Images"
    print("doing image tweet fetch now!")
    url_formatter(USER_ID, user, tweet_count, query, request_type, p_call, r_call)
    return

def url_formatter(USER_ID, user, tweet_count, query, type, p_call, r_call):
    next_token = ""
    h = 100
    original_count = tweet_count
    tweet_count = int(tweet_count)
    while tweet_count > 0:
        #case where its the first search, and has more than 100 tweets
        if (tweet_count > h) and (next_token == ""):
            next_token = tweet_puller(USER_ID, user, h, next_token, query, type)
            tweet_count -= h
            p_call.emit(int(1/(int(original_count)/(int(original_count) - int(tweet_count)))*100))
        #case where its the first search, and has less than 100 tweets
        elif (tweet_count < h) and (next_token == ""):
            next_token = tweet_puller(USER_ID, user, tweet_count, next_token, query, type)
            tweet_count = 0
            p_call.emit(int(1/(int(original_count)/(int(original_count) - int(tweet_count)))*100))
            r_call.emit("all wanted tweets read, finishing fetch!\n")
            return 1
        #case where there is a next token, and theres more than 100 tweets remaining
        elif int(tweet_count) > h:
            next_token = tweet_puller(USER_ID, user, h, next_token, query, type)
            tweet_count -= h
            p_call.emit(int(1/(int(original_count)/(int(original_count) - int(tweet_count)))*100))
        #case where there is less than 100 tweets remaining and no token, or something messed up
        else:
            tweet_puller (USER_ID, user, tweet_count, next_token, query, type)
            next_token = ""
            tweet_count = 0
            p_call.emit(int(1/(int(original_count)/(int(original_count) - int(tweet_count)))*100))
            r_call.emit("all wanted tweets read, finishing fetch!\n")
            return 


def tweet_puller (USER_ID, user, max_results, next_token, query, type):
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results={max_results}{query}"
    if (next_token != ""):
        url += f"&pagination_token={next_token}"
    json_response = connect_to_endpoint(url)
    SendToArchive(json_response, type, user,)
    try:
        next_token = json_response["meta"]["next_token"]
    except KeyError:
        print("no next token returned")
        return
    return next_token


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "SnutrisTwitAPI"
    return r

def look_up_user(u):
    ux = f"https://api.twitter.com/2/users/by/username/{u}"
    json_response = connect_to_endpoint(ux)
    return json_response["data"]["id"]

def connect_to_endpoint(url):  # sourcery skip: raise-specific-error
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    return response.json()


def api_script(state, tweet_count, user, secret, bearer, token, p_call, r_call):
    global bearer_token
    bearer_token = str(bearer)
    print(threading.get_ident())
    state_director(state, tweet_count, user, secret, bearer, token, p_call, r_call)

def state_director(state, tweet_count, user, secret, bearer, token, p_call, r_call):
    match state:
        case 1:
            s = user_timeline_fetch(look_up_user(user), user, f"{tweet_count}", p_call, r_call)
            return s
        case 2:
            s = image_handler(user, p_call, r_call)
            return s
        case 3:
            s = user_timeline_fetch(look_up_user(user), user, f"{tweet_count}")
            return s

if __name__ == "__main__":
    api_script()