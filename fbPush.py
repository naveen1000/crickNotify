from pyfcm import FCMNotification
push_service = FCMNotification(api_key="AAAALXgG6s8:APA91bHaUoZ9MwS78rdihRMc7GsN-NQ8oNDSEjEZcDMeU7DyAr_8EJRHCB_o13ydJXpGYLu4Nl3sA5rpNW6pPdK5Q9Fa50R6zdO6fiQnDU8OG7ZC7hieVYdTn_NeeBTY-XIRwowDh0KA")

registration_idLenovo="efNEoC5EUlg:APA91bGjWMcjMp2LxuyjRPjoAkdTL_px4t8iHITBNrku2gdPAsczs-hvPO8SKcyYxyhg1yMhTT3anZSxRnkJjS85aQyDErb4pGfvrfA8N7uDSmqb_vSaM4D5xODzUuCCwY88ApFw5MkU"
registration_idLoki = "cJgkzsCtdWI:APA91bFtwDKqHfyTUz4FNPV8OepucAQ8Wx840xddmjV0HztLHkkQsz2is7QFZK7o67SC4yjXV0oceWywSCkGTkfOpE9V_C51PddQIfaE3F5SkOWvAkqY7RYinze8Z0FjWCe57sy4p6lC"
registration_idLaptop="edgivMskGxQ:APA91bH-vIHwz1l4-kDmlqhwoJ41NwQGOGb2KCawiOMGAhmtGabeI_nGdUmp9AJ8GdtslFf3UMao-Wy9SAsd_eCa7ELxUUliFdW48k7sZCxAP_MPVLLjyuLVn86LOad3_xvQ_-eXAokX"
registration_ids = [registration_idLoki, registration_idLenovo,registration_idLaptop]

message_title = "CricNotify"
message_icon="firebase-logo.png"

def fbpush(message_body):
    try:
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,message_body = message_body ,message_icon=message_icon)
        print(result)
    except:
        print("An exception occurred while trying to notify firebase")
