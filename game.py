import socket
import time
from helperfunctions import recvjson, sendjson
from helperclasses import Player, GameBoard
# Will use some help from regular expressions later on to provide better user input error checking
# import re

# Enter your local IP or AWS IP address here in host variable
host = ""
port = 5555

accusation_suspect = {
    "0": "Mr. Green",
    "1": "Mrs. White",
    "2": "Col. Mustard",
    "3": "Miss Scarlet",
    "4": "Prof. Plum",
    "5": "Mrs. Peacock"
}

accusation_weapons = {
    "0": "Rope",
    "1": "Lead Pipe",
    "2": "Revolver",
    "3": "Candlestick",
    "4": "Wrench",
    "5": "Knife"
}

accusation_rooms = {
    "0": "Study",
    "1": "Hall",
    "2": "Lounge",
    "3": "Dining Room",
    "4": "Kitchen",
    "5": "Ballroom",
    "6": "Billiard Room",
    "7": "Conservatory",
    "8": "Library"
}

gameboard = GameBoard()
game_board = gameboard.get_gameboard()
locations = gameboard.get_locations()


def generate_choices():
    """
    Provide choices to player to make accusation
    Returns:
        A tuple that contains the player's choices.
    """
    numbers_of_suspects = list(accusation_suspect.keys())
    suspects = list(accusation_suspect.values())
    for i in range(0, len(accusation_suspect)):
        print(numbers_of_suspects[i] + " -> " + suspects[i])
    suspect_choice = input("Which suspect do you think committed the crime? ")
    suspect = accusation_suspect[suspect_choice]
    numbers_of_weapons = list(accusation_weapons.keys())
    weapons = list(accusation_weapons.values())
    for i in range(0, len(accusation_weapons)):
        print(numbers_of_weapons[i] + " -> " + weapons[i])
    weapon_choice = input("Which weapon do you think was used to commit the crime? ")
    weapon = accusation_weapons[weapon_choice]
    numbers_of_rooms = list(accusation_rooms.keys())
    rooms = list(accusation_rooms.values())
    for i in range(0, len(accusation_rooms)):
        print(numbers_of_rooms[i] + " -> " + rooms[i])
    room_choice = input("Which room do you think the crime was committed in? ")
    room = accusation_rooms[room_choice]
    return suspect, weapon, room


def make_accusation():
    """
    Provide choices to player to make accusation
    Returns:
        A JSON string that represents the player's accusation.
    """
    suspect, weapon, room = generate_choices()
    accusation = {"Client Choice" : "Accusation", "Suspect Choice" : suspect, "Weapon Choice" : weapon, "Room Choice" : room, "suspect_name" : my_player.get_suspect(), "client ID" : client_id}
    return accusation


def make_suggestion():
    """
    Provide choices to player to make a suggestion
    Returns:
        A JSON string that represents the player's suggestion.
    """
    suspect, weapon, room = generate_choices()
    suggestion = {"Client Choice" : "Suggestion", "Suspect Choice" : suspect, "Weapon Choice" : weapon, "Room Choice" : room, "suspect_name" : my_player.get_suspect(), "client ID" : client_id, "new_position" : gameboard.get_position_of_location(room)}
    return suggestion


def other_player_occupying_space(direction, player, players):
    """
    Check to see if another player is blocking a hallway.
    Returns:
        True if another player is currently occupying a hallway
        False otherwise
    """
    global game_board
    for person in players:
        if player != person:
            # player is current player who we are interested in, person is the one that we need to check to see
            # if he/she is blocking
            if direction == "x-right":
                if player.get_position()[0] == person.get_position()[0] and player.get_position()[1] + 1 == person.get_position()[1] and game_board[player.get_position()[0]][player.get_position()[1] + 1] == 1:
                    return True
            elif direction == "x-left":
                if player.get_position()[0] == person.get_position()[0] and player.get_position()[1] - 1 == person.get_position()[1] and game_board[player.get_position()[0]][player.get_position()[1] - 1] == 1:
                    return True
            elif direction == "y-up":
                if player.get_position()[1] == person.get_position()[1] and player.get_position()[0] - 1 == person.get_position()[0] and game_board[player.get_position()[1]][player.get_position()[0] - 1] == 1:
                    return True
            else:
                if player.get_position()[1] == person.get_position()[1] and player.get_position()[0] + 1 == person.get_position()[0] and game_board[player.get_position()[1]][player.get_position()[0] + 1] == 1:
                    return True
    return False


