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
	
Establish connection with two clients - label sockets p1 and p2				yes.

Provide identical seed for random generation of obstacle positions.			yes.

When both seed reciepts confirmed give 3s countdown to start of game.		yes.

While(at least one player lives):
	Trade location data for P1 and P2. (y coord and t)						no.

Once both players have lost:
	Send message ((PLayer x won!))											no.	

"""



from socket import *
from time import *
import random

# Control Variables
SERVER_PORT = 9000
ONEPLAYER = False


random.seed()

print("Initializing Server....")

s = socket(AF_INET, SOCK_STREAM)
s.bind(("", SERVER_PORT))
s.listen(5)       	# start listening for connections on socket. (max 5 connections)

print("listening for connections on port ", SERVER_PORT)

# ESTABLISHING CONNECTION WITH TWO CLIENTS

print("Searching for player 1")

while(True):
	player1, a1 = s.accept()		# Returns a socket object player1 and a socket adress a1
	if player1 != None: 
		print("Player 1 connected from port ", str(a1))
		break		

if not ONEPLAYER:

	print("Searching for player 2")

	while(True):
		player2, a2 = s.accept()									# Returns a socket object player2 and a socket adress a2
		if a2 != a1: 												# only stop when two unique sockets are obtained
			print("Player 2 connected from port ", str(a2))
			break

	print("connected to two sockets")

seed = random.randrange(10000)				# Generate seed to send to client-side RNG

print("sending random seed {}".format(seed))

player1.send(str(seed).encode('utf-8'))
if not ONEPLAYER: player2.send(str(seed).encode('utf-8'))

sleep(2)

print("Sending game start signal")

for i in range(3):
	player1.send(str(3-i).encode('utf-8'))
	if not ONEPLAYER: player2.send(str(3-i).encode('utf-8'))
	sleep(1)

print("starting game")

# GAME STATE LOOP:
# listen for messages from either player and sends their location to the other player.

sleep(1)

while(True):
	p1_pos = player1.recv(4096)
	p2_pos = player2.recv(4096)

	# Get player positions

	try:
		p1_pos = int(p1_pos)

	except:
		p1_pos = 9000

	if not ONEPLAYER:
		try: 
			p2_pos = int(p2_pos)
		except:
			p2_pos = 9000			# ignore value

	# Send player positions if valid.

	if(p1_pos != 9000):
		player2.send(p1_pos)

	if((p2_pos != 9000) & (not ONEPLAYER)):
		player1.send(p2_pos)



player1.close()
if not ONEPLAYER: player2.close()

print("closed sockets")


"""

while(True):



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

"""
