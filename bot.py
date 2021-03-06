import tweepy, DMSender, Asciify, time, os, RepoUploader, RepoUploaderV2, traceback
from PIL import Image

total = 0
repliedImg = 0
repliedNoImg = 0
errors = 0
recipient = "860537503006298113"    #Yep, that is me, DM me if you want :)

def authenticate():
    auth = tweepy.OAuthHandler(os.environ["tw_consumer_key"],os.environ["tw_consumer_secret"])
    auth.set_access_token(os.environ["tw_access_token"],os.environ["tw_access_token_secret"])
    api = tweepy.API(auth)
    gh = RepoUploader.API(os.environ["gh_key"])
    gl = RepoUploaderV2.API(os.environ["gl_token"])
    return (api,gh,gl)

def getImgUrl(tweet):
    return tweet.entities["media"][0]["media_url"]+':large'

def noImage(tweet):
    api.update_status("@{} Sorry, image not found 😔".format(tweet.user.screen_name),in_reply_to_status_id = tweet.id)
    global repliedNoImg 
    repliedNoImg+=1

def replyTo(tweet):
    if(tweet.user == api.me() or tweet.in_reply_to_user_id == api.me().id):
        return
    url = ""
    if 'media' in tweet.entities:
        url = getImgUrl(tweet)
    elif tweet.in_reply_to_status_id:
        inReplyTo = api.get_status(tweet.in_reply_to_status_id, tweet_mode = 'extended')
        if not 'media' in inReplyTo.entities:
            noImage(tweet)
            return
        url = getImgUrl(inReplyTo)
    else:
        noImage(tweet)
        return
    
    img = Asciify.getImage(url)
    
    mat = Asciify.generate(img,"Assets/JetBrainsMono-ExtraBold.ttf",saveAs = "reply.png")
    img.close()
    pageUrl = gh.postNewPage(tweet.user.screen_name+str(time.time()).replace(".",""),Asciify.matrixToString(mat))
    media = api.media_upload("reply.png")
    api.update_status("@{} 😀\n{}".format(tweet.user.screen_name,pageUrl),in_reply_to_status_id = tweet.id,media_ids=[media.media_id])
    global repliedImg
    repliedImg+=1

def checkStatuses(lastId):
    mentions = api.mentions_timeline(lastId, tweet_mode = 'extended')
    mentions.reverse()
    for tweet in mentions:
        global total
        total+=1
        try:
            replyTo(tweet)
        except Exception as e:
            DMSender.sendMsg(api,recipient,"Unexpected error while replying to {}".format(tweet.id))
            print(DMSender.sendMsg(api,recipient,str(e)))
            global errors
            errors+=1
    if(len(mentions)>0):lastId = mentions[-1].id
    return lastId

dailyUpdate = True
previousLastId = None

api,gh,gl = authenticate()
print(DMSender.sendMsg(api,recipient,"We are up and running"))

try:
    while(True):
        try:
            if(time.localtime().tm_hour == 2):
                dailyUpdate = False
            if(not dailyUpdate and time.localtime().tm_hour == 3):
                print(DMSender.sendMsg(api,recipient,"Daily stats: {} mentions, {} replies, {} replied no image, {} errors. LAST_ID: {}".format(total,repliedImg,repliedNoImg,errors,previousLastId)))
                total = repliedImg = repliedNoImg = errors = 0
                dailyUpdate = True 
            tries = 0
            while True:
                try:
                    previousLastId = int(gl.getFileStr('lastID.txt'))
                    break
                except:
                    if tries == 4:
                        traceback.print_exc()
                        raise Exception('Gitlab issue')
                    print(DMSender.sendMsg(api,recipient,"Unable to read last id, retry in 30 seconds"+str(tries)))
                    tries+=1
                time.sleep(30)
            newLastId = checkStatuses(previousLastId)
            #This is to only update the file if requiered
            if(newLastId != previousLastId):
                tries = 0
                while True:
                    try:
                        gl.updateFile('lastID.txt',str(newLastId))
                        break
                    except:
                        if(tries == 4):
                            traceback.print_exc()
                            raise Exception('Gitlab issue')
                        print(DMSender.sendMsg(api,recipient,"Unable to write last id, retry in 30 seconds"))
                        tries+=1
                    time.sleep(30)
            print("So far today: {} mentions, {} replies, {} replied no image, {} errors. LAST_ID: {}".format(total,repliedImg,repliedNoImg,errors,newLastId))
            
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
            traceback.print_exc()
            time.sleep(7200)
        time.sleep(17)
except Exception as e:
    api.sendMsg(api,recipient, "My battery is low, and it's getting dark")
    api.sendMsg(api,recipient,str(e))


