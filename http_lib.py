import os
import shutil
import socket
import datetime
import threading
from urllib.parse import urlparse

from env import Debug


class httpserver:
    """This is the http class for Server side operations"""
    port = 8080
    host = ""  # localhost
    directory = "data"
    is_get = is_post = False

    FORMAT = 'utf-8'
    BUFFER_SIZE = 102400

    def __init__(self, verbose, port, directory):
        """Init required params"""
        self.verbose = verbose
        if port is not None:
            self.port = int(port)
        if directory is not None:
            self.directory = directory
        # For Path & Extra Params
        self.path = self.query = self.body = None

    def run_server(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #  This allows the address/port to be reused immediately instead of
        #  it being stuck in the TIME_WAIT state for several minutes, waiting for late packets to arrive.
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listener.bind((self.host, self.port))
            listener.listen(5)  # ?
            print('Server is listening at', self.port)
            while True:
                conn, addr = listener.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        finally:
            listener.close()

    def handle_client(self, conn, addr):
        print('New client from', addr)
        try:
            request = conn.recv(1024)

            request = request.decode(self.FORMAT)

            if self.verbose:
                print(request.strip(), "\n")

            # Divide Request to 2 parts (Header & Body)
            request = request.split("\r\n\r\n")
            # Parse Request Here and Return the Response
            response = self.parse(request)
            # Demo Response
            response = """HTTP/1.1 200 OK\r\nDate: """ + self.get_time() + """"\r\nServer: httpfs/1.0\r\n\r\nHello test is working!"""
            response = response.encode(self.FORMAT)
            conn.sendall(response)
            # Question: Connection should be persistence or non-persistence?
            # I think it's non-persistence.
        finally:
            conn.close()

    def parse(self, request):
        header_lines = request[0].split("\r\n")

        # GET /get?course=networking&assignment=1 HTTP/1.1
        first_header_line = header_lines[0]

        # Get Request Type
        if "GET" in first_header_line:
            self.is_get = True
        elif "POST" in first_header_line:
            self.is_post = True
        # Parse the path & query
        self.parse_url(first_header_line.split()[1])

        # Parse Headers
        # Some point in future LOL ;)

        # Store the request body
        if len(request) > 1:
            self.body = request[1]


        if Debug: print("is_get:",self.is_get,"is_post:",self.is_post,"Path:",self.path,"Query:",self.query,"Body:",self.body)

    def parse_url(self, url):
        parsed_url = urlparse(url)
        self.path = parsed_url.path
        self.query = parsed_url.query

    def get_handler(self, request):
        pass

    def post_handler(self, request):
        pass

    def load_folders(self):
        input_folders = []
        for root, dirs, files in os.walk(self.directory, topdown=False):
            for name in dirs:
                input_folders.append(os.path.join(name))
        return input_folders

    def get_time(self):
        return str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))

    def create_folder(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def create_file(self, file_path, text):
        f = open(file_path, "w")
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
