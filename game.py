from client import Client
from helper_classes import Card, Game, Player
import time

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
    number_of_lost = 0
    for i in range(len(players)):
        # print(players[i].get_player_status())
        if (players[i] == None and players[i] != players[current_player_index]) or (players[i].get_player_status() == True and players[i] != players[current_player_index]):
            number_of_lost += 1
    if number_of_lost == len(players) - 1:
        return True
    else:
        return False


def turn_options(options):
    print("Where would you like to move? ")
    choice = input("Please select a choice: ")
    return choice


def main(name):
    """
    function for running the game,
    includes the main loop of the game
    :param players: a list of dicts represting a player
    :return: None
    """
    global players

    # start by connecting to the network
    client = Client()
    current_id = client.connect(name)
    players, current_player_index = client.send("get")
    player = players[current_id]

    print(f"My player is {player.identifier[0]} and {player.identifier[1]}")
    print(f"My player's position is: {player.get_position()}")

    # players wait until there are at least 3 people connected to the server
    while len(players) < 3:
        # Might not have to be sending data to server at this point...
        players, current_player_index = client.send("get")
        time.sleep(0.1)

    # pass out cards to players
    players, current_player_index = client.send("pass out cards")

    players[current_id].display_cards()

    # first initialzation to gameboard
    game_board = Game()

    lost = False
    run = True
    while players[current_id].get_playing_status():
        # Get updated players list and who's turn it is from server
        players, current_player_index = client.send("get")
        # Perform some action when it is the player's turn
        if players[current_id] == players[current_player_index]:
            # Check to see if player has lost, i.e. made an incorrect accusation
            # if so, that player's turn is skipped, but he/she remains in the game
            if not lost:
                if check_if_winner(current_player_index):
                    print(
                        "You are the winner by default since everyone else made an incorrect accusation or left the game. Congrats!")
                    players, current_player_index = client.send(
                        "end game")
                    break
                # choice = turn_options()
                # Print locations to move to on player's turn
                initial_position = players[current_id].get_position()
                move_options = game_board.get_next_position_options(
                    players[current_id].get_position(), players[current_id], players)
                print("It is your turn")
                print(f"Your current options to move are: {move_options}")
                choice = turn_options(move_options)
                print(f"You have moved to the {move_options[int(choice)]}")
                # Update player position
                players[current_id].set_position(
                    game_board, move_options[int(choice)])
                final_position = players[current_id].get_position()

                # need last case where other player moves you into a room
                # if player moves from hallway to room, suggestion option 1
                if game_board.gameboard[initial_position[0]][initial_position[1]] == 1 and game_board.gameboard[final_position[0]][final_position[1]] == 2:
                    suggestion_choice = input(
                        "Would you like to make a suggestion? Yes or No? ")
                    if suggestion_choice == "Yes":
                        print("You made a suggestion.")
                # if player moves from one room to another by secret passageway
                elif game_board.gameboard[initial_position[0]][initial_position[1]] == 2 and game_board.gameboard[final_position[0]][final_position[1]] == 2:
                    suggestion_choice = input(
                        "Would you like to make a suggestion? Yes or No? ")
                    if suggestion_choice == "Yes":
                        print("You made a suggestion.")
                # handle accusation
                accusation_choice = input(
                    "Would you like to make an accusation? Yes or No? ")
                if accusation_choice == "Yes":
                    winning_cards = client.send("accuse")
                    result = handle_accusation(winning_cards)
                    if result:
                        print("Your accusation was correct. You win!")
                        players, current_player_index = client.send(
                            "end game")
                    else:
                        print("Your accusation was incorrect. Sorry you're out!")
                        lost = True
                        players[current_player_index].change_player_status()
                        players, current_player_index = client.send(
                            "update players")
                # end of player's turn
                print("Your turn is now over.")
                # print(str(players[current_id].get_position()))
                players, current_player_index = client.send(
                    "next " + str(players[current_id].get_position()))
            else:
                print(
                    "You are still in the game to help disprove suggestions when a suggestion is made")
                players, current_player_index = client.send(
                    "next " + str(players[current_id].get_position()))
        else:  # Not player's turn: Can listen to results from other players' turns here?
            # Since this area is for players whose turn it isn't, we can listen for the
            # results from accusations and such to send to all players
            time.sleep(0.1)
    client.disconnect()
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
