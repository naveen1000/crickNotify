from firebase import firebase 
firebase = firebase.FirebaseApplication('https://naveen-kumar-simma.firebaseio.com/',None)    
 
def fputOnRdb(detailed_score):
    try:
        firebase.put('/','object',detailed_score)
    except:
        print("An exception occurred updating Fdb")
