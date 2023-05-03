import select
import socket
import sys
import signal
from communication import send, receive


def getname(client_socket):
    # Return the printable name of the
    # client, given its socket...
    info = clientmap[client_socket]
    host, name = info[0][0], info[1]
    return '@'.join((name, host))


if __name__ == "__main__":
    BUFSIZ = 1024
    server = socket.socket(socket.AF_INET,  socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    server.bind(('', 12000))
    server.listen(10)
    print("Сервер работает")

    clientmap = {}
    inputs = [server, sys.stdin]
    outputs = []
    clientsnumber = 0
    running = 1
    while running:
        try:
            inputready, outputready, exceptready = select.select(inputs, outputs, [])
        except select.error as e:
            break
        except socket.error as e:
            break
        for conn in inputready:
            if conn == server:
                client, address = server.accept()
                print("%d client connected from %s" % (client.fileno(), address))
                username = receive(client).split('NAME: ')[1]

                clientsnumber += 1
                clientmap[client] = (address, username)
                inputs.append(client)

                msg = '\n Новый пользователь ' % username + ' присоединился'
                outputs.append(client)
                for out in outputs:
                    send(out, msg)

            elif conn == sys.stdin:
                junk = sys.stdin.readline()
                running = 0
            else:
                try:
                    data = receive(conn)
                    if data:
                        msg = '\n#[' + getname(conn) + '] >> ' + data
                        for out in outputs:
                            if out != conn:
                                send(out, msg)
                    else:
                        print('ChatServer %d hung up ' % conn.fileno())
                        clientsnumber -= 1
                        conn.close()
                        inputs.remove(conn)
                        outputs.remove(conn)
                        msg = '\n(Hung up :Client  %s)' % getname(conn)
                        for out in outputs:
                            send(out, msg)
                except socket.error as e:
                    inputs.remove(conn)
                    outputs.remove(conn)
        server.close()