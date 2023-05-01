#############################################################################
# The chat client
#############################################################################
# ! /usr/bin/env python

"""
Simple chat client for the chat server. Defines
a simple protocol to be used with chatserver.

"""

import socket
import sys
import select
from communication import send, receive

BUFSIZ = 1024


class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self):
        self.name = input("Введите своё имя")
        # Quit flag
        self.flag = False
        self.port = 11490
        self.host = '127.0.0.1'
        # Initial prompt
        self.prompt = '[' + '@'.join((self.name, socket.gethostname().split('.')[0])) + ']> '
        # Connect to server at port
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            print('Connected to chat server@%d' % self.port)
            # Send my name...
            self.client.send(('NAME: ' + self.name).encode())
            data = self.client.recv(4096)
            # Contains client address, set it
            addr = data.decode().split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error as e:
            print(
                'Could not connect to chat server @%d' % self.port)
            sys.exit(1)

    def cmdloop(self):

        while not self.flag:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin & socket
                inputready, outputready, exceptready = select.select([0, self.sock], [], [])

                for i in inputready:
                    if i == 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)
                    elif i == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Shutting down.')
                            self.flag = True
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print('Interrupted.')
                self.sock.close()
                break


if __name__ == "__main__":
    import sys

    # if len(sys.argv) < 3:
    #     sys.exit('Usage: %s chat id host no port founded' % sys.argv[0])

    client = ChatClient()
    client.cmdloop()
