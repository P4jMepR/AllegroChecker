from fbchat import log, Client
from fbchat.models import *
from datetime import datetime
import os, sys, re, time, requests, pydirectinput, random, cv2, asyncio
import dataimport
import DBHandling
# import DiscordBot
global increment, bazka, mydb
increment = 1

def sendmail(kupujacymail, gra, nick, platform):
    try:
        import smtplib 
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        port_number = 1025
        msg = MIMEMultipart()
        msg['From'] = 'TanieGryPL@protonmail.com'
        msg['To'] = str(kupujacymail)
        msg['Subject'] = "Zakup gry " + str(dataimport.getdetails(gra, "printname")) + "\n"
        message = "Użytkowniku " + nick + "! Dziękujemy za zakup gry " + str(dataimport.getdetails(gra, "printname")) + "." + "\nPoniżej znajdują się dane, których należy użyć, aby uzyskać dostęp do konta na platformie " + platform + ": \nLogin: " + dataimport.getdetails(gra, "login") + "\n" + "Hasło: " + dataimport.getdetails(gra, "pass") + " \n"
        if platform == "Steam":
            message = message + 'Przed zalogowaniem należy dołączyć na nasz serwer Discord (Zaproszenie: https://discord.gg/Mm9htA9uMN) gdzie na kanale info znajdują się wszystkie niezbędne instrukcje do otrzymania kodu Steam Guard, który należy wpisać przy logowaniu.' + '\n'
        message = message + " \n" + "Na Discordzie, chętnie również odpowiemy na Państwa pytania, rozwiążemy wątpliwości lub ewentualne problemy :)" + "\n" + "Pozdrawiamy, TanieGryPL"
        msg.attach(MIMEText(message))
        mailserver = smtplib.SMTP_SSL('localhost',port_number)
        mailserver.login("TanieGryPL@protonmail.com", "")
        mailserver.sendmail('TanieGryPL@protonmail.com',kupujacymail,msg.as_string())
        mailserver.quit()
    except Exception as e:
        print("Error occured while trying to send mail \n" + str(e))
        return False


