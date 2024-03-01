@echo off
:start
taskkill /f /im python.exe
start /B C:\Users\Borys\AppData\Local\Programs\Python\Python38\python.exe C:\Users\Borys\Desktop\AllegroChecker\DiscordBot.py
ping 127.0.0.1 -n 3600> nul
goto start
