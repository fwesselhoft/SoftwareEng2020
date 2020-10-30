class Card():
    def __init__(self, value):
        self.value = value

    def get_card_value(self):
        return self.value


class Player():
    def __init__(self, identity):
        # identity is a tuple ("Mrs. Scarlett", "Erik")
        self.identifier = identity
        self.cards = []
        self.position = self.initialize_position(identity[0])

    def __eq__(self, other):
        if (isinstance(other, Player)):
            return self.identifier[0] == other.identifier[0] and self.identifier[1] == other.identifier[1]

    def add_card(self, card):
        self.cards.append(card)

    def get_suspect(self):
        return self.identifier[0]

    def get_name(self):
        return self.identifier[1]

    def display_cards(self):
        print(f"My cards are: ", end="")
        for i in range(0, len(self.cards) - 1):
            print(f"{self.cards[i].get_card_value()}, ", end="")
        print(f"{self.cards[len(self.cards) - 1].get_card_value()}")

    def initialize_position(self, suspect):
        if suspect == "Mr. Green":
            position = (4, 1)
        elif suspect == "Mrs. White":
            position = (4, 3)
        elif suspect == "Col. Mustard":
            position = (1, 4)
        elif suspect == "Miss Scarlet":
            position = (0, 3)
        elif suspect == "Prof. Plum":
            position = (1, 0)
        else:
            position = (3, 0)
        return position

    def get_position(self):
        return self.position


class GameBoard():
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
    def __init__(self, player, players):
        self.gameboard = [[2, 1, 2, 1, 2], [1, 0, 1, 0, 1], [
            2, 1, 2, 1, 2], [1, 0, 1, 0, 1], [2, 1, 2, 1, 2]]
        self.locations = {
            (0, 0): "Study",
            (0, 1): "Hallway between Study and Hall",
            (0, 2): "Hall",
            (0, 3): "Hallway between Hall and Lounge",
            (0, 4): "Lounge",
            (1, 0): "Hallway between Study and Library",
            (1, 1): "Invalid Position",
            (1, 2): "Hallway between Hall and Billiard Room",
            (1, 3): "Invalid Position",
            (1, 4): "Hallway between Lounge and Dining Room",
            (2, 0): "Library",
            (2, 1): "Hallway between Library and Billiard Room",
            (2, 2): "Billiard Room",
            (2, 3): "Hallway between Billiard Room and Dining Room",
            (2, 4): "Dining Room",
            (3, 0): "Hallway between Library and Conservatory",
            (3, 1): "Invalid Position",
            (3, 2): "Hallway between Billiard Room and Ballroom",
            (3, 3): "Invalid Position",
            (3, 4): "Hallway between Dining Room and Kitchen",
            (4, 0): "Conservatory",
            (4, 1): "Hallway between Conservatory and Ballroom",
            (4, 2): "Ballroom",
            (4, 3): "Hallway between Ballroom and Kitchen",
            (4, 4): "Kitchen"
        }
        self.current_player = player
        self.players = players

    def other_player_occupying_space(self, direction):
        """
        Return True if another player is currently occupying a possible new position
        Return False otherwise
        """
        for player in self.players:
            if player != self.current_player and direction == "x":
                if (player.get_position()[0] == self.current_player.get_position()[0] and player.get_position()[1] == self.current_player.get_position()[1] + 1) or (player.get_position()[0] == self.current_player.get_position()[0] and player.get_position()[1] == self.current_player.get_position()[1] - 1):
                    return True
            if player != self.current_player and direction == "y":
                if (player.get_position()[1] == self.current_player.get_position()[1] and player.get_position()[0] == self.current_player.get_position()[0] + 1) or (player.get_position()[1] == self.current_player.get_position()[1] and player.get_position()[0] == self.current_player.get_position()[0] - 1):
                    return True
        return False

    def get_next_position_options(self):
        """
        Get the options to where you can move your character
        param: player a Player who's position will be used to determine next possbile positions
        """
        options = []
        # Check to see if x coordinate is out of bounds of the board
        if self.current_player.get_position()[1] + 1 > 4 or self.current_player.get_position()[1] - 1 < 0:
            pass
        else:
            if (self.gameboard[self.current_player.get_position()[0]][self.current_player.get_position()[1] + 1] in [1, 2]) and not(self.other_player_occupying_space("x")):
                options.append(
                    self.locations[(self.current_player.get_position()[0], self.current_player.get_position()[1] + 1)])
            if (self.gameboard[self.current_player.get_position()[0]][self.current_player.get_position()[1] - 1] in [1, 2]) and not(self.other_player_occupying_space("x")):
                options.append(
                    self.locations[(self.current_player.get_position()[0], self.current_player.get_position()[1] - 1)])
        # Check to see if y coordinate is out of bounds of the board
        if self.current_player.get_position()[0] + 1 > 4 or self.current_player.get_position()[0] - 1 < 0:
            pass
        else:
            if (self.gameboard[self.current_player.get_position()[1]][self.current_player.get_position()[0] + 1] in [1, 2]) and not(self.other_player_occupying_space("y")):
                options.append(
                    self.locations[(self.current_player.get_position()[0] + 1, self.current_player.get_position()[1])])
            if (self.gameboard[self.current_player.get_position()[1]][self.current_player.get_position()[0] - 1] in [1, 2]) and not(self.other_player_occupying_space("y")):
                options.append(
                    self.locations[(self.current_player.get_position()[0] - 1, self.current_player.get_position()[1])])
        if self.current_player.get_position()[0] == 0 and self.current_player.get_position()[1] == 0:
            options.append(self.locations[(4, 4)])
        elif self.current_player.get_position()[0] == 0 and self.current_player.get_position()[1] == 4:
            options.append(self.locations[(4, 0)])
        elif self.current_player.get_position()[0] == 4 and self.current_player.get_position()[1] == 0:
            options.append(self.locations[(0, 4)])
        elif self.current_player.get_position()[0] == 4 and self.current_player.get_position()[1] == 4:
            options.append(self.locations[(0, 0)])
        return options
