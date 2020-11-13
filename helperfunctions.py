import json

# Some helper functions to send data between server and clients
def send(socket, data):
    """
    Helper method to send data to server/client.
    Args: 
        socket: The point of connection between the client and server.
        data: The data to be sent.
    """
    try:
        serialized = json.dumps(data)
    except (TypeError, ValueError) as e:
        raise Exception('You can only send JSON-serializable data')
    # send the length of the serialized data first
    socket.send('{}\n'.format(len(serialized)).encode()) 
    # send the serialized data
    socket.sendall(serialized.encode())


def recv(socket):
    """
    Helper method to receive data from the client/server.
    Args: 
        socket: The point of connection between the client and server.
    Returns:
        A JSON string containing data received.
    """
    # read the length of the data, letter by letter until we reach EOL
    length_str = ''
    char = socket.recv(1).decode()
    while char != '\n':
        length_str += char
        char = socket.recv(1).decode()
    total = int(length_str)
    # use a memoryview to receive the data chunk by chunk efficiently
    view = memoryview(bytearray(total))
    next_offset = 0
    while total - next_offset > 0:
        recv_size = socket.recv_into(view[next_offset:], total - next_offset)
        next_offset += recv_size
    try:
        deserialized = json.loads(view.tobytes())
    except (TypeError, ValueError) as e:
        raise Exception('Data received was not in JSON format')
    return deserialized


def sendjson(socket, data):
    """
    Send a JSON string to the client/server represented by the socket.
    Args: 
        socket: The point of connection between the client and server.
        data: The data to be sent.
    """
    if not socket:
        raise Exception('You have to connect first before sending data')
    send(socket, data)
    # return self


def recvjson(socket):
    """
    Receive a JSON string from the client/server represented by the socket.
    Args: 
        socket: The point of connection between the client and server.
    Returns:
        A JSON string containing data received.
    """
    if not socket:
        raise Exception('You have to connect first before receiving data')
    return recv(socket)


def convert_into_real_position(position):
    """
    Transforms String representation of position to a tuple
    containing integers.
    Args:
        position: A String representation of the (x, y) coordinates of a position.
    Returns:
        A tuple containing integers of the (x, y) coordinates given as input.
    """
    return (int(position[1]), int(position[4]))