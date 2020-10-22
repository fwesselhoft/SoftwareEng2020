import socket
import pickle
import time


class Client():
    """
    Class to connect, send, and receive information from the client to the server
    """

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ""  # Enter IP address of your local network here as a String
        self.port = 5555
        self.address = (self.host, self.port)

    def connect_to_server(self, name):
        """
        Connects to server and returns the name of the client that connected
        :param name: A string representing the name of the client being connected
        :return: The name of the client
        """
        # Anyting printed here appears on client screen
        self.client.connect(self.address)
        # 1 send client name to server
        self.client.send(str.encode(name))

        # 2 receive suspects data from server
        suspects_list = pickle.loads(self.client.recv(2048))
        print(suspects_list)
        print("Choose one of the suspects by entering the number next to their name.")

        # 3 send suspects choice to server
        # assuming the user will enter the correct information for now so avoiding error handling
        suspect_choice = input("Suspect choice: ")
        self.client.send(str.encode(suspect_choice))

        return name

    def join_waiting_lobby(self, gamestate):
        """
        Joins the waiting lobby of the game until there are enough players present
        :param gamestate: A string representing the current gamestate
        """
        print("Currently in lobby waiting for enough players to join...")
        while gamestate == "INITIALIZING":
            gamestate = self.client.recv(2048).decode("utf-8")
        print("The game has started, goodluck!")

    def disconnect_from_server(self):
        """
        Disconnects from the server
        :return: None
        """
        self.client.close()

    def send_data_to_server(self, data):
        """
        Sends information from client to server
        :param data: A string representing the data to be sent to the server
        :return: A string that is a reply from the server that the data was received
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048 * 4)
            return reply
        except socket.error as e:
            print(e)
