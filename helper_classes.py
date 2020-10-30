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
