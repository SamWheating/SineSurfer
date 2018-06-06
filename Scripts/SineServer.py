"""

SineSurfer!

SineServer.py:

Server-side script for running the game. 
Will interact with SineSurfer.py.

---------

Uses Pygame for game logic + rendering, sockets for network communications.
Launch SineServer.py before launching instances of SineSurfer.py

---------

Server Operations:															implemented?
	
Establish connection with two clients - label sockets p1 and p2				yes.

Provide identical seed for random generation of obstacle positions.			yes.

When both seed reciepts confirmed give 3s countdown to start of game.		yes.

While(at least one player lives):
	Trade location data for P1 and P2. (y coord and t)						yes.

Once both players have lost:
	Send message ((Player x won!))											yes.

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


# ESTABLISHING CONNECTION WITH TWO CLIENTS ---------------

print("Searching for player 1")

while(True):
	player1, a1 = s.accept()		# Returns a socket object player1 and a socket adress a1
	if player1 != None: 
		print("Player 1 connected from port ", str(a1))
		break		


print("Searching for player 2")

while(True):
	player2, a2 = s.accept()									# Returns a socket object player2 and a socket adress a2
	if a2 != a1: 												# only stop when two unique sockets are obtained
		print("Player 2 connected from port ", str(a2))
		break

print("connected to two sockets")


sleep(1)

# Seeding random number generators -----------------------------

seed = random.randrange(10000)				# Generate seed to send to client-side RNG

print("sending random seed {}".format(seed))

player1.send(str(seed).encode('utf-8'))
sleep(0.5)
player2.send(str(seed).encode('utf-8'))
sleep(0.5)

# Sending countdown to clients ---------------------------------

print("Sending game start signal")

for i in range(5):
	player1.send(str(5-i).encode('utf-8'))
	player2.send(str(5-i).encode('utf-8'))
	sleep(1)

print("starting game")


# GAME STATE LOOP ---------------------------------------------
# listen for messages from either player and sends their location to the other player.

s.setblocking(0)  		# Set socket to non-blocking

while(True):

	try:
		p1_pos = player1.recv(4096)
	except: pass
	try:
		p2_pos = player2.recv(4096)
	except: pass

	# Get player positions

	try:
		p1_pos = int(p1_pos)

	except:
		p1_pos = 9000 # cheap way of removing player from the screen

	try: 
		p2_pos = int(p2_pos)
	except:
		p2_pos = 9000	# ignore value

	# Send player positions if valid.

	if(p1_pos != 9000):
		player2.send(str(p1_pos).encode('utf-8'))

	if(p2_pos != 9000):
		player1.send(str(p2_pos).encode('utf-8'))


player1.close()
player2.close()

print("closed sockets")
