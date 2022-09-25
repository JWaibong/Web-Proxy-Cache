
from socket import *
from lib import HTTPRequest
import sys
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
        url = req.url

        if len(url) > 1:
            url = url[1:]

        if url.startswith("http://"):
            url = url[7:]
        if url.startswith("www."):
            url = url[4:]

        tokens = url.split("/") 
        
        resource = ""
        if len(tokens) <= 1:
            resource = ""
        else:
            url = tokens[0]
            resource = '/'.join(tokens[1:]) #for example www.google.com/a/b/c/index.html => /a/b/c/index.html 

        if url == "favicon.ico":
            print("Cannot handle favicon.ico request", file=sys.stderr)
            connSock.close()
            continue

        print(url+"/"+resource)
        #strip off "http://" and "www." from the url
        if req.type == "GET":
            if url+"/"+resource in cache:

                print("Requested file found in cache: {}".format(url+"/"+resource), file=sys.stderr)
                connSock.send(cache[url+"/"+resource])
                connSock.close()
            else: #need to make an explicit request
                try:
                    ip = gethostbyname(url)
                    newReq = "GET /{} HTTP/1.1\r\nHost: {}\r\nAccept: text/html \r\n\r\n".format(resource, url)

                    clientSock = socket(AF_INET, SOCK_STREAM)
                    clientSock.connect((ip, 80))
                    clientSock.send(newReq.encode())
                    msg = b""
                    while True:
                        bytes = clientSock.recv(4096)
                        msg += bytes
                        if len(bytes) < 4096:
                            break
                        

                    print("response received: {}".format(url+"/"+resource), file=sys.stderr)
                    #print(msg.decode("utf-8"), file=sys.stderr)

                    cache[url+"/"+resource] = msg

                    clientSock.close()
                    connSock.send(msg)
                    connSock.close()
                except:
                    print("Could not resolve host ip adddress", file=sys.stderr)
                    connSock.close()
                    continue
        else: 
            print("Unimplemented handling for this http request type lol")
        

    return


if __name__ == "__main__":
    main()