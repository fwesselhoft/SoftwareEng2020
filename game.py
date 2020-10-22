import socket
from client import Client

# We can also change this to a enum if we would like, I made this a string for
# demonstration purposes
GAME_STATE = "INITIALIZING"

# Currently the clients are disconnected from the server once the 3rd player
# joins the server. This is just to demonstrate how to connect a user to a server.
# These files can be easily adapted to show the capability of sending messages to the
# server and from the server to the clients which we will need to do for the skeletal
# increment


def main():
    print("Welcome to Clue-Less!")

    # get users name
    while True:
        name = input("Please enter your name: ")
        if 0 < len(name) < 20:
            break
        else:
            print(
                "Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")
    client_manager = Client()
    client_id = client_manager.connect_to_server(name)
    client_manager.join_waiting_lobby(GAME_STATE)
    client_manager.disconnect_from_server()
    quit()


if __name__ == "__main__":
    main()
