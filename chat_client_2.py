# telnet program example
import socket
import select
import sys


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


# main function
if __name__ == "__main__":

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    client.settimeout(2)
    running = 1
    # connect to remote host
    try:
        client.connect(('192.168.100.16', 12000))
        print('Подключение к серверу прошло успешно. Можно отправлять сообщения')
        username = input('Введите своё имя  \n')
        client.send(username.encode())
        prompt()
    except:
        print('Не удалось подключиться')
        sys.exit()

    # print('Connected to remote host. Start sending messages')
    # prompt()

    while running:
        socket_list = [sys.stdin, client]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            # incoming message from remote server
            if sock == client:
                data = sock.recv(4096).decode()
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    prompt()
            # user entered a message
            else:
                msg = sys.stdin.readline()
                if msg.rstrip('\n') == "exit":
                    client.close()
                    running = 0
                    break
                else:
                    client.send(msg.encode())
                    prompt()
