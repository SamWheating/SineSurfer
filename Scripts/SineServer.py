"""

SineSurfer!

SineServer.py:

Server-side script for running the game. 
Will interact with SineSurfer.py.

---------

Game made for CENG356 - Engineering System Software
Uses Pygame fo rgame logic + rendering, sockets for network communications.
Launch SineServer.py before launching instances of SineSurfer.py

---------

Server Operations:															implemented?
	
Establish connection with two clients - label sockets p1 and p2				no.

Provide identical seed for random generation of obstacle positions.			no.

When both seed reciepts confirmed give 3s countdown to start of game.		no.

While(at least one player lives):
	Trade location data for P1 and P2. (y coord and t)						no.

Once both players have lost:
	Send message ((PLayer x won!))											no.	

"""



from socket import *
from time import *

# Control Variables
SERVER_PORT = 9000

print("Initializing Server....")

s = socket(AF_INET, SOCK_STREAM)
s.bind(("", SERVER_PORT))
s.listen(5)       	# start listening for connections on socket. (max 5 connections)

print("listening for connections on port ", SERVER_PORT)

while(True):
	c, a = s.accept()

	print("recieved connection from ", a)

	while(c != None):
		sleep(1)
		message = "Hello " + str(a[1] + 1)
		print(message)
		c.send(message.encode('utf-8'), a[1])



	print("recieved connection from ", a)
	print("c = ", c)

	message = "Hello"

	c.send(message.encode('utf-8'), a[1])
	
	c.close()


