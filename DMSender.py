import tweepy

def formatter(mentions = 0,replies = 0,errors = 0):
    return "{} mentions, {} replies, {} errors".format(mentions,replies,errors)

def sendMsg(api,recipient,msg):
    try:
        api.send_direct_message(recipient,msg)
        return "Message sent"
    except Exception as e:
        return "Unable to reach user via DM"+e.response.text