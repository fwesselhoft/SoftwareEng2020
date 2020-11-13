import socket
import time
import random
from helperfunctions import recvjson, sendjson
from helperclasses import Player

# All the code between the hash marks is setting up the server
############################################################### 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


PORT = 5555
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

try:
    server.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

server.listen()
###############################################################

# The number of clients connected to the server
connections = 0
# A list of tuples containing the sockets of the clients to communicate with them
clients = []

client_id = 0
current_player_index = 0

# General form of player data so that each client may draw a new frame during game
players = [
    {"suspect_name" : "Miss Scarlet", "position" : "(0, 3)", "cards" : [], "accusation wrong" : "False"}, 
    {"suspect_name" : "Prof. Plum", "position" : "(1, 0)", "cards" : [], "accusation wrong" : "False"}, 
    {"suspect_name" : "Col. Mustard", "position" : "(1, 4)", "cards" : [], "accusation wrong" : "False"},
    {"suspect_name" : "Mrs. White", "position" : "(4, 3)", "cards" : [], "accusation wrong" : "False"},
    {"suspect_name" : "Mr. Green", "position" : "(4, 1)", "cards" : [], "accusation wrong" : "False"},
    {"suspect_name" : "Mrs. Peacock", "position" : "(3, 0)", "cards" : [], "accusation wrong" : "False"}
]

suspect_cards = ["Mr. Green", "Mrs. White", "Col. Mustard",
                 "Miss Scarlet", "Prof. Plum", "Mrs. Peacock"]

weapon_cards = ["Rope", "Lead Pipe", "Revolver",
                "Candlestick", "Wrench", "Knife"]

room_cards = ["Study", "Hall", "Lounge", "Dining Room", "Kitchen",
              "Ballroom", "Billiard Room", "Conservatory", "Library"]

game_data = {
    "players" : players,
    "current_player_index" : str(current_player_index),
    "accusation_correct" : "False",
    "players who lost" : [],
    "number of players" : connections,
    "kicked players" : [],
    "game status" : "The Game Has Started. Goodluck!"
}


def shuffle_cards(deck):
    """
    Shuffles deck of cards which is a list of Strings
    Args: 
        deck: The list of Strings to be shuffled
    """
    random.shuffle(deck)


def get_random_winning_cards(suspect_cards, weapon_cards, room_cards):
    """
    Pick three cards to be the set of winning cards to end the game.
    Args:
        suspect_cards: A list of Strings containing the suspects.
        weapon_cards: A list of Strings containing the weapons.
        room_cards: A list of Strings containing the room.
    Returns:
        A tuple containing three strings which represent winning cards: (suspect, weapon, room)
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


def combine_decks_into_one(suspect_cards, weapon_cards, room_cards):
    """
    Combine different lists of cards into a single list
    Args:
        suspect_cards: A list of Strings containing the suspects.
        weapon_cards: A list of Strings containing the weapons.
        room_cards: A list of Strings containing the room.
    Returns:
        A combined list of all the cards
    """
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
    Pass out remaining cards one at a time to players after choosing winning cards.
    Args:
        combined_deck: A list of all the cards to be passed out
    """
    current = 0
    while len(combined_deck) != 0:
        if current > len(clients) - 1:
            current = 0
        players[current]["cards"].append(combined_deck[0])
        del combined_deck[0]
        current += 1


def initialize_game():
    """
    Perform initial card setup, that includes shuffing each dech respectively, 
    choosing one card from each deck as the game winning card, recombining all the 
    cards and re-shuffling the cards
    Returns:
        A tuple containing the tuple of winning cards and the combined deck of cards
    """
    shuffle_cards(room_cards)
    shuffle_cards(weapon_cards)
    shuffle_cards(suspect_cards)
    winning_cards = get_random_winning_cards(
        room_cards, weapon_cards, suspect_cards)
    print("The suspect winning card is", winning_cards[2])
    print("The weapon winning card is", winning_cards[1])
    print("The room winning card is", winning_cards[0])
    combined_deck = combine_decks_into_one(
        suspect_cards, weapon_cards, room_cards)
    shuffle_cards(combined_deck)
    return winning_cards, combined_deck


# Helper function to determine correct next player index
def get_next_player():
    """
    Updates the index of the next player into the game_data variable,
    taking into account whether that player has made an incorrect accusation 
    or not. Cycles around players, so that when one round of player turns has
    passed, it starts again at the first player.
    """
    global current_player_index, game_data, players
    current_player_index += 1
    if current_player_index >= len(clients):
        current_player_index = 0
        if players[current_player_index]["accusation wrong"] == "True":
            while players[current_player_index]["accusation wrong"] == "True":
                current_player_index += 1
                if current_player_index >= len(clients):
                    current_player_index = 0
    elif players[current_player_index]["accusation wrong"] != "True":
        current_player_index = current_player_index
    else:
        while players[current_player_index]["accusation wrong"] == "True":
            current_player_index += 1
            if current_player_index >= len(clients):
                current_player_index = 0
    game_data["current_player_index"] = str(current_player_index)


