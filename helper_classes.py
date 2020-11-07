Class Card():
    def __init__(self, value):
        self.value = value

    def get_card_value(self):
        return self.value


class Player():
    def __init__(self, identity):
        # identity is a tuple ("Mrs. Scarlett", "Erik")
        self.identifier = identity
        self.cards = []
        self.position = self.initialize_position(
            self.identifier[0])
        self.lost = False
        self.playing = True

    def __eq__(self, other):
        if (isinstance(other, Player)):
            return self.identifier[0] == other.identifier[0] and self.identifier[1] == other.identifier[1]

    def add_card(self, card):
        self.cards.append(card)

    def get_suspect(self):
        return self.identifier[0]

    def get_name(self):
        return self.identifier[1]

    def change_player_status(self):
        self.lost = True

    def get_player_status(self):
        return self.lost

    def change_playing_status(self):
        self.playing = False

    def get_playing_status(self):
        return self.playing

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

    def update_position(self, x_coordinate, y_coordinate):
        self.position = (x_coordinate, y_coordinate)

    def set_position(self, gameboard, new_position):
        keys = list(gameboard.locations.keys())
        values = list(gameboard.locations.values())
        index = values.index(new_position)
        self.position = keys[index]


class Game():
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
    def __init__(self):
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

    def other_player_occupying_space(self, direction, player, players):
        """
        Return True if another player is currently occupying a possible new position and is a hallway
        Return False otherwise
        """
        for person in players:
            if player != person:
                # player is current player who we are interested in, person is the one that we need to check to see
                # if he/she is blocking
                if direction == "x-right":
                    if player.get_position()[0] == person.get_position()[0] and player.get_position()[1] + 1 == person.get_position()[1] and self.gameboard[player.get_position()[0]][player.get_position()[1] + 1] == 1:
                        return True
                elif direction == "x-left":
                    if player.get_position()[0] == person.get_position()[0] and player.get_position()[1] - 1 == person.get_position()[1] and self.gameboard[player.get_position()[0]][player.get_position()[1] - 1] == 1:
                        return True
                elif direction == "y-up":
                    if player.get_position()[1] == person.get_position()[1] and player.get_position()[0] - 1 == person.get_position()[0] and self.gameboard[player.get_position()[1]][player.get_position()[0] - 1] == 1:
                        return True
                else:
                    if player.get_position()[1] == person.get_position()[1] and player.get_position()[0] + 1 == person.get_position()[0] and self.gameboard[player.get_position()[1]][player.get_position()[0] + 1] == 1:
                        return True
        return False

    def get_next_position_options(self, position, player, players):
        """
        Get the options to where you can move your character
        param: position the current player's position
        """
        options = {}
        option_choice = 1
        # can move right in the board
        if position[1] + 1 <= 4:
            if (self.gameboard[position[0]][position[1] + 1] in [1, 2]) and not(self.other_player_occupying_space("x-right", player, players)):
                options[option_choice] = (
                    self.locations[(position[0], position[1] + 1)])
                option_choice += 1
        # can move left in the board
        if position[1] - 1 >= 0:
            if (self.gameboard[position[0]][position[1] - 1] in [1, 2]) and not(self.other_player_occupying_space("x-left", player, players)):
                options[option_choice] = (
                    self.locations[(position[0], position[1] - 1)])
                option_choice += 1
        # can move up in the board
        if position[0] - 1 >= 0:
            if (self.gameboard[position[0] - 1][position[1]] in [1, 2]) and not(self.other_player_occupying_space("y-up", player, players)):
                options[option_choice] = (
                    self.locations[(position[0] - 1, position[1])])
                option_choice += 1
        # can move down in the board
        if position[0] + 1 <= 4:
            if (self.gameboard[position[0] + 1][position[1]] in [1, 2]) and not(self.other_player_occupying_space("y-down", player, players)):
                options[option_choice] = (
                    self.locations[(position[0] + 1, position[1])])
                option_choice += 1

        # handle corner room cases
        if position[0] == 0 and position[1] == 0:
            options[option_choice] = (self.locations[(4, 4)])
            option_choice += 1
        elif position[0] == 0 and position[1] == 4:
            options[option_choice] = (self.locations[(4, 0)])
            option_choice += 1
        elif position[0] == 4 and position[1] == 0:
            options[option_choice] = (self.locations[(0, 4)])
            option_choice += 1
        elif position[0] == 4 and position[1] == 4:
            options[option_choice] = (self.locations[(0, 0)])
            option_choice += 1
        return options
