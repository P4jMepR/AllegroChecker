from matplotlib.pyplot import connect
import mysql.connector, functools, time, os

# import DiscordBot
global bazka, mydb, mail, nick, fetchresult


# def fetch():
#     global mydb, bazka, mail, nick, mydb, fetchresult
#     fetchresult = bazka.fetchall()
#     print(fetchresult)
#     return fetchresult


def convertTuple(tup):
    strang = functools.reduce("( , )", (tup))
    return strang


def update():
    wynik = []
    query = "SELECT `Zaplacone`, `Niezaplacone`, `Odsetek`, `Zarobek`,`SredniaGodzinowa`, `WyslaneMaile` FROM `stats`"
    bazka.execute(query)
    result = bazka.fetchall()
    for x in range(0,6):
        selected_items = str([item[x] for item in result]).strip("[").strip("]")
        wynik.append(selected_items)
    
    Zaplacone = int(wynik[0])
    Niezaplacone = int(wynik[1])
    Odsetek = float(wynik[2])
    Zarobek = float(wynik[3])
    SredniaGodzinowa = float(wynik[4])
    WyslaneMaile = int(wynik[5])
    #bazka.reset()
    return Zaplacone,Niezaplacone,Odsetek,Zarobek,SredniaGodzinowa,WyslaneMaile




def refresh():
    # bazka.fetchall()
    #os.system("cls")
    bazka.close()
    mydb.close()
    connecttodb()


def connecttodb():
    global mydb, bazka, mail, nick, mydb, fetchresult
    try:
        mydb = mysql.connector.connect(host="localhost",user="root",password="",database="allegro")
        bazka = mydb.cursor(buffered=True)
        # fetch()
        # fetchresult = bazka.fetchall()
        # print(fetchresult)
        # return fetchresult

    except Exception as e:
        print("Error occured while trying to connect to DB \n" + str(e))

def isUserPresent(creditType, credit):
    global bazka, mydb
    query = "SELECT * FROM `klienci` WHERE `" + creditType+ "` LIKE '" + credit + "'"
    rez = bazka.execute(query)
    rez = bazka.fetchall()
    if rez != "":
        if rez == []:
            return False
        else:
            return True
    else:
        return False

def AddStats(typeOfStat, val):
    try:
        typeOfStat = "`" + str(typeOfStat) + "`"
        global bazka, mydb, fetchresult
        if typeOfStat == "`Zarobek`":
            value = float(val)
        else:
            value = int(val)
        #Getting current values from DB
        query = "SELECT " +typeOfStat + " FROM `stats`"
        bazka.execute(query)
        result = bazka.fetchall()
        # refresh()
        value = str(result[0])
        value = value.lstrip("(").rstrip(")").rstrip(",")
        ####Query for floats:
        if typeOfStat == "`Zarobek`" or typeOfStat == "`Odsetek`" or typeOfStat == "`SredniaGodzinowa`":
            if typeOfStat == "`Zarobek`":
                value = float(val) + float(value)
                query = "UPDATE `stats` SET " + typeOfStat +" = " + str(value)
            else:
                value = float(val)
                query = "UPDATE `stats` SET " + typeOfStat +" = " + str(value) 
        else:
            value = int(value) + int(val)
            # print(value, " pieces sold")
            query = "UPDATE `stats` SET " + typeOfStat + " = " + str(value) 
        bazka.execute(query)
        mydb.commit()
    except Exception as e:
        print("\n" + str(e))
def checkdata(whattocheck, creditType, credit):
    global bazka, mydb, fetchresult
    #| ID | Email  | Nick | Produkt  | Data | StatusPlatnosci | CzyWyslane
    whattocheck = str(whattocheck)
    creditType = str(creditType)
    credit = str(credit)
    query = "SELECT `" + str(whattocheck) +"` FROM `klienci` WHERE `"+ str(creditType) +"` LIKE '" + str(credit) + "'"
    bazka.execute(query)
    result = bazka.fetchall()
    for row in result:
        row = str(convertTuple(row))
        print(row)
        if whattocheck == "AmountGenerated":
            print("DBHandling ", row)
            return "0"
        else:
            return(row)
    #bazka.reset()

def addnewuser(Email,Nick,Produkt,Data,StatusPlatnosci,CzyWyslane):
    global bazka, mydb, fetchresult
    try:
        query = "INSERT into `klienci` (Email, Nick, Produkt, Data, StatusPlatnosci, Sent) VALUES (%s, %s, %s,%s, %s, %s)"
        data = (Email, Nick, Produkt, Data, StatusPlatnosci, CzyWyslane)
        bazka.execute(query, data)
        #os.system("cls")
        mydb.commit()
        print('\033[92;1;1m' + "Successfully added new user!"+ '\033[0m')
        #bazka.reset()
    except Exception as e:
        print("Error occured while trying to add new user! \n" + str(e))
        #bazka.reset()
    

def updateuser(field2update, info, typeofcred, cred):
    global bazka, mydb, fetchresult

    # if field2update != "Sent" or field2update !="Nick" or field2update != "Produkt" or field2update != "Data" or field2update != "StatusPlatnosci" or field2update != "Sent":
    if True == False:
        print("Error occured while trying to update user! Wrong field to update!")
        print(field2update,info,typeofcred,cred)
        #bazka.reset()
    else:
        try:
            typeofcred = "`"+ str(typeofcred) + "`"
            cred = "'" + str(cred) + "'"
            field2update = "`" + str(field2update) + "`"
            info = "'" + str(info) + "'"
            query = "UPDATE `klienci` SET " + field2update +" = " + info + " WHERE " + typeofcred  + " LIKE " + cred 
            bazka.execute(query)
            mydb.commit()
        except Exception as e:
            #os.system("cls")
            print("Error occured while trying to update data of user in DB! \n" + str(e))


if __name__ != '__main__':
    os.system("cls")
    print('\033[92;1;1m' + "DBHandling.py has been imported correctly!"+ '\033[0m')
    time.sleep(1)