print("[SERVER] Waiting for connections")


def broadcast(msg):
    """
    Sends a message to all clients connected to the server.
    Args:
        msg: A JSON string representing the message to be send to the client.
    """
    for client in clients:
        # client[0].send(str.encode(msg))
        sendjson(client[0], msg)


def broadcast_to_everyone_except_current_player(msg):
    """
    Sends a message to all clients connected to the server except 
    for the player who's current turn it is.
    Args:
        msg: A JSON string representing the message to be send to the client.
    """
    for i in range(0, len(clients)):
        if current_player_index != i:
            sendjson(clients[i][0], msg)


def update_players(suspect, new_position):
    """
    Updates the position of the current player to the new position they chose.
    Args:
        suspect: A String representing the name of the suspect of the current player
        new_position: A String representing the coordinates of the new position.
    """
    global players
    for player in players:
        if player["suspect_name"] == suspect:
            player["position"] = new_position


def kick_player(suspect):
    """
    Sets the player's accusation wrong flag to be true.
    Args:
        suspect: A String representing the name of the suspect of the current player
    """
    global players
    for player in players:
        if player["suspect_name"] == suspect:
            player["accusation wrong"] = "True"


def validate_accusation(response):
    """
    Validates the player's accusation and determines whether it was 
    correct or incorrect.
    Args:
        response: A JSON string that contains the player's accusation
                choices.
    Returns: 
        A String representing a correct/incorrect accusation.
    """
    global game_data
    suspect_choice = response["Suspect Choice"]
    weapon_choice = response["Weapon Choice"]
    room_choice = response["Room Choice"]
    if suspect_choice == winning_cards[0] and weapon_choice == winning_cards[1] and room_choice == winning_cards[2]:
        game_data["accusation_correct"] = "True"
        return "Correct"
    else:
        game_data["players who lost"].append(response["client ID"])
        kick_player(response["suspect_name"])
        return "Incorrect"


def remove_players_who_lost(client_id):
    """
    Adds players who have lost due to an incorrect accusation to the list of 
    players that are no longer in the game.
    Args: 
        client_id: A string representing the client ID of the winner
    """
    global game_data
    for i in range(0, len(clients)):
        id_of_player_who_lost = str(i)
        if id_of_player_who_lost != client_id:
            game_data["kicked players"].append(id_of_player_who_lost)


# winning_cards[2] is the suspect
# winning_cards[1] is the weapon
# winning_cards[0] is the room
winning_cards, combined_deck = initialize_game()
winning_cards = [winning_cards[2], winning_cards[1], winning_cards[0]]

# Keep looping to accept new connections
while True:
    host, addr = server.accept()
    connections += 1
    clients.append((host, client_id))
    client_id += 1

    game_data["number of players"] += 1

    print("[SERVER] A new connection has been established.")
    
    if connections >= 3:
        pass_out_cards(combined_deck)
        # send start game message to each client, along with their ID "The Game Has Started,ID#"
        for client in clients:
            client[0].send(str.encode("The Game Has Started," + str(client[1])))
        time.sleep(1)

        print("[SERVER] The game has started.")

        # Playing game
        while True:
            # Send game data to players so they can make a move
            broadcast(game_data)
            # Receive the players move
            response = recvjson(clients[current_player_index][0])
            
            # print(response)
            # Process the player's move
            if response["Client Choice"] == "End Game":
                break
            elif response["Client Choice"] == "Kick Players":
                remove_players_who_lost(response["client ID"])
                broadcast(game_data)
                break
            elif response["Client Choice"] == "Accusation":
                guess = validate_accusation(response)
                game_data["game status"] = response["suspect_name"] + " made a " + guess + " accusation."
                clients[current_player_index][0].send(str.encode(guess))
                get_next_player()
                # broadcast_to_everyone_except_current_player(game_data)
            elif response["Client Choice"] == "Suggestion":
                game_data["game status"] = "A player made a suggestion."
                get_next_player() # For now when a player makes a suggestion, the server simply gets the next player
                # broadcast_to_everyone_except_current_player(game_data)
            elif response["Client Choice"] == "Update":
                new_coordinates = response["coordinates"]
                game_data["game status"] = response["suspect_name"] + " has moved to the " + response["new_position"]                
                update_players(response["suspect_name"], new_coordinates)
                get_next_player()
                # broadcast_to_everyone_except_current_player(game_data)
            else:
                get_next_player()
            time.sleep(0.1)
    if connections >= 3:
        break
    time.sleep(1)

print("[SERVER] Server offline")
