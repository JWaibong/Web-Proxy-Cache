
from http import client, server
from socket import *
#from os import getcwd
from lib import HTTPRequest, HTTPResponse

import requests
def main():

    cache = {}
    port = 8888

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(("127.0.0.1", port))
    serverSock.listen(1)
    while True:
        connSock, addr = serverSock.accept()
        print("Connected to " + str(addr))
        msg = connSock.recv(2048).decode("utf-8")

        req = HTTPRequest(msg)
        #connSock.send(res.res.encode())
        if req.type == "GET":
            if req.url in cache:


                return 
            else: #need to make an explicit request 
                #print(req.url[1:])
                #https://stackoverflow.com/questions/22492484/how-do-i-get-the-ip-address-from-a-http-request-using-the-requests-library?noredirect=1&lq=1
                url = req.url[1:]

                startsWithHTTP = True
                if not url.startswith("http://"):
                    startsWithHTTP = False


                tokens = url.split("/") if not startsWithHTTP else url[7:].split("/")

                if not startsWithHTTP:
                    url = "http://" + url
                
                resource = ""
                if len(tokens) <= 1:
                    resource = "/"
                else:
                    resource = '/'.join(tokens[1:]) #for example www.google.com/a/b/c/index.html => /a/b/c/index.html 

                
                getIP = requests.get(url, stream=True)
                
                ip, port = getIP.raw._connection.sock.getsockname()
                print(ip)
                newReq = "GET {} HTTP/1.1\r\n".format(resource)
                print(newReq)
                print(url)

                clientSock = socket(AF_INET, SOCK_STREAM)
                clientSock.connect((ip, 80))
                clientSock.send(newReq)

                msg = clientSock.recv(2048)
                print(msg.decode("encoding=utf-8"))
                #connSock.close()
                #serverSock.close()
        else: 
            print("Unimplemented handling for this http request type lol")
        

    return


if __name__ == "__main__":
    main()