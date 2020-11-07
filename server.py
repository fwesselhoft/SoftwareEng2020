import socket
import _pickle as pickle
import time
import random
from _thread import *
from helper_classes import Card, Player, Game

# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 5555

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

# try to connect to server
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()  # listen for connections

players = []
connections = 0
_id = 0
current_player_index = 0

suspects = {
    "0": "Miss Scarlet",
    "1": "Prof. Plum",
    "2": "Col. Mustard",
    "3": "Mrs. White",
    "4": "Mr. Green",
    "5": "Mrs. Peacock"
}

suspect_cards = [Card("Mr. Green"), Card("Mrs. White"), Card("Col. Mustard"),
                 Card("Miss Scarlet"), Card("Prof. Plum"), Card("Mrs. Peacock")]

weapon_cards = [Card("Rope"), Card("Lead Pipe"), Card("Revolver"),
                Card("Candlestick"), Card("Wrench"), Card("Knife")]

room_cards = [Card("Study"), Card("Hall"), Card("Lounge"), Card("Dining Room"), Card("Kitchen"),
              Card("Ballroom"), Card("Billiard Room"), Card("Conservatory"), Card("Library")]

turn_status = ""


def broadcast():
    pass


def shuffle_cards(deck):
    random.shuffle(deck)


def get_random_winning_cards(suspect_cards, weapon_cards, room_cards):
    """
    Get three cards to be the set of winning cards to end the game.
    winning_cards[0] is the character to win
    winning_cards[1] is the weapon to win
    winning_cards[2] is the room to win
    """
    num_of_suspect_cards = len(suspect_cards) - 1
    num_of_weapon_cards = len(weapon_cards) - 1
    num_of_room_cards = len(room_cards) - 1
    winning_cards = (suspect_cards[random.randint(
        0, num_of_suspect_cards)], weapon_cards[random.randint(0, num_of_weapon_cards)], room_cards[random.randint(0, num_of_room_cards)])
    suspect_cards.remove(winning_cards[0])
    weapon_cards.remove(winning_cards[1])
    room_cards.remove(winning_cards[2])
    return winning_cards


def combine_decks_into_one(room_cards, weapon_cards, suspect_cards):
    combined_deck = []
    for card in room_cards:
        combined_deck.append(card)
    for card in weapon_cards:
        combined_deck.append(card)
    for card in suspect_cards:
        combined_deck.append(card)
    return combined_deck


def pass_out_cards(combined_deck):
    """
    Pass out remaining cards to the players after picking 3 out as winning cards.
    """
    current = 0
    while len(combined_deck) != 0:
        if current > len(players) - 1:
            current = 0
        players[current].add_card(combined_deck[0])
        del combined_deck[0]
        current += 1


def initialize_game():
    """
    Perform initial card setup, that includes shuffing each dech respectively, 
    choosing one card from each deck as the game winning card, recombining all the 
    cards and re-shuffling the cards
    """
    shuffle_cards(room_cards)
    shuffle_cards(weapon_cards)
    shuffle_cards(suspect_cards)
    winning_cards = get_random_winning_cards(
        room_cards, weapon_cards, suspect_cards)
    print("The suspect winning card is", winning_cards[2].get_card_value())
    print("The weapon winning card is", winning_cards[1].get_card_value())
    print("The room winning card is", winning_cards[0].get_card_value())
    combined_deck = combine_decks_into_one(
        room_cards, weapon_cards, suspect_cards)
    shuffle_cards(combined_deck)
    return winning_cards, combined_deck


def threaded_client(conn, _id):
    """
    runs in a new thread for each player connected to the server
    :param con: IP address of connection
    :param _id: int
    :return: None
    """
    global connections, players, current_player_index, winning_cards, turn_status

    current_id = _id

    # recieve the name of the client
    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[LOG]", name, "connected to the server.")
    player_data = (suspects[str(current_id)], name)
    players.append(Player(player_data))

    # send initial info to clients
    conn.send(str.encode(str(current_id)))

    while True:
        try:
            data = conn.recv(32)

            if not data:
                break

            data = data.decode("utf-8")

            if data == "get":
                send_data = pickle.dumps(
                    (players, current_player_index))

            elif data.split(" ")[0] == "next":
                # Adjust next to account for removed players which are defaulted to None
                # if current_player_index == len(players) - 1:
                #     current_player_index = 0
                # else:
                #     current_player_index += 1
                players[current_player_index].update_position(
                    int(data.split(" ")[1][1]), int(data.split(" ")[2][0]))
                # logic to get next player
                current_player_index += 1
                if current_player_index >= len(players):
                    current_player_index = 0
                    if players[current_player_index] == None:
                        while players[current_player_index] == None:
                            current_player_index += 1
                            if current_player_index >= len(players):
                                current_player_index = 0
                elif players[current_player_index] != None:
                    current_player_index = current_player_index
                else:
                    while players[current_player_index] == None:
                        current_player_index += 1
                        if current_player_index >= len(players):
                            current_player_index = 0
                # send player's data to server to update gameboard
                send_data = pickle.dumps((players, current_player_index))

            # if data == "accusation result":
            #     send_data = str.encode(
            #         "This is the accusation result from the other player")

            elif data == "update players":
                players[current_player_index].change_player_status()
                send_data = pickle.dumps((players, current_player_index))

            elif data == "end game":
                for player in players:
                    player.change_playing_status()
                send_data = pickle.dumps((players, current_player_index))

            elif data == "pass out cards":
                pass_out_cards(combined_deck)
                send_data = pickle.dumps((players, current_player_index))

            elif data == "accuse":
                send_data = pickle.dumps(winning_cards)
            else:
                send_data = pickle.dumps(
                    (players, current_player_index))

            conn.send(send_data)

        except Exception as e:
            print(e)
            break  # if an exception has been reached disconnect client

        time.sleep(0.001)

    # When user disconnects
    print("[DISCONNECT] Name:", name,
          ", Client Id:", current_id, "disconnected")

    connections -= 1
    players[current_id] = None
    # del players[current_id]  # remove client information from players list
    conn.close()  # close connection


# setup gameboard
main_gameboard = Game()
# winning_cards[0] is the room
# winning_cards[1] is the weapon
# winning_cards[2] is the suspect
winning_cards, combined_deck = initialize_game()
print("[SERVER] Waiting for connections")

# Keep looping to accept new connections
while True:

    host, addr = S.accept()

    # increment connections start new thread then increment ids
    connections += 1
    start_new_thread(threaded_client, (host, _id))
    _id += 1

# when program ends
print("[SERVER] Server offline")
