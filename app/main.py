from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from plyer import notification
from kivy.properties import NumericProperty

from config import API_key
from summoner import Summoner

class ErinyCatcher(App):
    
    time_period= 10
    countdown = NumericProperty(time_period)  # 5 saniye

    # def __init__(self):
    #     # summoner objesi oluşturuyoruz
    #     self.summ_obj = Summoner("Eriny", API_key)
    def build(self):
        
        if not hasattr(self, 'summ_obj'):
        # summoner objesi oluşturuyoruz
            self.summ_obj = Summoner("Eriny", API_key)
    
        
        # Ana düzenimiz olan bir kutu düzeni oluşturuyoruz
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        background = Image(source='../images/eriny.png', allow_stretch=False, keep_ratio=True, )
        self.layout.add_widget(background)
        # Sayaç için bir etiket oluşturuyoruz ve düzene ekliyoruz
        self.label = Label(text='Uygulama başlatıldı.', font_size='20sp', color=(1, 1, 1, 1))
        # Bir etiket oluşturuyoruz ve düzene ekliyoruz
        self.layout.add_widget(self.label)
        self.label2 = Label(text='', font_size='30sp', color=(0, 1, 0, 1))
        # Belirli aralıklarla bildirim göndermek için Clock.schedule_interval kullanıyoruz
        Clock.schedule_interval(self.update_countdown, 1)  # Her 1 saniyede bir
        return self.layout

    def update_countdown(self, dt):
        # sayaç azalt
        self.countdown -= 1

        # Sayaç değerini yazdır
        self.label.text = f"Kalan zaman: {self.countdown} saniye"
        
        if self.countdown == 0:
            response = self.send_api_request()

            if response:
                self.label2.text = "HAİN OYUNDA"
                if self.label2 not in self.layout.children:
                    self.layout.add_widget(self.label2)
                Clock.schedule_once(self.clear_label, 5)  # 5 saniye sonra label2'yi temizle
                
            else:
                self.label.text = "Oyunda Değil"

            self.reset_countdown()

    def format_time(self, seconds):
        # saniyeyi dakika ve saniye olarak çevir
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def reset_countdown(self):
        # Sayaç değerini sıfırla
        print("sayaç sıfırlandı")
        self.countdown = self.time_period

    def send_api_request(self):
        
        summoner_id = self.summ_obj.get_summoner_id() 
        print("Summoner id : ", summoner_id)
        if summoner_id is None:
            return False 
        result = self.summ_obj.summoner_isOnline(summoner_id) 
        print(result)
        return result

    def send_scheduled_notification(self):
        # Bildirim gönderme
        notification.notify(
            title='Bildirim Başlığı',
            message='Bildirim',
            app_icon=None,
            timeout=10
        )
        # Etiketi güncelleme
        self.label.text = 'Bildirim gönderildi.'

    def clear_label(self, dt):
        # Etiketi temizle
        print("Label2 temizlendi")
        self.layout.remove_widget(self.label2)
        Clock.schedule_interval(self.update_countdown, 1)  # update_countdown fonksiyonunu tekrar başlat

if __name__ == '__main__':
    eriny = ErinyCatcher()
    eriny.run()
    