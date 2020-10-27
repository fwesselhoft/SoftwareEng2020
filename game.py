from client import Network
from helper_classes import Card
import time

# DISCLAIMER: This is a super quick and dirty implementation simply to
# get something out on time due to time constraints. Will definitly clean
# things up later when more time is available.

players = []

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


def handle_accusation(winning_cards):
    global accusation_rooms, accusation_suspect, accusation_weapons
    print(accusation_suspect)
    suspect_choice = input(
        "Choose a suspect by typing in the number next to their name: ")
    print(accusation_weapons)
    weapon_choice = input(
        "Choose a weapon by typing in the number next to the name: ")
    print(accusation_rooms)
    room_choice = input(
        "Choose a room by typing in the number next to the name: ")
    room_winner = winning_cards[0].get_card_value()
    weapon_winner = winning_cards[1].get_card_value()
    suspect_winner = winning_cards[2].get_card_value()
    if accusation_rooms[room_choice] == room_winner and accusation_weapons[weapon_choice] == weapon_winner and accusation_suspect[suspect_choice] == suspect_winner:
        return True
    else:
        return False


def check_if_winner(current_player_index):
    number_of_nones = 0
    for i in range(0, current_player_index + 1):
        if players[i] == None and i != current_player_index:
            number_of_nones += 1
    if number_of_nones == 2:
        return True
    else:
        return False


def main(name):
    """
    function for running the game,
    includes the main loop of the game
    :param players: a list of dicts represting a player
    :return: None
    """
    global players

    # start by connecting to the network
    server = Network()
    current_id = server.connect(name)
    players, current_player_index = server.send("get")
    player = players[current_id]

    run = True
    while run:
        # Players wait until there are at least 3 people connected to the server
        while len(players) < 3:
            players, current_player_index = server.send("get")
            time.sleep(0.1)

        # Get updated players list and who's turn it is from server
        players, current_player_index = server.send("get")

        # Perform some action when it is the player's turn
        if player == players[current_player_index]:
            if check_if_winner(current_player_index):
                print(
                    "You are the winner by default since everyone else made an incorrect accusation or left the game. Congrats!")
                break
            print("It is your turn")
            print("What would you like to do? ")
            print("1 : Make an Accusation")
            print("2 : Make an Suggestion")
            print("3 : Move")
            print("4 : End your turn")
            # When exiting, must be careful with players length since del players[current_id]
            # is called and players since changes so it throws an index out of bounds error
            print("5 : Exit Game")
            choice = input("Please select a choice: ")
            if choice == "1":
                # Handle Accusation
                winning_cards = server.send("accuse")
                # print(f"winning_cards sent from server: {winning_cards}")
                result = handle_accusation(winning_cards)
                if result:
                    print("Your accusation is correct. You win!")
                else:
                    print("Your accusation was incorrect. Sorry you're out!")
                    run = False
            elif choice == "2":
                # Handle Suggestion
                print("You made a suggestion.")
            elif choice == "3":
                print("You have moved!")
            elif choice == "4":
                print("You chose to end your turn.")
            elif choice == "5":
                print("Exiting the game.")
                run = False
            # Get index of current player
            print("Your turn is now over.")
            server.send("next")
        else:  # Not player's turn: Can listen to results from other players' turns here?
            # Since this area is for players whose turn it isn't, we can listen for the
            # results from accusations and such to send to all players
            # accusation_result = server.send("accusation result")
            time.sleep(0.1)
    server.disconnect()
    quit()


print("Welcome to Clue-less! Goodluck!")
# get users name
while True:
    name = input("Please enter your name: ")
    if 0 < len(name) < 20:
        break
    else:
        print(
            "Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")
# start game
main(name)
