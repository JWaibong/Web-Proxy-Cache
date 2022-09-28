
from socket import *
from lib import HTTPRequest # my own code found in lib.py
import sys
def main():
    cache = {} # cache internally represented as hashmap from string to bytes
    ipCache = {}
    port = 8888


    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # makes it so that the OS doesnt say port already in use after killing the process
    serverSock.bind(("127.0.0.1", port))
    serverSock.listen(1)
    try:
        while True:
            connSock, addr = serverSock.accept()
            #print("Connected to " + str(addr))
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
            
            if url == "favicon.ico": #cannot handle this so just ignore
                #print("Cannot handle favicon.ico request", file=sys.stderr) 
                connSock.close()
                continue

            completeURL = "{}/{}".format(url, resource) # join URL back together so we can search for it in the cache (hashmap)
            if req.type == "GET":
                if completeURL in cache:

                    print("Requested file found in cache: {}".format(completeURL), file=sys.stderr)
                    f, fileLength, contentType = cache[completeURL]
                    resp = "HTTP/1.1 200 OK\r\nContent-Length: {}\r\n{}\r\n\r\n".format(fileLength, contentType)
                    connSock.send(resp.encode() + f) # send the cached file
                    connSock.close()
                else: #need to make an explicit request
                    print("Client Requested Resource Not Cached: " + completeURL)
                    ip = ""
                    #print("Attempting to connect to {}".format(url))
                    if url in ipCache:
                        ip = ipCache[url]
                    else:
                        try:
                            ip = gethostbyname(url) # this raise an exception if the function fails to resolve hostname to ip address
                        except:
                            print("Could not resolve host ip adddress, {}".format(url), file=sys.stderr)
                            connSock.close()
                            continue
                    

                    newReq = "GET /{} HTTP/1.1\r\nHost: {}\r\nAccept: */* \r\n\r\n".format(resource, url)
                    clientSock = socket(AF_INET, SOCK_STREAM) 
                    clientSock.connect((ip, 80)) # create a socket and connect with the server specified by URL in client's request
                    clientSock.send(newReq.encode())

                    msg = b""
                    f = b""
                    
                    #STEP 1: READ RESPONSE FROM SERVER UP UNTIL \r\n\r\n INDICATING THE START OF THE FILE
                    while True:
                        bytes = clientSock.recv(8192) # read from the socket 8192 bytes at a time
                        msg += bytes
                        attemptToSplitHeader = msg.decode(errors="ignore").split("\r\n\r\n")
                        if (len(attemptToSplitHeader) > 1):
                            header = attemptToSplitHeader[0]
                            f += msg[len(header) + 4:] # it's possible to have read past the header. This would be the beginning of the file
                            break
                    
                    headerLines = header.split("\r\n") 
                    
                    #STEP 2: EXTRACT THE Content-Type AND Content-Length FIELDS OF THE HEADER
                    contentType = ""
                    fileLength = 0
                    foundLength = False
                    foundType = False
                    for line in headerLines:
                        if foundLength and foundType:
                            break
                        if line.startswith("Content-Length:"):
                            fileLength = int(line[16:].rstrip()) 
                            #print("Length as described in header " + str(fileLength))
                            foundLength = True
                        elif line.startswith("Content-Type:"):
                            contentType = line
                            foundType = True
                    
                    #STEP 3: READ THE REST OF THE FILE CONTENT FROM THE RESPONSE
                    currentLength = len(f) # > 0 if we accidentally read past the header and \r\n\r\n
                    byteArr = []
                    while currentLength < fileLength:
                        bytes = clientSock.recv(8192)
                        if(len(bytes) == 0):
                            break
                        byteArr.append(bytes)
                        currentLength += len(bytes)
                    #print(currentLength)
                    f += b"".join(byteArr)
                    #print(len(f))

                    #STEP 4: SEND THE ENTIRE RESPONSE BACK TO THE CLIENT
                    msg = (header + "\r\n\r\n").encode() + f # THIS IS THE FULL RESPONSE
                    print("Length {}: response received from {}\n{}\n".format(len(f), url+"/"+resource, header), file=sys.stderr)

                    #STEP 5: CACHE THE FILE IN PROCESS MEMORY, ALONG WITH ITS LENGTH AND TYPE
                    cache[completeURL] = (f, fileLength, contentType)
                    if url not in ipCache:
                        ipCache[url] = ip #CACHE THE IP ADDRESS TOO
                    clientSock.close() 
                    connSock.send(msg)
                    connSock.close() #CLOSE BOTH SOCKETS
            else: 
                print("Unimplemented handling for this http request type", file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
        serverSock.close()
        sys.exit(-1) #any regular errors should terminate program

    return


if __name__ == "__main__":
    main()