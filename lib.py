import os
import socket

def resolve_url_as_ipv4(url: str) -> str:
    ip = ""

    

    return ip
class HTTPRequest:
    def __init__(self, req):
        
        lines = req.split("\r\n")
        
        typeLine = lines[0].split(" ")
        type = typeLine[0]

        self.type: str = type
        self.url: str = typeLine[1]
        self.path: str = os.getcwd() + self.url
        return
    
    def validate_url(self):
        if not os.path.isfile(self.path):
            return 404

        return 200

class HTTPResponse:
    def __init__(self, status, req: HTTPRequest):
        self.status = status
        self.res = "HTTP/1.1 "

        if status == 404:
            self.res = "HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<html> <body> <h1> 404 NOT FOUND </h1> </body> </html>"
        elif status == 200:

            self.res += "200 OK\r\n"
            fileType = req.path.split(".")[-1]
            
            self.contentLength = "Content-Length: "
            self.contentType = "Content-Type: "

            if fileType == "html":
                self.contentType += "text/html; charset=utf-8\r\n"
            else:
                self.contentType += "text/plain; charset=utf-8\r\n" #unimplemented for other types of files
            

            self.path = req.path
            return
        return
    def read_file(self):
        buf = ""
        with open(self.path, "r") as f:
            buf += "".join(f.readlines())
        
        self.contentLength += (str(len(buf)) + "\r\n")
        
        self.res += self.contentLength
        self.res += self.contentType
        self.res += "\r\n"
        self.res += buf
        return