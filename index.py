import requests
import datetime
from win10toast import ToastNotifier
from config import API_key


summoner_name = "Eriny"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": API_key
}  
subject = "Hain Oyunda"
message = "OYUNDA MEHMET ÜNİDEN BİZDEN HABERSİZ"

def create_notification(start_time):
    global subject, message
    toast = ToastNotifier()
    toast.show_toast(
        subject,
        message + "\n" + start_time ,
        duration = 20,
        icon_path = "eriny.ico",
        threaded = True,
)

def get_summoner_id():
    summoner_url = f"https://tr1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"

    user_response = requests.get(summoner_url, headers=headers) 
    
    # Hata kontrolü

    if user_response.status_code == 200:
        # Sayfa içeriğini BeautifulSoup ile işle
        last_time = user_response.json().get("revisionDate")
        summoner_id = user_response.json().get("id")
        print("user id : ", summoner_id)
        date = datetime.datetime.fromtimestamp(last_time/1000)
        print("last event(not activated) : ", date)
        return summoner_id
    
    else:
        print(f"Hata: {user_response.status_code}")
        print(user_response.json())
        return None


def summoner_isOnline(summoner_id):
    summoner_isOnline_url = f"https://tr1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
    result = requests.get(summoner_isOnline_url, headers=headers)
    if result.status_code == 200:
        print("user in game")
        start_time = result.json().get("gameStartTime")
        start_time = datetime.datetime.fromtimestamp(start_time/1000)
        print("game start time : ", start_time) 
        print(result)
        create_notification(str(start_time))
        
    else:
        print("user is offline or not in game")
        print(result.json() )
    
def main():
    summoner_id = get_summoner_id()
    if summoner_id:
        summoner_isOnline(summoner_id)
        return True
        
if __name__ == '__main__':
    main()
