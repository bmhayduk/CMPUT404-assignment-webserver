# coding: utf-8

import SocketServer
import os
import posixpath



# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

"""
Example of General Formatting Guidelines

Response:

= Status-Line
*(( general-header | response-header | entity-header ) CRLF)
CLRF
[ message-body ] 

HTTP/1.1 404 Not Found
Date: Sun, 19 Jan 2014 09:35:21 GMT
Content-Type: text/html
Content-Length: 1354

<html>
...

</html> 
"""


returnCodes = {"200":" 200 OK", "404": " 404 Not Found"}
returnTypes = {"html":"Content-Type: text/html", "css":"Content-Type: text/css"}
EOL = "\r\n"
HTTP = "HTTP/1.1"

class MyWebServer(SocketServer.BaseRequestHandler):
   
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #Begin breakdown of request
        lines = self.data.splitlines()
        # print(lines[0])
        getline = lines[0]
        elements = getline.split(" ")

        #Get the path and http version of request
        path = elements[1]    
        httpversion = elements[2]
        #Create the response based on the path
        response = self.servePathResponse(path)

        self.request.sendall(response)

    def servePathResponse(self, path):
        """
        This function will take an input path and serve a response 
        accordingly
        List of free tests:
        >>> servePathResponse("/base.css")
        >>> servePathResponse("/")
        >>> servePathResponse("index.html")
        >>> servePathResponse("/do-not-implement...")
        """ 

        #Compose path consisting of root for server
        workingDir = os.getcwd() + "/www"
        #Normalize the path 
        finalPath = posixpath.normpath(workingDir + path)

            #Handle .html & css cases
        if os.path.exists(finalPath) and os.path.isfile(finalPath):
             if finalPath.startswith(workingDir):
                 ftype = path.split('.')[-1]
                 if(ftype == 'css') or (ftype == 'html'):
                     try:
                         htmlFile = open(finalPath, 'r') 

                         response = HTTP + " " + returnCodes["200"] + EOL + returnTypes[ftype] + EOL + EOL + htmlFile.read()
                     except:
                         None

                 else:
                      response = self.gen404()
             else:
                  response = self.gen404()

        #Handle case of paths ending with '.../' 
        elif path.endswith('/'):
            #handle if only served '/' 
            if path == '/':
                workingDir += "/index.html"
            else:
                workingDir = workingDir + path + 'index.html'
            if workingDir.startswith(finalPath):
                try:
                    htmlfile = open(workingDir, 'r')
                except:
                    None

                response = HTTP + " " + returnCodes["200"] + EOL + returnTypes["html"] + EOL + EOL + htmlfile.read()

            else:
                response = self.gen404()

        #If it is not html, css or a directory we are not able to find what they are looking for
        else:
           response = self.gen404()

       # print(response.splitlines()[0])
       # print(response.splitlines()[1])
       # print(response.splitlines()[2])
        print(EOL)
        return response

    #Format response when resource not found 
    def gen404(self):
        response = (HTTP + " " + returnCodes["404"] + EOL + returnTypes["html"] + EOL + EOL + "<!DOCTYPE html>\n" + "<html><body>" + HTTP + " " + returnCodes["404"] + "\n" + "</body></html>")
        return response


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