def get_next_position_options(position, player, players):
    """
    Get a list of options to where you can move your character
    Args:
        position: The current player's position
        player: The current player 
        players: A list of the other players
    Returns: 
        A list containing the possible locations where the current player can move to.
    """
    global game_board, locations
    options = {}
    option_choice = 1
    # can move right in the board
    if position[1] + 1 <= 4:
        if (game_board[position[0]][position[1] + 1] in [1, 2]) and not(other_player_occupying_space("x-right", player, players)):
            options[str(option_choice)] = (
                locations[(position[0], position[1] + 1)])
            option_choice += 1
    # can move left in the board
    if position[1] - 1 >= 0:
        if (game_board[position[0]][position[1] - 1] in [1, 2]) and not(other_player_occupying_space("x-left", player, players)):
            options[str(option_choice)] = (
                locations[(position[0], position[1] - 1)])
            option_choice += 1
    # can move up in the board
    if position[0] - 1 >= 0:
        if (game_board[position[0] - 1][position[1]] in [1, 2]) and not(other_player_occupying_space("y-up", player, players)):
            options[str(option_choice)] = (
                locations[(position[0] - 1, position[1])])
            option_choice += 1
    # can move down in the board
    if position[0] + 1 <= 4:
        if (game_board[position[0] + 1][position[1]] in [1, 2]) and not(other_player_occupying_space("y-down", player, players)):
            options[str(option_choice)] = (
                locations[(position[0] + 1, position[1])])
            option_choice += 1

    # handle corner room cases
    if position[0] == 0 and position[1] == 0:
        options[str(option_choice)] = (locations[(4, 4)])
        option_choice += 1
    elif position[0] == 0 and position[1] == 4:
        options[str(option_choice)] = (locations[(4, 0)])
        option_choice += 1
    elif position[0] == 4 and position[1] == 0:
        options[str(option_choice)] = (locations[(0, 4)])
        option_choice += 1
    elif position[0] == 4 and position[1] == 4:
        options[str(option_choice)] = (locations[(0, 0)])
        option_choice += 1
    return options


def build_list_of_players(list_of_players):
    """
    Builds an iterable list of players from the game data provided.
    Args:
        list_of_players: A list of dictionaries where each dictionary
                        represents a player.
    Returns:
        A list of the players in the game.
    """
    players_list = []
    for player in list_of_players:
        players_list.append(Player(player))
    return players_list


def turn_options(options):
    """
    Presents player the choice to pick where to move to.
    Args:
        options: A list containing the possible locations where the current player can move to.
    Returns: 
        A String representing the integer of the choice made.
    """
    length_of_dict = len(options)
    print("Where would you like to move? ")
    while True: 
        choice = input("Please select a choice: ")
        if int(choice) >= 1 and int(choice) <= length_of_dict:
            return choice
        else:
            print("Sorry that choice is not available. Please choose from one of the given options.")


def display_options(options):
    """
    Displays all the turn options in a friendly manner to the player.
    Args:
        options: A dictionary containing all the possible locations the player
                can move to.
    """
    numbers = list(options.keys())
    locations = list(options.values())
    print("Your options to move are shown below:")
    for i in range(0, len(options)):
        print(numbers[i] + " -> " + locations[i])


def suggestion_prompt():
    """
    Prompt player for choices when making a suggestion.
    """
    print("Would you like to make a suggestion?")
    print("1 -> Yes")
    print("2 -> No")
    # Basic error checking for user input, should add regex support for final target
    while True: 
        suggestion_choice = input("Please select a choice: ")
        if int(suggestion_choice) >= 1 and int(suggestion_choice) <= 2:
            return suggestion_choice
        else:
            print("Sorry that choice is not available. Please choose from one of the given options.")


