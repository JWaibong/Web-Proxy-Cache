import os
from socket import *
from lib import HTTPRequest, HTTPResponse  #my own code

def main():

    port = 80

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(("127.0.0.1", port))
    serverSock.listen(1)

    print("Currently in " + os.getcwd())
    while True:
        connSock, addr = serverSock.accept()
        print("Connected to " + str(addr))
        msg = connSock.recv(2048).decode("utf-8")

        req = HTTPRequest(msg)

        if req.type == "GET":
            status = req.validate_url()

            res = HTTPResponse(status, req)
            res.read_file()
            connSock.send(res.res.encode())
            #print("sent")

        else: 
            print("Unimplemented handling for this http request type lol")


    return


if __name__ == "__main__":
    main()