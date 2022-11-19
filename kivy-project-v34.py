from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import datetime
import locale
from kivy.clock import Clock
from kivy.uix.image import Image
import requests
from googletrans import Translator # pip install googletrans==4.0.0-rc1 ile sorunu çözdüm.



class Program(App):
    def build(self):

        # Ana BOX
        self.anaDuzen = BoxLayout() # Elemanların hepsini tutan ana pencere düzenimiz

        # Alt BOX
        # BoxLayout olarak tanımladık.
        self.ilkSatir = BoxLayout(orientation = "vertical") # ilkSatir içindeki widgetleri alt alta yerleştirdik.
        self.ikinciSatir = BoxLayout() # ikinciSatir ile ilkSatir default yani varsayılan olarak yan yana dizilecektir. Fakat ilkSatir içindeki widgetler bu durumdan etkilenmeyecek ve alt alta yerleştirilecektir.

        Clock.schedule_interval(self.saat_hesaplama,0) # 1 saniye sonra, self.saat_hesaplama adlı fonksiyonu çalıştır
        Clock.schedule_interval(self.hava_durumu,0) # 1 saniye sonra, self.saat_hesaplama adlı fonksiyonu çalıştır

        ###############################

        self.sehir_ismi = "Istanbul"
        
        api = "89f43f1f20b6e6c6e3a602d47906405b"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        url = base_url + "appid=" + api + "&q=" + self.sehir_ismi

        self.gelen_veri = requests.get(url)
        self.gelen_veri_json = self.gelen_veri.json()
        self.description = self.gelen_veri_json["weather"][0]["description"]

        self.havaDrm = str(self.description)
            
        translator = Translator()
        sentence = self.havaDrm
        example = translator.translate(sentence,dest="tr")
        example = example.text
        example = example.title()
        self.havaDrm = example

        ################################
        a = 1
        while a == 1:
            self.havadurumu = self.havaDrm # Hava durumu için hangi görsellerin kullanılacağı belirlendiği yer. Hava Durumu Görsel Belirleme Referans Adresi: https://openweathermap.org/weather-conditions
            
            if self.havadurumu == "Açık Hava":
                self.havadurumu = "D:/Python Projeler/Kivy/kivy-gorseller/gunesli.png"
                a = 0
            elif self.havadurumu == "Bulutlar":
                self.havadurumu = "D:/Python Projeler/Kivy/kivy-gorseller/bulutlu.png"
                a = 0
            elif self.havadurumu == "Dağınık Bulutlar":
                self.havadurumu = "D:/Python Projeler/Kivy/kivy-gorseller/bulutlu.png"
                a = 0
            elif self.havadurumu == "Kırık Bulutlar":
                self.havadurumu = "D:/Python Projeler/Kivy/kivy-gorseller/bulutlu.png"
                a = 0
            elif self.havadurumu == "Duş Yağmuru":
                self.havadurumue = "D:/Python Projeler/Kivy/kivy-gorseller/firtinali.png"
                a = 0 
            elif self.havadurumu == "Yağmur":
                self.havadurumu = "D:/Python Projeler/Kivy/kivy-gorseller/firtinali.png"
                a = 0
            elif self.havadurumu == "Fırtına":
                self.havadurumu = "D:/Python Projeler/Kivy/kivy-gorseller/firtinali.png"
                a = 0 
            elif self.havadurumu == "Gece":
                self.havadurumu = "D:/Python Projeler/Kivy/kivy-gorseller/gece-acik.png"
                a = 0
 
        # İçerikler/Widget Oluşturma (BOXların içine gelecek içerikler/widgetler.)
        self.hava = Image(source = "{}".format(self.havadurumu)) #hava görselini tanmladık
        self.time = Label(markup = True)
        self.derece = Label(markup = True)

        # Widget Tanımlama (Oluşturulan widgetleri Alt BOXlara tanımlıyoruz.)
        self.ilkSatir.add_widget(self.hava)
        self.ikinciSatir.add_widget(self.time)
        self.ilkSatir.add_widget(self.derece)

        # Şimdi hepsini ana düzene yerleştiriyoruz
        # Ana BOXa yerleştirme. (Widgetleri Alt BOXlara yerleştirdikten sonra, Alt BOXları Ana BOXa yerleştiriyoruz.)
        self.anaDuzen.add_widget(self.ilkSatir)
        self.anaDuzen.add_widget(self.ikinciSatir)

        # Ana BOXumuzu return ile geri döndürerek ekrana ekranda gösterilmesini sağlıyoruz.
        return self.anaDuzen
    
    # Saat Hesaplaması Yapılan Yer
    def saat_hesaplama(self,event):
        zaman = datetime.datetime.now()
        self.saat = "[size=90sp]{}:{}:{}[/size]".format(zaman.hour,zaman.minute,zaman.second)
        self.time.text = self.saat
    
    # Hava Durumu Hesaplaması Yapılan Yer
    def hava_durumu(self,event):

        if (self.gelen_veri_json["cod"] != "404"):

            temp = self.gelen_veri_json["main"]["temp"]
            description = self.gelen_veri_json["weather"][0]["description"]
            pressure = self.gelen_veri_json["main"]["pressure"]
            country = self.gelen_veri_json["sys"]["country"]

            self.sicaklik = str(int(temp) - 273)
            self.havaDrm = str(description)
            self.basinc = str(pressure)
            self.lokasyon = self.sehir_ismi + " " + str(country)
            
            translator = Translator()
            sentence = self.havaDrm
            example = translator.translate(sentence,dest="tr")
            example = example.text
            example = example.title()
            self.havaDrm = example

        

            self.derece.text = """[size=50sp]
            {}°C
            Hava Durumu: {} 
            Lokasyon: {}[/size]""".format(self.sicaklik,self.havaDrm,self.lokasyon)

        else:
            print("Böyle bir şehir bulunamadı!")


Program().run()