def accusation_prompt():
    """
    Prompt player for choices when making an accusation.
    """
    print("Would you like to make an accusation?")
    print("1 -> Yes")
    print("2 -> No")
    # Basic error checking for user input, should add regex support for final target
    while True: 
        accusation_choice = input("Please select a choice: ")
        if int(accusation_choice) >= 1 and int(accusation_choice) <= 2:
            return accusation_choice
        else:
            print("Sorry that choice is not available. Please choose from one of the given options.")


def everyone_else_lost(client_id_of_current_player, number_of_players, players_who_lost):
    """
    Determines if everyone else except the current player has lost, i.e. made an incorrect accusation.
    Args:
        client_id_of_current_player - An integer representing the ID of the current player
        number_of_players - An integer representing the number of players in the game
        players_who_lost - A list containing strings of the client ID's of the clients who lost
    Returns:
        True if everyone else has lost except for current player 
        else returns False
    """
    if len(players_who_lost) == number_of_players - 1 and client_id_of_current_player not in players_who_lost:
        return True
    else:
        return False


def check_cards(player_cards, suspect, weapon, room):
    """
    Obtains a list of possible cards that can disprove suggestion.
    Args:
        suspect: A String that is the suspect chosen for the suggestion.
        weapon: A String that is the weapon chosen for the suggestion.
        room: A String that is the room chosen for the suggestion.
    Returns:
        A list of Strings that are the cards that can disprove a suggestion.
    """
    options = []
    for card in player_cards:
        if card == suspect or card == weapon or card == room:
            options.append(card)
    return options


# Print welcome message here 
print("Welcome to ClueLess!")


