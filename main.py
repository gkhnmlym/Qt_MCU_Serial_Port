import sys
from time import *
import serial   
import sqlite3  

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMainWindow, QMessageBox, QTableWidgetItem             
from PyQt5 import QtCore # timer için

from girissayfasi import * 
from kayitol import * 
from proje import *  
from hakkinda import *
   
#arduino anasayfası için bağlantılar
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

#giriş sayfası için bağlantılar
app1=QtWidgets.QApplication(sys.argv)
MainWindow1=QtWidgets.QMainWindow()
ui1= Ui_girispenceresi()
ui1.setupUi(MainWindow1)
MainWindow1.show()

#kayıt sayfası için bağlantılar
app2=QtWidgets.QApplication(sys.argv)
MainWindow2=QtWidgets.QMainWindow()
ui2= Ui_kayitoll() 
ui2.setupUi(MainWindow2)

#hakkında sayfası için bağlantılar
app3=QtWidgets.QApplication(sys.argv)
MainWindow3=QtWidgets.QMainWindow()
ui3= Ui_hakkinda()
ui3.setupUi(MainWindow3)

#Veritabanı bağlantı kurma
conn=sqlite3.connect('seri.db') 
curs=conn.cursor() 
curs.execute("CREATE TABLE IF NOT EXISTS seri (id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,	saat	TEXT NOT NULL,	sicaklik	TEXT NOT NULL,	nem	TEXT NOT NULL)")
conn.commit() #bağlantıyı commit ediyoruz.

#giriş-kayıt veritabanı bağlantısı
conn2=sqlite3.connect('giris.db') 
curs2=conn2.cursor() 
curs2.execute("CREATE TABLE IF NOT EXISTS giris (id2	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,	username	TEXT NOT NULL UNIQUE,	passwoord	TEXT NOT NULL, email TEXT, adsoyad TEXT)")
conn2.commit() #bağlantıyı commit ediyoruz.

def girisiac():
    MainWindow.close()
    MainWindow2.close()
    MainWindow3.close()
    MainWindow1.show()    

def kayitiac():
    MainWindow.close()
    MainWindow1.close()
    MainWindow3.close()
    MainWindow2.show()
    
def hakkindaac():
    MainWindow.close()
    MainWindow1.close()
    MainWindow2.close()
    MainWindow3.show()

def kayitol():
    
    ad=ui2.AdSoy.text()
    kullanici=ui2.KulAd.text()
    sifre1=ui2.Sif.text()
    sifre2=ui2.SifT.text()
    mail=ui2.Email.text()
    mail2 = str()
    kullanici2 = str()
    
    if sifre1==sifre2:
        curs2.execute("SELECT * FROM giris WHERE username='%s'" %(kullanici2))
        conn2.commit()
        if(len(curs2.fetchall())<0):
            if kullanici2==kullanici:
                ui2.statusbar.showMessage(" "*5 + " Kayıt gerçekleştirilemedi.Kullanıcı adı daha önce alınmış. ", 1500)
        curs2.execute('INSERT INTO giris (username, passwoord, email, adsoyad) VALUES ( ?, ?, ?, ?)', (kullanici,sifre1,mail,ad) )
        conn2.commit()
        ui2.statusbar.showMessage(" "*5 + " Kayıt gerçekleştirildi.", 1500)
        ui2.AdSoy.clear()  #kayıt gerçekleştikten sonra lineeditleri temizliyoruz
        ui2.KulAd.clear()
        ui2.Sif.clear()
        ui2.SifT.clear()
        ui2.Email.clear()
        curs2.execute("SELECT * FROM giris WHERE username='%s'" %(kullanici2))
        conn2.commit()
        if(len(curs2.fetchall())<0):
            if kullanici2==kullanici:
                ui2.statusbar.showMessage(" "*5 + " Kayıt gerçekleştirilemedi.Kullanıcı adı daha önce alınmış. ", 1500)
    else:
        ui2.statusbar.showMessage(" "*5 + " Kayıt gerçekleştirilemedi. Şifre alanları aynı değil. ", 1500)
        
