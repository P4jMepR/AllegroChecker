from datetime import datetime
import os, sys, re, time, discord, mysql.connector, logging,asyncio,mysql,functools,threading,nest_asyncio
import requests as r
nest_asyncio.apply()

global Zaplacone, Niezaplacone, Odsetek, Zarobek, SredniaGodzinowa, WyslaneMaile, WygenerowaneKody

def checkdata(whattocheck, creditType, credit):
    global bazka, mydb, fetchresult
    #| ID | Email  | Nick | Produkt  | Data | StatusPlatnosci | CzyWyslane	
    query = "SELECT `" + str(whattocheck) +"` FROM `klienci` WHERE `"+ str(creditType) +"` LIKE '" + str(credit) + "'"
    bazka.execute(query)
    result = bazka.fetchall()
    for row in result:
        row = str(convertTuple(row))
        refresh()
        return row
        

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
        value = str(result[0])
        value = value.lstrip("(").rstrip(")").rstrip(",")
        ####Query for floats:
        if typeOfStat == "`Zarobek`":
            value = float(value) + float(val)
            query = "UPDATE `stats` SET " + typeOfStat +" = " + str(value)
        else:
            value = int(value) + int(val)
            # print(value, " ints")
            query = "UPDATE `stats` SET " + typeOfStat + " = " + str(value) 
        bazka.execute(query)
        mydb.commit()
    except Exception as e:
        print("\n" + str(e))


def convertTuple(tup):
    strang = functools.reduce("( , )", (tup))
    return strang
def update():
    refresh()
    global Zaplacone, Niezaplacone, Odsetek, Zarobek, SredniaGodzinowa, WyslaneMaile, WygenerowaneKody
    wynik = []
    query = "SELECT `Zaplacone`, `Niezaplacone`, `Odsetek`, `Zarobek`,`SredniaGodzinowa`, `WyslaneMaile`, `WygenerowaneKody` FROM `stats`"
    bazka.execute(query)
    result = bazka.fetchall()
    for x in range(0,7):
        selected_items = str([item[x] for item in result]).strip("[").strip("]")
        wynik.append(selected_items)
    
    Zaplacone = int(wynik[0])
    Niezaplacone = int(wynik[1])
    Odsetek = float(wynik[2])
    Zarobek = float(wynik[3])
    SredniaGodzinowa = float(wynik[4])
    WyslaneMaile = int(wynik[5])
    WygenerowaneKody = int(wynik[6])
    return Zaplacone,Niezaplacone,Odsetek,Zarobek,SredniaGodzinowa,WyslaneMaile, WygenerowaneKody
    
def refresh():
    mydb.commit()
    # bazka.close()
    # mydb.close()
    # connecttodb()


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

def connecttodb():
    global mydb, bazka, mail, nick, mydb, fetchresult
    try:
        mydb = mysql.connector.connect(host="localhost",user="discordbot",password="",database="allegro")
        bazka = mydb.cursor(buffered=False)
        # print("DB connection sucessful")

    except Exception as e:
        print("Error occured while trying to connect to DB \n" + str(e))

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)




client = discord.Client()



    


