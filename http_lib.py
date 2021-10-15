import os
import shutil
import socket
import datetime
import threading
import urllib
from urllib.parse import urlparse

from env import Debug

FORMAT = 'utf-8'
BUFFER_SIZE = 102400


class httpserver:
    """This is the http class for Server side operations"""

    directory = "./data"
    is_get = is_post = False

    def __init__(self, verbose, directory):
        """Init required params"""
        self.verbose = verbose
        if directory is not None:
            self.directory = directory
        # For Path & Extra Params
        self.path = self.query = self.body = None

    def parse(self, request):
        header_lines = request[0].split("\r\n")

        # GET /get?course=networking&assignment=1 HTTP/1.1
        first_header_line = header_lines[0]
        req_type = str(first_header_line.split()[0]).upper()

        # Parse the path & query
        self.parse_url(first_header_line.split()[1])

        # Parse Headers
        # Some point in future LOL ;)

        # Store the request body
        if len(request) > 1:
            self.body = request[1]

        # Get Request Type
        if "GET" == req_type:
            self.is_get = True
            return self.get_handler()
        elif "POST" == req_type:
            self.is_post = True
            return self.post_handler()

    def parse_url(self, url):
        parsed_url = urlparse(url)
        self.path = parsed_url.path
        self.query = parsed_url.query

    def get_handler(self):
        files = self.get_files()
        body = ""
        if self.path == "/":
            body = "\n".join(files)
            return self.response_generator(code=200,body=body)
        else:
            file = [p for p in self.path.split("/") if p][0]
            if file in files:
                with open(self.directory+'/'+file, 'r') as file:
                    body = file.read()
                return self.response_generator(code=200, body=body)
            else:
                body = "404. That’s an error.\n"
                body += "The requested URL " + self.path+" was not found on this server.\n"
                body += "That’s all we know."

                return self.response_generator(code=404, body=body)

    def post_handler(self):
        files = self.get_files()
        body = ""

        file = [p for p in self.path.split("/") if p][0]
        # File exist
        if file in files:
            body = "File has been successfully overwritten."
            self.create_file(file, self.body)
            return self.response_generator(code=204, body=body)
        else:
            body = "File has been successfully created."
            self.create_file(file, self.body)
            return self.response_generator(code=201, body=body)

    def response_generator(self,code,body):
        # Create Response
        response = ""
        if code == 200:
            response += "HTTP/1.1 200 OK\r\n"
        if code == 201:
            response += "HTTP/1.1 201 Created\r\n"
        if code == 204:
            response += "HTTP/1.1 204 No Content\r\n"
        elif code == 404:
            response += "HTTP/1.1 404 Not Found\r\n"

        response += "Date: " + self.get_time() + "\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Content-Length: "+str(len(body)) + "\r\n"
        response += "Server: httpfs/1.0\r\n"
        if code == 201:
            response += "Location: "+self.path+"\r\n"
        response += "\r\n"
        response += body

        return response

    def get_files(self):
        list_of_files = []
        for root, dirs, files in os.walk(self.directory, topdown=True):
            dirs.clear()
            for name in files:
                list_of_files.append(name)
        return list_of_files

    def get_time(self):
        return str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))

    def create_folder(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def create_file(self, name, text):
        f = open(self.directory+'/'+name, "w")
        f.write(text)
        f.close()

    def save(self, id, name, content):
        self.create_folder(self.directory + "/" + id)
        self.create_file(self.directory + "/" + id + "/" + name, str(content))

    def remove_old_outputs(self):
        try:
            shutil.rmtree(self.directory)
        except:
            pass


def run_server(host, port, verbose, directory):
    port = int(port)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #  This allows the address/port to be reused immediately instead of
    #  it being stuck in the TIME_WAIT state for several minutes, waiting for late packets to arrive.
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listener.bind((host, port))
        listener.listen(5)  # ?
        print('Server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr, verbose, directory)).start()
    finally:
        listener.close()


def handle_client(conn, addr, verbose, directory):
    if Debug:
        print('------------------------------------------')
        print('New client from', addr)
        print('------------------------------------------')

    try:
        request = conn.recv(BUFFER_SIZE)

        request = request.decode(FORMAT)

        if verbose:
            print(request.strip(), "\n")

        server = httpserver(verbose=verbose, directory=directory)
        # Divide Request to 2 parts (Header & Body)
        request = request.split("\r\n\r\n")
        # Parse Request Here and Return the Response
        response = server.parse(request)
        # Demo Response
        # response = """HTTP/1.1 200 OK\r\nDate: """ + server.get_time() + """"\r\nServer: httpfs/1.0\r\n\r\nHello test is working!"""
        response = response.encode(FORMAT)
        conn.sendall(response)
        # Question: Connection should be persistence or non-persistence?
        # I think it's non-persistence.
    finally:
        conn.close()