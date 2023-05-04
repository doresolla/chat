# telnet program example
import socket
import select
import string
import sys


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


# main function
if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    s.settimeout(2)
    running = 1
    # connect to remote host
    try:
        s.connect(('localhost', 12000))
        print('Подключение к серверу прошло успешно. Можно отправлять сообщения')
        username = input('Введите своё имя  \n')
        s.send(username.encode())
        prompt()
    except:
        print('Не удалось подключиться')
        sys.exit()

    # print('Connected to remote host. Start sending messages')
    # prompt()

    while running:
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
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
                if msg == 'exit':
                    s.close()
                    running = 0
                    break
                else:
                    s.send(msg.encode())
                    prompt()