def giris():
    #giriş sayfası kodları
    global username
    username=ui1.KulAdi.text()
    passwoord=ui1.Sifre.text()
    """kullanıcının lineeditlere yazdığı username ve password bilgilerini alıp 2. veritabanı üzerinde
    arama yapıyoruz. curs2 ile."""    
    curs2.execute("SELECT * FROM giris WHERE username='%s' and passwoord='%s'" %(username,passwoord))
    conn2.commit()
    
    if(len(curs2.fetchall())>0):  #hazır komut. Veritabanının içinde otomatik olarak aramayı yapar. 
        ui.statusbar.showMessage(" "*3 + " Giriş yapıldı", 1500) 
        MainWindow1.close()
        MainWindow.show()
        """eğer veritabanı içinde aranan kişi varsa statusbar'a yazı yazıyoruz ve arduino sayfasını açıp, giriş sayfasını kapatıyoruz"""
        
    else:
        ui1.statusbar.showMessage(" "*3 + " Giriş yapılamadı.  Hatalı kullanıcı adı veya şifre", 1500)  
           
def sifre_goster():
    """giriş sayfası üzerinde şifre istenilirse görüntülenebilir. Bunu bir checkbox ile sağlıyoruz. ui1 üzerinde
    bulunan checkbox eğer işaretlenirse QLineEdit fonksiyonu olarak normal seçiyoruz."""
    if ui1.checkBox.isChecked():
        ui1.Sifre.setEchoMode(QLineEdit.Normal)    
    else:
        ui1.Sifre.setEchoMode(QLineEdit.Password)

def zaman_yaz():
    
    global zaman
    zaman = ctime()
    ui.label_10.setText(zaman[10:19])
    global saat
    saat=zaman[10:19]

timer0 = QtCore.QTimer()
timer0.start(1000)
timer0.timeout.connect(zaman_yaz)

def port_ac():
    
    port = str(ui.port.currentText())
    baud = str(ui.baudrate.currentText())
    
    global ser
    ser = serial.Serial(port, baudrate=baud, timeout=0)
    
    if ser.is_open:
        ui.statusbar.showMessage(" "*1 + " Port açıldı...", 1500)
    
        global timer1    
        timer1 = QtCore.QTimer()
        timer1.start(1000)
        timer1.timeout.connect(sensoroku)
    
    else:
        ui.statusbar.showMessage(" "*1 + " Port açılamadı !!!", 1500)
      
def port_kapat():
    
    if ser.is_open:
        
        ser.close()
        timer1.stop()
        print("Port kapatıldı...")
        
        ui.seriPort.setText("")
                 
        ui.statusbar.showMessage(" "*1 + " Port kapatıldı...", 1500)        

def sensoroku():
    
    print ("Bekleyen byte sayısı :", ser.in_waiting)
    data = ser.read(10)   # Seri Porttan 10 bytelık veri okunuyor
    print(data)
    
    veri = str(data)
    
    if len(veri) > 3: # b'' değilse...
        print(" seri: ", veri)
        
        seri = (veri)
                    
        ui.seriPort.setText(veri)
        ui.label_5.setText(str(derece))

        curs.execute('INSERT INTO seri (saat, seri ) VALUES (?,?)', (saat, seri))
        conn.commit()

def cikis():
    try:
        port_kapat()
    except (NameError):  
        sys.exit(app.exec_())
    finally:
        sys.exit(app.exec_())
    
def kapat():
    MainWindow.close()
    MainWindow1.close()
    MainWindow2.close()
    MainWindow3.close()

#Buton bağlantıları
ui.portac.clicked.connect(port_ac)
ui.portkapat.clicked.connect(port_kapat)
ui.KayitOl.clicked.connect(kayitiac)
ui.pb_cikis.clicked.connect(cikis)
ui1.GrsG.clicked.connect(giris)
ui1.pb_cikis.clicked.connect(cikis)
ui1.checkBox.clicked.connect(sifre_goster)
ui2.Ztnuye.clicked.connect(girisiac)
ui2.KayitOl.clicked.connect(kayitol)
ui.ProHak.triggered.connect(hakkindaac)
ui1.ProCik.triggered.connect(cikis)
ui1.ProHak.triggered.connect(hakkindaac)
ui1.ProKay.triggered.connect(kayitiac)
ui2.ProGir.triggered.connect(girisiac)
ui2.ProHak.triggered.connect(hakkindaac)
ui3.ProGir.triggered.connect(girisiac)
ui3.ProKay.triggered.connect(kayitiac)
ui.ProCik.triggered.connect(kapat)
ui1.ProCik.triggered.connect(kapat)
ui2.ProCik.triggered.connect(kapat)
ui3.ProCik.triggered.connect(kapat)
ui3.DonGir.clicked.connect(girisiac)
sys.exit(app.exec_())