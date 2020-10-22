import socket
import pickle
import time
from _thread import *


class Hand():
    def __init__(self):
        self.cards = []


class NotePad():
    def __init__(self):
        pass


class Player():
    def __init__(self, identifier, suspect):
        self.suspect = suspect
        self.notes = NotePad()
        self.hand = Hand()
        self.identifier = identifier

    def add_card_to_hand(card):
        pass

    def get_identifier(self):
        return self.identifier


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 5555
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)


# Attempt to start server
try:
    s.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("Server could not start...")
    quit()


# Listen for connections to the server
s.listen(6)

# Message to show server started
print(f"Server started with local IP {SERVER_IP}")

suspects = {
    "0": "Miss Scarlet",
    "1": "Prof. Plum",
    "2": "Col. Mustard",
    "3": "Mrs. White",
    "4": "Mr. Green",
    "5": "Mrs. Peacock"
}

players = []
# Number of connections that have been made to the server, i.e. number of clients that have
# connected
connections = 0
# ID of client that connected
_id = 0


def threaded_client(connection, _id):
    global players, connections, suspects
    # Anything printed here appears on server screen

    reply = ""
    current_id = _id

    # 1 receive client name on server
    data = connection.recv(48)
    name = data.decode("utf-8")
    print(name, "connected to the server.")

    # 2 send suspects data to client
    suspects_data = pickle.dumps(suspects)
    connection.send(suspects_data)

    # 3 receive suspect choice from client
    # suspect_choice contains int representing suspect player chose
    suspect_choice = connection.recv(2048).decode()

    players.append(Player((connection, _id), suspect_choice))

    # remove that suspect from player options, so other players may choose from
    # remaining suspects
    suspects.pop(suspect_choice, None)

    while len(players) < 3:
        for player in players:
            player.get_identifier()[0].send(str.encode("INITIALIZING"))
        time.sleep(5)

    print("Client has left.")
    connections -= 1
    print("Connections:", connections)
    print("current_id:", current_id)
    # disconnect client from server
    connection.close()


while True:
    host, _id = s.accept()
    connections += 1
    print(start_new_thread(threaded_client, (host, _id)))
    print(f"{_id} has connected to the server.")
