#! /usr/bin/env python
import socket
import webbrowser
import time


def parse_details(client_data):
    """This method are parsing data and returns it"""

    try:
        lines = client_data.splitlines()
        while lines[len(lines)-1] == '':
            lines.remove('')
        first_line_tokens = lines[0].split()
        url = first_line_tokens[1]

        url_pos = url.find(b"://")
        if url_pos != -1:
            url = url[(url_pos+3):]

        port_pos = url.find(b":")
        path_pos = url.find(b"/")
        if path_pos == -1:
            path_pos = len(url)

        if port_pos == -1 or path_pos < port_pos:
            server_port = 80
            server_url = url[:path_pos]
        else:
            server_port = int(url[(port_pos+1): path_pos])
            server_url = url[:port_pos]

        first_line_tokens[1] = url[path_pos:]
        lines[0] = b' '.join(first_line_tokens)
        client_data = b"\r\n".join(lines) + b'\r\n\r\n'

        a = {
            "server_port": server_port,
            "server_url": server_url,
            "client_data": client_data,
            "method": first_line_tokens[0]
        }
        print(a)
        return a
    except:
        pass


class Server:
    @staticmethod
    def serve_get(client_socket, details):
        """This method are connecting to the webserver if method is GET"""

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((details["server_url"], details["server_port"]))
            server_socket.send(details["client_data"])

            reply = server_socket.recv(8192)
            server_socket.settimeout(0.4)
            while len(reply):
                try:
                    client_socket.send(reply)
                    reply = server_socket.recv(8192)
                except socket.timeout:
                    break
            client_socket.send(b"\r\n\r\n")
            print(reply)
            server_socket.close()
            client_socket.close()
            return
        except Exception as e:
            server_socket.close()
            client_socket.close()
            print(e)
            return

    @staticmethod
    def serve_connect(client_socket, details, param):
        """This method are connecting
        to the webserver if
         method is CONNECT (for https only)"""

        print(details["server_url"])
        conn = socket.socket()
        param.connections[client_socket] = conn
        param.connections[client_socket].connect((details["server_url"], details["server_port"]))
        param.connections[client_socket].settimeout(0.3)
        param.connections[conn] = client_socket
        param.input_list.add(conn)
        param.input_list.add(client_socket)
        client_socket.send((b"HTTP/1.1 200 Connection established\r\n"
                            b"Date: Fri, 1 Jun 2019 13:21:53 GMT\r\n"
                            b"Server: Apache/2.2.14 (Win64)\r\n"
                            b"\r\n"))

    @staticmethod
    def handle_request(socket, addr, data, param):
        """This method starts parse_details and serve_get or serve_connect"""
        details = parse_details(data)

        if not details:
            socket.close()
            return

        ban_list = open("BanList.txt", "r").read()
        if str(details["server_url"].decode()) in ban_list:
            if param.flag == False:
                webbrowser.open(r"ban.png")
                param.flag = True
                time.sleep(10)
            param.flag = False
            param.for_del.append(socket)
            socket.close()
            return

        if details['method'] == b'GET':
            Server.serve_get(socket, details)
            socket.close()

        elif details['method'] == b'CONNECT':
            Server.serve_connect(socket, details, param)




