import requests
import time
while True:
	r = requests.get('http://localhost:1234/')
	print(r.text)
	time.sleep(1)