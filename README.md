Testing was done on WSL Ubuntu with Google Chrome as the client browser. The version of python used was 3.8.10

To run part A (sudo was necessary for me in order for the process to gain network capabilities): 
```sudo python3 webserver.py```
Runs on port 80 at ip 127.0.0.1
Typing ```127.0.0.1:80/HelloWorld.html``` into the search bar will retrieve the requested html file from the server

To run part B: 
```sudo python3 proxyserver.py```
Runs on port 8888 at ip 127.0.0.1

A demonstration of the proxy server caching files is found in ```client_screenshots.pdf```

Make sure to disable caching in the dev console (and keep the dev console open the entire time). Do not close the tab because this will enable caching again. If you request a webpage from the proxy, close the tab, open a new tab, and then request the same webpage again, then the browser will prefer using its own cache over the proxy server's.  

I tested the proxy server by typing, for instance ```127.0.0.1:8888/http://example.com```, into the search bar rather than setting up the browser to use the proxy directly.

Some webpages the proxy server works with:

http://gaia.cs.umass.edu/

http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html

http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html

http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html

http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file5.html

http://www.columbia.edu/~fdc/sample.html

http://www.gnu.org/doc/doc.html

http://example.com

http://wa.gov/