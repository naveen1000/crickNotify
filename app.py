import requests
import time
from pycricbuzz import Cricbuzz
from pyfcm import FCMNotification

from firebase import firebase 
firebase = firebase.FirebaseApplication('https://naveen-kumar-simma.firebaseio.com/',None)    
 

push_service = FCMNotification(api_key="AAAALXgG6s8:APA91bHaUoZ9MwS78rdihRMc7GsN-NQ8oNDSEjEZcDMeU7DyAr_8EJRHCB_o13ydJXpGYLu4Nl3sA5rpNW6pPdK5Q9Fa50R6zdO6fiQnDU8OG7ZC7hieVYdTn_NeeBTY-XIRwowDh0KA")
registration_idLenovo="efNEoC5EUlg:APA91bGjWMcjMp2LxuyjRPjoAkdTL_px4t8iHITBNrku2gdPAsczs-hvPO8SKcyYxyhg1yMhTT3anZSxRnkJjS85aQyDErb4pGfvrfA8N7uDSmqb_vSaM4D5xODzUuCCwY88ApFw5MkU"
registration_idLoki = "cJgkzsCtdWI:APA91bFtwDKqHfyTUz4FNPV8OepucAQ8Wx840xddmjV0HztLHkkQsz2is7QFZK7o67SC4yjXV0oceWywSCkGTkfOpE9V_C51PddQIfaE3F5SkOWvAkqY7RYinze8Z0FjWCe57sy4p6lC"
registration_idLaptop="edgivMskGxQ:APA91bH-vIHwz1l4-kDmlqhwoJ41NwQGOGb2KCawiOMGAhmtGabeI_nGdUmp9AJ8GdtslFf3UMao-Wy9SAsd_eCa7ELxUUliFdW48k7sZCxAP_MPVLLjyuLVn86LOad3_xvQ_-eXAokX"
registration_ids = [registration_idLoki, registration_idLenovo,registration_idLaptop]
message_title = "CricNotify"
message_icon="firebase-logo.png"

def listOfMatches():
    try:
        c = Cricbuzz()
        matches=c.matches()
        for match in matches:
            print(match['id'] + "  " + match['start_time'] + " " + match['srs']  )
        print(matches[0]['id'])
        return matches[0]['id']

    except:
        print("An exception occurred fetching list of matches")

#prefetch wicket and over inorder to notify.
def prefetch():
    try:
        global tover
        global twicket
        global series_name
        source=requests.get(ur)
        data = source.json()
        series_name = data["series_name"]
        twicket=int(data["comm_lines"][0]["wkts"])
        twicket=twicket+1
        tover=int(float(data['bat_team']['innings'][0]['overs']))
        tover=tover+1
        #print(tover)
        #print(twicket)
        series_name="--"+series_name+"--"
        print(series_name)
    except:
        print("An exception occurred prefetching")
        time.sleep(5)
        prefetch()
#Fetching score main function of this app.

def score():
    try:
        global tover
        global twicket
        source=requests.get(ur)
        data = source.json()
        score=int(data["comm_lines"][0]["score"])
        wicket=int(data["comm_lines"][0]["wkts"])
        over=float(data['bat_team']['innings'][0]['overs'])
        detailed_score=data["comm_lines"][0]["score"]+"/"+data["comm_lines"][0]["wkts"]+" "+data['bat_team']['innings'][0]['overs']
        print(detailed_score,end=" ")

        try:
            firebase.put('/','object',detailed_score)
        except:
             print("An exception occurred updating Fdb")

        try:
            bowler=data['bowler'][0]['name']
            print(bowler)
            batname0=data['batsman'][0]['name']
            batname1=data['batsman'][1]['name']
            bat0score=data['batsman'][0]['r']
            bat1score=data['batsman'][1]['r']
            bat0ball=data['batsman'][0]['b']
            bat1ball=data['batsman'][1]['b']
            bowler=data['bowler'][0]['name']
            batters=batname0+"("+bat0score+"-"+bat0ball+")"+batname1+"("+bat1score+"-"+bat1ball+")"
            detailed_score=data["comm_lines"][0]["score"]+"/"+data["comm_lines"][0]["wkts"]+" "+data['bat_team']['innings'][0]['overs']
            print(batters)
        except:
            print("An exception occurred fetching either batters or bowler")
        try:    
            if (over==(tover-1.0+0.5)):
                global bow
                bow=bowler
            if over==tover:
                print("notified")
                msg = series_name+"\n"+ detailed_score+" " + bow + "\n" + batters +"\n"+ data['prev_overs']
                
                message_body = msg
                try:
                    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,message_body = message_body ,message_icon=message_icon)
                    print(result)
                except:
                    print("An exception occurred while trying to notify firebase")

                print(msg)
                notify(msg)
                tover=tover+1
                time.sleep(15)
            if wicket==twicket:
                msg=series_name+"\n"+"wicket "+str(twicket)+" "+data['last_wkt_name']+" "+data['last_wkt_score']+" B: "+bowler+"\n"+detailed_score
                message_body = msg
                try:
                    result =  push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,message_body = message_body ,message_icon=message_icon)
                    print(result)
                except:
                    print("An exception occurred while trying to notify firebase")

                
                notify(msg)
                twicket=twicket+1
                time.sleep(15)
        except:
            print("An exception occurred while trying to notify")
    except:
        print("An exception occurred fetching score")
    
 #Telegram notification    
def notify(msg):
    #Telegam Bot Url
    #url='https://api.telegram.org/bot879982304:AAHG7ZRyEMWoQB-ToaiJBv_gMvkW-ekJcSg/sendMessage?chat_id=582942300&text='+msg
    #TelegramChannel chatId -1001181667975
    url='https://api.telegram.org/bot879982304:AAHG7ZRyEMWoQB-ToaiJBv_gMvkW-ekJcSg/sendMessage?chat_id=-1001181667975&text='+msg
    requests.get(url)

def main():   
    global ur 
    mid=listOfMatches()
    mid=input('Enter mid..\n')
    if mid=='':
        print("Automatically fetching")
        mid=listOfMatches()
        if mid==None:
            mid=input('Enter mid..\n')
            

    print(mid)
    ur='http://mapps.cricbuzz.com/cbzios/match/'+mid+'/leanback.json'
    prefetch()
    while(True):
        score()
        time.sleep(5)

main()






