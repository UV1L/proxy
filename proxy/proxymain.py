import socket
import sys
import threading
import server as ser
import argparse
import select


class Params:
    flag = False
    input_list = set()
    connections = {}
    for_del = []


parser = argparse.ArgumentParser(description='You started a proxy-script.'
                                             ' Enter your port to use '
                                             'this. Good luck!')
parser.add_argument('-p', '--port', help='This will be your port')
port = parser.parse_args().port


def main():
    """This method are getting data
     from browser and starts handle_request or delete socket"""
    print("Waiting for connect")
    param = Params()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', int(port)))
        s.listen(200)
        param.input_list.add(s)
    except Exception as e:
        sys.exit(e)

    while True:
        try:
            inputs, _, _ = select.select(param.input_list, [], [])
            for sock in inputs:
                if sock == s:
                    client, addr = s.accept()
                    data = receive(client)
                    threading.Thread(target=ser.Server.handle_request, args=(
                        client, addr, data, param
                    )).start()
                else:
                    data = receive(sock)
                    if not data:
                        param.for_del.append(sock)
                    else:
                        param.connections[sock].send(data)
        except ConnectionResetError:
            client.close()
        try:
            for _s in param.for_del:
                if _s == s:
                    continue
                _s.close()
                param.input_list.remove(_s)
                if param.connections[_s] in param.input_list:
                    param.input_list.remove(param.connections[_s])
                del param.connections[_s]
        except:
            pass


def receive(s):
    """This method receiving data"""
    s.settimeout(1)
    try:
        data = b''
        while True:
            part = s.recv(8192)
            if not part:
                return data
            data += part
    finally:
        return data


if __name__ == '__main__':
    main()