class MyClient(discord.Client):
    global Zaplacone, Niezaplacone, Odsetek, Zarobek, SredniaGodzinowa, WyslaneMaile
    
    async def DiscordRegistered(self, email, senderid, message):
        email = "'" + str(email) + "'"
        discordid = int(senderid)
        senderid = "'" + str(senderid) + "'"
        if "@" in email:
            try:
                query = "SELECT `Discord` FROM `klienci` WHERE `Email` = " + email
                bazka.execute(query)
                result = bazka.fetchall()
                if result == []:
                    channel = await message.author.create_dm()
                    print("Email użytkownika nie występuje w bazie")
                    await channel.send("Ten adres E-mail nie występuje w naszej bazie :disappointed:. Upewnij się czy podałeś poprawny adres email i spróbuj ponownie.")
                    return False
                if "None" in str(result) or "NULL" in str(result):
                    print("User not registered")
                    query = "UPDATE `klienci` SET `Discord` = " + senderid + " WHERE `Email` LIKE " + email
                    bazka.execute(query)
                    mydb.commit()
                    channel = await message.author.create_dm()
                    await channel.send("Zostałeś pomyślnie zarejestrowany! Od teraz możesz korzystać ze wszystkich funkcji serwera :partying_face: ")
                    role = discord.utils.get(message.guild.roles, name="Kupujący")
                    await message.author.add_roles(role)
                    return True
                else:
                    print("User already registered")
                    channel = await message.author.create_dm()
                    await channel.send("Dokonałeś już rejestracji, raz w zupełności wystarczy :wink:")
                    refresh()
                    return True
            except Exception as e:
                print("Error while trying to get Discord ID (DiscordRegistered) \n")
                print(e)
                return False
            
        else:
            print("Nieprawidłowy email przekazany do funkcji DiscordRegistered")



    async def CodeSend(self):
        import CodeGen
        Code = await CodeGen.CodeGen()
        return Code
    async def on_ready(self):
        print('Connected!')
        print('Username: {0.name}\nID: {0.id}'.format(self.user))
        connecttodb()


    async def sendMessage(self,userid, channel, asd):
        if channel == "dev":
            
            channel = client.get_channel(977551946674221067)
            await channel.send(f"<@{userid}> {asd}")

        if channel == "logi":
            channel = client.get_channel(993887947298451588)
            await channel.send(f"<@{userid}> {asd}")

        
    async def on_message(self, message):
        try:
            global Zaplacone, Niezaplacone, Odsetek, Zarobek, SredniaGodzinowa, WyslaneMaile, WygenerowaneKody
            if message.author == client.user:
                return
            if message.content == "!SteamGuard" and checkdata("Discord", "Discord",message.author.id):
                amtgen = checkdata("AmountGenerated", "Discord", str(message.author.id))
                if amtgen == None or amtgen == "None":
                    amtgen = "0"
                if message.content == "!SteamGuard" and int(amtgen) < 3:
                    code = await self.CodeSend()
                    await message.channel.send(f"{message.author.mention} Twój kod Steam Guard: ```{code}```")
                    # try:
                    AddStats("WygenerowaneKody", 1)
                    xd = checkdata("AmountGenerated", "Discord", message.author.id)
                    try:
                        if xd == None or xd == "None":
                            xd = "0"
                        displayxd = int(xd) + 1
                        displayxd = str(displayxd)
                        query = f"UPDATE `klienci` SET `AmountGenerated`= {str(displayxd)} WHERE `Discord` LIKE {str(message.author.id)}"
                        bazka.execute(query)
                        mydb.commit()
                        refresh()
                    except Exception as e:
                        print("Error while trying to update AmountGenerated in DB", e)
                        pass
                    # except Exception as e:
                    #     # print(e)
                    #     # pass
                else:
                    if amtgen == None:
                        print("Użytkownik nie jest zarejestrowany.")
                        await message.channel.send(f"{message.author.mention} Aby użyć tej komendy musisz się najpierw zarejestrować.")
                        return
                    elif int(amtgen) > 2:
                        print("Użytkownik wygenerował za dużo kodów.")
                        await message.channel.send(f"{message.author.mention} Twój kod Steam Guard nie został wygenerowany, ponieważ przekroczyłeś limit dobowy, spróbuj ponownie za 24 godziny.")
                        return
                        

            if message.content == "!help":
                if message.author.id == 169819237353914369 and message.author != client.user:
                    embedVar = discord.Embed(title="Commands:", description="", color=0x00ff00)
                    embedVar.add_field(name="!flipper enable", value="Starts script for checking if flipper is purchasable.", inline=False)
                    embedVar.add_field(name="!flipper disable", value="Stops script mentioned above.", inline=False)
                    embedVar.add_field(name="!stats", value="Displays statistics for Allegro Bot from it's database.", inline=False)
                    embedVar.add_field(name="!update", value="Forces database refresh.", inline=False)
                    await message.channel.send(content=None, embed=embedVar)
                else:
                    msg = await message.channel.send("Sorry, You are not allowed to use this command.")

            
            if message.content == "!acctype":
                print(message.author.id)
                if message.author.guild_permissions.administrator and message.author != client.user:
                    await message.channel.send("I've got great news, You are an admin!")
                else:
                    msg = await message.channel.send("Sorry, You are not an admin.")

            if message.content.startswith("!rejestracja"):
                if message.author != client.user:
                    refresh()
                    email = message.content[13:]
                    senderid = message.author.id
                    await self.DiscordRegistered(email, senderid, message)
                else:
                    pass
            if "!rejestracja" in message.content and message.author != client.user and message.channel.id != 993639473353084938:
                try:
                    await message.delete()
                    await message.channel.send(f"Użytkowniku {message.author.mention}! Ze względu na prywatność prosimy o używanie komendy !rejestracja wyłącznie w wiadomości prywatnej ze mną lub na kanale #rejestracja :)")
                except:
                    pass
            if message.content == "!update" and message.author.guild_permissions.administrator and message.author != client.user:
                msg = await message.channel.send('Updating...')
                try:
                    content = update()
                    Zaplacone = content[0]
                    Niezaplacone = content[1]
                    Odsetek = content[2]
                    Zarobek = content[3]
                    SredniaGodzinowa = content[4]
                    WyslaneMaile = content[5]
                    WygenerowaneKody = content[6]
                    msg = await msg.edit(content="Updated!")

                except Exception as e:
                    msg = await msg.edit(content="Error occured while trying to update.\n" + str(e))
                    pass
            
            
            if message.content.startswith('!stats'):
                if message.author.guild_permissions.administrator and message.author != client.user:
                    msg = await message.channel.send('Checking...')
                    embedVar = discord.Embed(title="Statystyki:", description="", color=0x00ff00)
                    embedVar.add_field(name="Ilość zakupionych gier:", value=Zaplacone, inline=False)
                    embedVar.add_field(name="Ilość nieopłaconych gier:", value=Niezaplacone, inline=False)
                    displayzarobek = str(Zarobek).replace(".", ",") + " złotych"
                    embedVar.add_field(name="Zarobek:", value=displayzarobek, inline=False)
                    embedVar.add_field(name="Wygenerowane kody Steam Guard:", value=str(WygenerowaneKody), inline=False)
                    displayOdsetek = "~" + str(Odsetek)
                    embedVar.add_field(name="Odsetek zapłacone/niezapłacone:", value=displayOdsetek, inline=False)
                    embedVar.add_field(name="Średni zarobek godzinowy:", value=SredniaGodzinowa, inline=False)
                    embedVar.add_field(name="Ilość wysłanych maili:", value=WyslaneMaile, inline=False)
                    await asyncio.sleep(0.5)
                    await msg.edit(content="",embed=embedVar)
                else:
                    msg = await message.channel.send("Sorry, You are not an admin.")
            # if message.content == "!grantrole":
            #     if message.author.guild_permissions.administrator and message.author != client.user:
            #         await message.channel.send("Granting role...")
            #         role = discord.utils.get(message.guild.roles, name="Kupujący")
            #         await message.author.add_roles(role)
            #         # await message.author.add_roles(message.author.id, role)
            #         msg = await message.channel.send("Done!")
            #     else:
            #         msg = await message.channel.send("Sorry, You are not an admin.")
            #         return

        except Exception as e:
            print("Exception occured \n", e)
            pass
    # async def on_message_edit(self, before, after):
    #     fmt = '**{0.author}** edited their message:\n{0.content} -> {1.content}'
    #     await before.channel.send(fmt.format(before, after))

client = MyClient()

client.run('TokenGoesHere')
        


if __name__ != '__main__':
    os.system("cls")
    print('\033[92;1;1m' + "DiscordBot.py has been imported correctly!"+ '\033[0m')
    time.sleep(1)
connecttodb()
