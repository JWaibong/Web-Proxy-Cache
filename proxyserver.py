
from socket import *
from lib import HTTPRequest
import sys
def main():

    cache = {} # cache internally represented as hashmap from string to bytes
    port = 8888


    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(("127.0.0.1", port))
    serverSock.listen(1)
    while True:
        connSock, addr = serverSock.accept()
        print("Connected to " + str(addr))
        msg = connSock.recv(2048).decode("utf-8")

        req = HTTPRequest(msg) # parse the info from the http request
        url = req.url

        if len(url) > 1:
            url = url[1:]

        #strip off "http://" and "www." from the url
        if url.startswith("http://"):
            url = url[7:]
        if url.startswith("www."):
            url = url[4:]

        tokens = url.split("/") 
        
        resource = ""
        if len(tokens) > 1:
            # separate the beginning part of the url from the resource part
            #for example for google.com/a/b/c/index.html
            url = tokens[0] # => url == "google.com"
            resource = '/'.join(tokens[1:]) #=> resource == "/a/b/c/index.html"
        
        if url == "favicon.ico":
            print("Cannot handle favicon.ico request", file=sys.stderr) 
            connSock.close()
            continue

        completeURL = "{}/{}".format(url, resource) # join URL back together so we can search for it in the cache (hashmap)
        print(completeURL)
        if req.type == "GET":
            if completeURL in cache:

                print("Requested file found in cache: {}".format(completeURL), file=sys.stderr)
                connSock.send(cache[completeURL]) # send the cached HTTP response (real server would make a new response and store only the file in cache)
                connSock.close()
            else: #need to make an explicit request
                try:
                    ip = gethostbyname(url) # this can fail and raise an exception
                    newReq = "GET /{} HTTP/1.1\r\nHost: {}\r\nAccept: */* \r\n\r\n".format(resource, url)

                    clientSock = socket(AF_INET, SOCK_STREAM) 
                    clientSock.connect((ip, 80)) # create a socket and connect with the server specified by URL in client's request
                    clientSock.send(newReq.encode())
                    msg = b""
                    while True:
                        bytes = clientSock.recv(4096) # read from the socket 4096 bytes at a time
                        msg += bytes
                        if len(bytes) < 4096: # reading < 4096 bytes means there's nothing left to read 
                            break
                        

                    print("response received: {}".format(url+"/"+resource), file=sys.stderr)
                    #print(msg.decode("utf-8"), file=sys.stderr) # uncommented because the entire http response can be huge

                    cache[completeURL] = msg #cache the http response, file included

                    clientSock.close() 
                    connSock.send(msg)
                    connSock.close() #close both sockets
                except:
                    print("Could not resolve host ip adddress", file=sys.stderr)
                    connSock.close()
                    continue
        else: 
            print("Unimplemented handling for this http request type lol")
        

    return


if __name__ == "__main__":
    main()