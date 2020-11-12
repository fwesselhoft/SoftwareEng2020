import socket
from helperfunctions import convert_into_real_position, sendjson, recvjson

class Player():
    def __init__(self, jsonString):
        self.suspect = jsonString["suspect_name"]
        self.position = jsonString["position"]
        self.cards = jsonString["cards"]

    def __eq__(self, other):
        if (isinstance(other, Player)):
            return self.suspect == other.suspect

    def get_suspect(self):
        return self.suspect

    def display_cards(self):
        print(f"My cards are: ", end="")
        for i in range(0, len(self.cards) - 1):
            print(f"{self.cards[i]}, ", end="")
        print(f"{self.cards[len(self.cards) - 1]}")

    def get_position(self):
        position = convert_into_real_position(self.position)
        return position

    def get_position_as_string(self):
        return self.position

    def update_position(self, x_coordinate, y_coordinate):
        self.position = "(" + str(x_coordinate) + ", " + str(y_coordinate) + ")"

    def set_position(self, locations, new_position):
        keys = list(locations.keys())
        values = list(locations.values())
        index = values.index(new_position)
        self.position = str(keys[index])

    def display_info(self):
        print(f"Suspect is {self.suspect} and my position is {self.position} and cards are {self.cards}")

# A 1 or a 2 on the game board means you can move there, a 0 means you cannot
# A 2 on the game board signifies a room
# (1, 1), (1, 3), (3, 1), (3, 3) are the spots you cannot move to
# Starting positions for:
# Mr. Green: (4, 1)
# Mrs. White: (4, 3)
# Col. Mustard: (1, 4)
# Miss Scarlet: (0, 3)
# Prof. Plum: (1, 0)
# Mrs. Peacock: (3, 0)
class GameBoard():
    def __init__(self):
        self.gameboard = [
            [2, 1, 2, 1, 2], 
            [1, 0, 1, 0, 1], 
            [2, 1, 2, 1, 2], 
            [1, 0, 1, 0, 1], 
            [2, 1, 2, 1, 2]
        ]
        self.locations = {
            (0, 0) : "Study",
            (0, 1) : "Hallway between Study and Hall",
            (0, 2) : "Hall",
            (0, 3) : "Hallway between Hall and Lounge",
            (0, 4) : "Lounge",
            (1, 0) : "Hallway between Study and Library",
            (1, 1) : "Invalid Position",
            (1, 2) : "Hallway between Hall and Billiard Room",
            (1, 3) : "Invalid Position",
            (1, 4) : "Hallway between Lounge and Dining Room",
            (2, 0) : "Library",
            (2, 1) : "Hallway between Library and Billiard Room",
            (2, 2) : "Billiard Room",
            (2, 3) : "Hallway between Billiard Room and Dining Room",
            (2, 4) : "Dining Room",
            (3, 0) : "Hallway between Library and Conservatory",
            (3, 1) : "Invalid Position",
            (3, 2) : "Hallway between Billiard Room and Ballroom",
            (3, 3) : "Invalid Position",
            (3, 4) : "Hallway between Dining Room and Kitchen",
            (4, 0) : "Conservatory",
            (4, 1) : "Hallway between Conservatory and Ballroom",
            (4, 2) : "Ballroom",
            (4, 3) : "Hallway between Ballroom and Kitchen",
            (4, 4) : "Kitchen"
        }

    def get_gameboard(self):
        return self.gameboard

    def get_locations(self):
        return self.locations