# Get player's name
while True:
    name = input("Please enter your name: ")
    if 0 < len(name) < 20:
        break
    else:
        print(
            "Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

server_to_connect_to = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_to_connect_to.connect((host, port))

client_id = None

while True:
    server_data = server_to_connect_to.recv(1024).decode("utf-8")
    client_id = server_data.split(",")[1]
    if server_data.split(",")[0] == "The Game Has Started":
        break
    time.sleep(0.1)


# Playing game
while True:
    # Receive game data including other players' data from server
    game_data = recvjson(server_to_connect_to)
    # current_player_index is a string
    current_player_index = game_data["current_player_index"]

    my_player = Player(game_data["players"][int(client_id)])
    my_player.display_cards()


    ######################################################################

    if game_data["suggestion"] == "True":
        if str(game_data["player making disproval"]) == client_id:
            # function to pick card from possible disproval cards
            print("It is my turn to try and disprove the suggestion")
            possible_cards = check_cards(my_player.get_cards(), game_data["suggestion suspect"], game_data["suggestion weapon"], game_data["suggestion room"])
            if len(possible_cards) > 0:
                print(f"Possible cards are {possible_cards}")
                print("Choose one of the following cards to disprove the suggestion:")
                counter = 0
                for card in possible_cards:
                    print(str(counter + 1) + ": " + card)
                    counter += 1
                card_choice = input("Select a card: ")
                card = possible_cards[int(card_choice) - 1]
                sendjson(server_to_connect_to, {"Client Choice" : "Disprove", "client ID" : client_id, "disproval card" : card})
                continue
            else:
                sendjson(server_to_connect_to, {"Client Choice" : "Disprove", "client ID" : client_id, "disproval card" : ""})
                continue

    ######################################################################

    if client_id == str(int(current_player_index) - 1) or (int(client_id) - (game_data["number of players"] - 1)) == int(current_player_index):
        pass
    else:
        print(game_data["game status"])

    if client_id in game_data["kicked players"]:
        print("The game has ended since everyone except one player has made an incorrect accusation.")
        break

    # Check if we have a winner, if so disconnect from server.
    if game_data["accusation_correct"] == "True":
        print("Someone has made a correct accusation. The game is now over.")
        sendjson(server_to_connect_to, {"Client Choice" : "End Game", "client ID" : client_id})
        break

    if everyone_else_lost(client_id, game_data["number of players"], game_data["players who lost"]):
        print("Everyone has made an incorrect accusation, therefore you win by default. Congrats!")
        sendjson(server_to_connect_to, {"Client Choice" : "Kick Players", "client ID" : client_id})
        break
    
    # print(f"game_data is {game_data}") ## Super important! game_data seems to have all the data necessary to draw each frame for game

    list_of_players = build_list_of_players(game_data["players"])
    
    my_position = my_player.get_position()

    # Handle player turn
    if client_id == game_data["current_player_index"]: # current_player_index:
        # Get player's initial position
        initial_position = my_player.get_position()
        options = get_next_position_options(my_position, my_player, list_of_players)
        
        print("It is your turn.")

        display_options(options)
        choice = turn_options(options)

        # Update player position
        my_player.set_position(locations, options[choice])
        # Get player's final position
        final_position = my_player.get_position()

        # if player moves from hallway to room, suggestion option 1
        if game_board[initial_position[0]][initial_position[1]] == 1 and game_board[final_position[0]][final_position[1]] == 2:
            suggestion_choice = suggestion_prompt()
            if suggestion_choice == "1":
                suggestion = make_suggestion()
                sendjson(server_to_connect_to, suggestion)
                # Experimenting with suggestion
                ######################################################
                while True:
                    game_data = recvjson(server_to_connect_to)
                    disproval_card = game_data["disproval card"]
                    print(disproval_card)
                    if disproval_card != "": #or it it my turn again:
                        print(f"A player has showed you {disproval_card}")
                        break
                    elif game_data["suggestion"] == "False":
                        print("No one was able to disprove your suggestion")
                        break
                
                ######################################################

        # if player moves from one room to another by secret passageway
        elif game_board[initial_position[0]][initial_position[1]] == 2 and game_board[final_position[0]][final_position[1]] == 2:
            suggestion_choice = suggestion_prompt()
            if suggestion_choice == "1":
                suggestion = make_suggestion()
                sendjson(server_to_connect_to, suggestion)
                # Experimenting with suggestion
                ######################################################
                while True:
                    game_data = recvjson(server_to_connect_to)
                    disproval_card = game_data["disproval card"]
                    print(disproval_card)
                    if disproval_card != "": #or it it my turn again:
                        print(f"A player has showed you {disproval_card}")
                        break
                    elif game_data["suggestion"] == "False":
                        print("No one was able to disprove your suggestion")
                        break

                ######################################################

        # handle accusation
        accusation_choice = accusation_prompt()
        if accusation_choice == "1":
            accusation = make_accusation()
            # Send accusation choice to server
            sendjson(server_to_connect_to, accusation)
            # Receive response from server whether accusation was correct or not
            response = server_to_connect_to.recv(1024).decode("utf-8")
            if response == "Correct":
                print("You made a correct accusation. You win!")
                break
            else:
                print("Sorry you made an incorrect accusation. You lose. You will be kept in the game to help disprove suggestions.")
        # end of player's turn
        else:
            print("Your turn is now over. Please wait until it is your turn again.")
            # Send updated dictionary containing players' positions to server and get next player turn
            sendjson(server_to_connect_to, {"Client Choice" : "Update", "suspect_name" : my_player.get_suspect(), "new_position" : my_player.update_location(my_player.get_position_as_string()), "coordinates" : my_player.get_position_as_string(), "suggestion suspect" : game_data["suggestion suspect"], "player making suggestion" : my_player.get_suspect()})
    else:
        if client_id == str(int(current_player_index) - 1):
            pass
        else:
            current_player = game_data["players"][int(current_player_index)]["suspect_name"]
            print(f"It is still not your turn. Please wait while {current_player} finishes their turn.")
    time.sleep(1)