global notifymess, checktime, automated
checktime = 1
automated = True
notifymess = ""
while automated == True:
    def klik(elem):
        button = driver.find_element(By.XPATH, elem)
        button.click()
    def dirklik(elem1,elem2):
        pydirectinput.click(elem1,elem2)
    
    # EmailKonta = "###@gmail.com"
    # HasloKonta = ""
    EmailKonta = "####@gmail.com"
    HasloKonta = ''
    
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    import pyautogui  as pya
    
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('log-level=3')
    dirname = os.path.dirname(__file__) + "\chromedriver.exe"
    # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    options.add_argument('--no-first-run --no-service-autorun')
    #################################################################################
    time.sleep(checktime)
    driver = webdriver.Chrome(dirname, options=options)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.get("https://allegro.pl/")
    time.sleep(2)
    driver.get("https://allegro.pl/logowanie")
    time.sleep(1)
    acceptcookies = "/html/body/div[2]/div[1]/div/div[2]/div[2]/button[1]"
    klik(acceptcookies)
    EmailPlaceHolder = "/html/body/div[2]/div[3]/div/div/div/div/div/div/div/div/div[1]/div/section[1]/form/div/div/div[1]/div[1]/input"
    klik(EmailPlaceHolder)
    pya.typewrite(EmailKonta)
    #Obejście zabezpieczeń allegro, proste jak barszcz, a działa znakomicie :)
    pydirectinput.click(670, 365)
    pya.typewrite(HasloKonta)
    x1, y2 = pya.locateCenterOnScreen('C:\\Users\\Borys\\Desktop\\AllegroChecker\\Obrazki\\loginbutton.png', confidence = 0.5)
    dirklik(x1,y2)
    time.sleep(1)
    #fixing pyautogui for it's developer
    lock = pya.locateOnScreen("C:\\Users\\Borys\\Desktop\\AllegroChecker\\Obrazki\\allegroklodka.png", confidence = 0.5)
    if lock != None:
        pydirectinput.click(879,463) #cancels 2Factor prompt
    else:
        print("Brak pop-up'u o 2factor")
    
    time.sleep(1)
    dirklik(1681,337) #czy zapamiętać hasło popup
    time.sleep(1)

    x1, y2 = pya.locateCenterOnScreen('C:\\Users\\Borys\\Desktop\\AllegroChecker\\Obrazki\\mojeallegrodrop.png', confidence = 0.5)
    dirklik(x1,y2)
    time.sleep(1)
    x1, y2 = pya.locateCenterOnScreen('C:\\Users\\Borys\\Desktop\\AllegroChecker\\Obrazki\\sprzedaz.png', confidence = 0.5)
    dirklik(x1,y2)
    time.sleep(5)
    x1, y2 = pya.locateCenterOnScreen('C:\\Users\\Borys\\Desktop\\AllegroChecker\\Obrazki\\wystaw.png', confidence = 0.5)
    dirklik(x1,y2)
    time.sleep(2)
    x1, y2 = pya.locateCenterOnScreen('C:\\Users\\Borys\\Desktop\\AllegroChecker\\Obrazki\\kontyn.png', confidence = 0.5)
    dirklik(x1,y2)
    driver.get("https://allegrolokalnie.pl/konto/oferty/sprzedane")
    time.sleep(2)
    klik("/html/body/div[5]/div/div/div/div[2]/button[2]")



    time.sleep(3)
    DBHandling.connecttodb()
    while True:
        x = 0
        increment = 1
        for x in range(10):
            try:
                try:
                    imienazwisko = driver.find_element(By.XPATH, '//*[@id="app-root"]/main/div/div[2]/div/div/div/div['+ str(increment) + ']/div[2]/div/div[2]/p').text
                    nick = imienazwisko.split("(")[0].rstrip(" ").lstrip(" ")
                    print(imienazwisko)
                except:
                    print("xd")
                    pass
                try:
                    imienazwisko = imienazwisko.split("(")[1].lstrip(" ").rstrip(" )")
                except:
                    nick = imienazwisko
                    pass
                try:
                    email = driver.find_element(By.XPATH, '//*[@id="app-root"]/main/div/div[2]/div/div/div/div['+ str(increment) + ']/div[2]/div/div[3]').text
                    email = email[7:]
                    print(email)
                    if "@" not in email:
                        print("Brak emaila, użytkownik nie zapłacił")
                        email = "Brak emaila"
                except:
                    print("Brak emaila, użytkownik nie zapłacił")
                    email = "Brak emaila"
                    pass
                try:
                    produkt = driver.find_element(By.XPATH, '//*[@id="app-root"]/main/div/div[2]/div/div/div/div['+ str(increment) + ']/div[1]/div[1]/a/div[2]/h3').text
                    print(produkt)
                except:
                    produkt = "Brak produktu"
                    pass
                if produkt != "Brak emaila":
                    try:
                        cena = driver.find_element(By.XPATH, '//*[@id="app-root"]/main/div/div[2]/div/div/div/div['+ str(increment) + ']/div[1]/div[2]/div/div/span').text
                        cena = float(cena.rstrip(" zł").replace(",", "."))
                    except:
                        cena = float(0)
                        DBHandling.AddStats("Zarobek", cena)
                        pass
                else:
                    cena = 0
                    DBHandling.AddStats("Zarobek", cena)
                    
                try:
                    platnosc = driver.find_element(By.XPATH, '//*[@id="app-root"]/main/div/div[2]/div/div/div/div['+ str(increment) + ']/div[2]/div/p[3]/span').text.lstrip("Płatność: ")
                except:
                    print("Brak płatności, użytkownik nie zapłacił")
                    platnosc = "Nieopłacone"
                    pass
                try:
                    data = driver.find_element(By.XPATH, '//*[@id="app-root"]/main/div/div[2]/div/div/div/div[' + str(increment) + ']/div[2]/div/p[1]/time').text.lstrip("Kupione: ")
                except:
                    print("Brak daty")
                    data = "NULL"
                    pass
                if "Dying Light" in produkt:
                    gra = "dyinglight2"
                if "Just Cause 3" in produkt:
                    gra = "justcause3"
                if "Borderlands 3" in produkt:
                    gra = "borderlands3"
                if "Ready or Not" in produkt:
                    gra = "readyornot"
                if "Kangurek Kao" in produkt:
                    gra = "kangoo"
                if "STRAY - STEAM PC 24/7" in produkt:
                    gra = "stray"
                if "Brak Produktu" in produkt:
                    gra = "Brak Gry"
                
                increment = increment + 1
                if DBHandling.isUserPresent("Email", email) != True or DBHandling.isUserPresent("Nick", nick) != True:
                    print("Użytkownika nie ma w bazie, dodaję")
                    DBHandling.addnewuser(email,nick,produkt,data,platnosc,"False")
                    if platnosc == "Zakończona":
                        DBHandling.AddStats("Zaplacone", 1)
                        print("Stats updated, paid")
                    else:
                        DBHandling.AddStats("Niezaplacone", 1)
                        print("Stats updated, not paid")
                if str(DBHandling.checkdata("StatusPlatnosci", "Nick",nick)) == "Zakończona":
                    if str(DBHandling.checkdata("Sent", "Nick", nick)) != "True":
                        try:
                            sendmail(email, gra, nick, dataimport.getdetails(gra,"platform"))
                            sent = True
                            DBHandling.updateuser("Sent",sent, "Email", email)
                            print("Pomyślnie wysłano maila")
                            DBHandling.AddStats("WyslaneMaile", 1)
                            DBHandling.AddStats("Zarobek", float(cena))
                            content = DBHandling.update()
                            Zaplacone = content[0]
                            Niezaplacone = content[1]
                            Odsetek = content[2]
                            Zarobek = content[3]
                            
                            if Niezaplacone > 0:
                                Odsetek = float(Zaplacone) / float(Niezaplacone)
                                Odsetek = "{:.2f}".format(Odsetek)
                                Odsetek = float(Odsetek)
                                print(Odsetek)
                            else:
                                Odsetek = float(Zaplacone)
                                print(Odsetek)
                            if Zarobek != 0:
                                SredniaGodzinowa = float(float(Zarobek)/8)
                                SredniaGodzinowa = "{:.2f}".format(SredniaGodzinowa)
                                SredniaGodzinowa = float(SredniaGodzinowa)
                            else:
                                SredniaGodzinowa = 0.00
                            DBHandling.AddStats("SredniaGodzinowa", SredniaGodzinowa)
                            DBHandling.AddStats("Odsetek", Odsetek)
                            print("Niezaplacone:", Niezaplacone, "Zaplacone:", Zaplacone, "Odsetek:", Odsetek, "Zarobek:", Zarobek, "SredniaGodzinowa:", SredniaGodzinowa)

                        except Exception as e:
                            sent = "Error while sending email"
                            print("Error while sending email \n")
                            print("Error: " + e)
                            DBHandling.updateuser("Sent",sent, "Email", email)
                else:
                    print("Email nie został wysłany, ponieważ płatność nie została zakończona")
                    sent = False
                    DBHandling.updateuser("Sent",sent, "Nick", nick)
            except Exception as e:
                print("Error while getting data \n" + str(e))
                print("Something went wrong with auction no. " + str(increment))
                increment = increment + 1
            imienazwisko,nick,email,produkt,platnosc,data, gra, SredniaGodzinowa, Niezaplacone, Zaplacone, Odsetek, Zarobek, sent, content, cena= None,None,None,None,None,None,None, None,None,None,None,None,None,None,None
            sent = False
            #DBHandling.refresh()
            # DiscordBot.bot()
        print("Sleeping for 5 minutes")
        print("---------------------------------------------------------------------------------------------------------------------")
        time.sleep(500)
        driver.refresh()
        time.sleep(5)
        
    

input()
