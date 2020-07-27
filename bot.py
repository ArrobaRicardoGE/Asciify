import tweepy, DMSender, Asciify, time, os
from PIL import Image

total = 0
repliedImg = 0
repliedNoImg = 0
errors = 0
recipient = "860537503006298113"

def authenticate():
    auth = tweepy.OAuthHandler(os.environ["tw_consumer_key"],os.environ["tw_consumer_secret"])
    auth.set_access_token(os.environ["tw_access_token"],os.environ["tw_access_token_secret"])
    api = tweepy.API(auth)
    return api

def getImgUrl(tweet):
    return tweet.entities["media"][0]["media_url"]

def noImage(tweet):
    api.update_status("Image not found 😔",in_reply_to_status_id = tweet.id)
    global repliedNoImg 
    repliedNoImg+=1

def replyTo(tweet):
    url = ""
    try:
        url = getImgUrl(tweet)
    except:
        noImage(tweet)
        return
    img = Asciify.getImage(url)
    Asciify.generate(img,8,"Assets/JetBrainsMono-ExtraBold.ttf",10,saveAs = "reply.png")
    img.close()
    media = api.media_upload("reply.png")
    api.update_status("😀",in_reply_to_status_id = tweet.id,media_ids=[media.media_id])
    global repliedImg
    repliedImg+=1

def checkStatuses(lastId):
    mentions = api.mentions_timeline(lastId)
    mentions.reverse()
    for tweet in mentions:
        global total
        total+=1
        try:
            replyTo(tweet)
        except:
            retVal = DMSender.sendMsg(api,recipient,"Unexpected error while replying to {}".format(tweet.id))
            global errors
            errors+=1
            if(not retVal):
                print("Unable to reach user via DM")

    if(len(mentions)>0):lastId = mentions[-1].id
    return lastId

dailyUpdate = True
gLastId = "1287578288165130240"

api = authenticate()
DMSender.sendMsg(api,recipient,"We are up and running")

try:
    while(True):
        try:
            if(time.localtime().tm_hour == 2):
                dailyUpdate = False
            if(not dailyUpdate and time.localtime().tm_hour == 3):
                print(DMSender.sendMsg(api,recipient,"Daily stats: {} mentions, {} replies, {} replied no image, {} errors. LAST_ID: {}".format(total,repliedImg,repliedNoImg,errors,gLastId)))
                total = repliedImg = repliedNoImg = errors = 0
            gLastId = checkStatuses(gLastId)
            print("So far today: {} mentions, {} replies, {} replied no image, {} errors. LAST_ID: {}".format(total,repliedImg,repliedNoImg,errors,gLastId))

        except tweepy.RateLimitError as e:
            print("RateLimit: "+e.response.text)
            print(DMSender.sendMsg(api,recipient,"Urgent: {}\n Sleeping for one hour".format(e.response.text)))
            time.sleep(3600)
        except tweepy.TweepError as e:
            print("Error: "+e.response.text)
            print(DMSender.sendMsg(api,recipient,"Something went wrong\n{}".format(e.response.text)))
        except Exception as e:
            print("Error: "+str(e))
            print(DMSender.sendMsg(api,recipient,"URGENT: {}\n Sleeping for two hours".format(str(e))))
            time.sleep(7200)
        time.sleep(15)
except Exception as e:
    api.sendMsg(api,recipient, "My battery is low, and it's getting dark")
    api.sendMsg(api,recipient,str(e))


