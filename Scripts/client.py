from socket import *
from time import *

s = socket(AF_INET, SOCK_STREAM)

s.connect(("", 9000))

while(True):
	message = s.recv(4096)
	print(message)
	sleep(1)