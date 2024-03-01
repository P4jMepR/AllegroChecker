import imaplib, quopri
from re import L
from bs4 import BeautifulSoup
import ssl, email, json
import mailparser, asyncio,requests
# from scipy import rand
# Load system's trusted SSL certificates
ssl_context = ssl._create_unverified_context()

# Connect (unencrypted at first)
server = imaplib.IMAP4('127.0.0.1', port=1143)
# Start TLS encryption. Will fail if TLS session can't be established
server.starttls(ssl_context=ssl_context)
# Login. ONLY DO THIS AFTER server.starttls() !!
server.login('####@protonmail.com', '')
# Print list of mailboxes on server
# code, mailboxes = server.list()
# for mailbox in mailboxes:
#     print(mailbox.decode("utf-8"))
# Select mailbox
status, messages = server.select('INBOX')    

if status != "OK": exit("Incorrect mail box")


# Cleanup
async def CodeGen():
    try: 
        basecode = "XD2137"
        _, msgnums = server.search("HEADER FROM","noreply@steampowered.com")
        for msgnum in msgnums[0].split():
            _, data = server.fetch(msgnum, "(RFC822)")
            message = email.message_from_bytes(data[0][1])
            # server.set_flags(msgnum,['\\Seen'])
            # print(f"Message number: {msgnum}")
        # if "TanieGryPL@protonmail.com" in message.get('To'):
        #     print(message.get('To'))
            for part in message.walk():
                if part.get_content_type() == "text/html":
                    # print(part.get_content_type())
                    xd = part.as_string()
                    xd = xd.replace("3D", "")
                    soup = BeautifulSoup(xd, "html.parser")
                    # rows = soup.find_all('td', {'class': 'title-48 c-blue1 fw-b a-center'})
                    rows = soup.find_all('td', {'class': 'title-48 c-blue1 fw-b a-center'})
                    for row in rows:
                        asd = row.get_text()
                        basecode = str(asd)
                        basecode = basecode.replace(" ", "")
                        basecode = basecode.replace("\n", "") 
                        if len(basecode) < 27 or basecode == "XD2137":
                            basecode = "Wystąpił błąd podczas generowania kodu, prosimy zalogować się ponownie i spróbować wygenerować nowy kod za 5 minut jeszcze raz używając komendy !SteamGuard"
                        print(basecode)
    except Exception as e:
        print(e)
        pass

    return basecode
