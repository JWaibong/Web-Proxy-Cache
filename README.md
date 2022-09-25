Testing was done on WSL Ubuntu to run the python files and Google Chrome as the client browser

To run part A (sudo was necessary for me in order to gain network capabilities): 
```sudo python3 webserver.py```
Runs on port 80 at ip 127.0.0.1
Typing ```127.0.0.1:80/HelloWorld.html``` into the search bar will retrieve the requested html file from the server

To run part B: 
```sudo python3 proxyserver.py```
Runs on port 8888 at ip 127.0.0.1

A demonstration of the proxy server caching files (the program currently stores the original HTTP response along with the file, but I'm aware an actual server would create a new HTTP response and store only the file) is found in client_screenshots.pdf.

Make sure to disable caching in the dev console (and keep the dev console open the entire time). Do not close the tab because this will enable caching again. If you request a webpage from the proxy, close the tab, open a new tab, and then request the same webpage again, then the browser will prefer using it's own cache over the proxy server.  

I tested the proxy server by typing, for instance ```127.0.0.1:8888/http://example.com``` into the search bar rather than setting up the browser to use the proxy directly.

Some webpages the proxy server works with:
http://www.columbia.edu/~fdc/sample.html

http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html

http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html

http://www.gnu.org/doc/doc.html

http://nginx.org

http://example.com

http://wa.gov/