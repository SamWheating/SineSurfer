from socket import *
from time import *
import re

s = socket(AF_INET, SOCK_STREAM)

s.connect(("", 9000))

while(True):
	seed = s.recv(4096)
	print(seed)
	try:
		if int(seed) > 10: break
	except:
		pass

seed = int(re.search(r'\d+', str(seed)).group()) 	# Use regex to strip integer from string 

print("recieved seed {}".format(seed))

while(True):
	count = s.recv(4096)
	print(int(count))
	try:
		if int(count) == 1: 
			sleep(1)
			break
	except:
		pass

print("GO!")

s.close();