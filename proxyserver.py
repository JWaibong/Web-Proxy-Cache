
from socket import *
#from os import getcwd
from lib import HTTPRequest, HTTPResponse
        

def main():

    port = 8888

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(("127.0.0.1", port))
    serverSock.listen(1)
    while True:
        connSock, addr = serverSock.accept()
        print("Connected to " + str(addr))
        msg = connSock.recv(2048).decode("utf-8")

        req = HTTPRequest(msg)

        if req.type == "GET":
            status = req.validate_url()

            res = HTTPResponse(status, req)
            connSock.send(res.res.encode())

        else: 
            print("Unimplemented handling for this http request type lol")
    return


if __name__ == "__main__":
    main()