import select
import socket
import sctp


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message):
    # Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server and socket != sock:
            try:
                socket.send(message.encode())
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)


def getname(client_socket):
    # Return the printable name of the
    # client, given its socket...
    info = clientmap[client_socket]
    host, name = info[0][0], info[1]
    return '@'.join((name, host))


if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 12000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    # this has no effect, why ?
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', PORT))
    server.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server)
    clientmap = {}

    print("Chat server started on port " + str(PORT))

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server:
                # Handle the case in which there is a new connection recieved through server_socket
                conn, addr = server.accept()
                CONNECTION_LIST.append(conn)
                clientname = conn.recv(RECV_BUFFER).decode()
                clientmap[conn] = (addr, clientname)
                print("Client <%s> connected" % clientname)
                broadcast_data(conn, "<%s> entered room\n" % clientname)

            # Some incoming message from a client
            else:
                # Data received from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER).decode()
                    if data:
                        broadcast_data(sock, "\r" + '<' + getname(sock) + '> ' + data)
                except:
                    broadcast_data(sock, "Client (%s) is offline" % getname(sock))
                    print("Client (%s) is offline" % getname(sock))
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server.close()
