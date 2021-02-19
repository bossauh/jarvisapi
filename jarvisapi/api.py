from difflib import SequenceMatcher

import nltk
import requests
import socket
import random
import json
import threading

class ServerRequired(Exception):
    pass

class JarvisError(Exception):
    def __init__(self, error, message):
        pass

def how_similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class Websocket:
    def __init__(self, host, port, pymitter, server=False, client_list=[], logger=None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server

        if server:
            self.s.bind((host, port))
            self.s.listen(5)
            self.client_list = client_list
        else:
            self.s.connect((host, int(port)))
        
        self.logger_instance = logger
        self.event = pymitter
    
    def log(self, text, level):
        if self.logger_instance:
            self.logger_instance.log(text, level)
    
    def _listen_in_background(self):
        while True:
            try:
                if self.server:
                    self.log("Waiting for incoming connections", 0)
                    client, address = self.s.accept()
                    self.log(f"Connection from {address} established!", 0)
                    
                    if client not in self.client_list:
                        self.client_list.append(client)

                else:
                    client = self.s
                    self.log("Waiting to receive some data", 0)

                    data = client.recv(1048576)
                    data = json.loads(data.decode("utf-8"))

                    self.log(f"Websocket has received {data}", 0)
                    self.log("Now emitting to websocket_receive", 0)
                    self.event.emit("ws_" + data['type'], data)
                    self.log("Data has been successfully emitted to websocket_receive", 0)
            except KeyboardInterrupt:
                break

    def listen_in_background(self):
        self.log("Starting websocket listener", 0)
        threading.Thread(target=self._listen_in_background, daemon=True).start()
        self.log("Started websocket listener", 0)
    
    def send(self, data, _type=None, client=None):
        data = {"type": _type, "data": data}
        data_encoded = json.dumps(data).encode('utf-8')

        if client is None:
            client = self.s

        self.log(f"SENDING: {data} to client", 0)
        client.sendall(data_encoded)
        self.log(f"SENT: {data} to client", 0)
    
    def send_to_all(self, data, _type=None):
        if not self.server:
            self.log("send_to_all requires you to be a server", 3)
            raise ServerRequired("This function only works for servers")
        
        for client in self.client_list:
            self.send(data, _type=_type, client=client)
    
class API:
    # TODO Add some sort of security layer so that no random fuck could just make jarvis say random shit. Basically just make jarvis secure because it is so goddamn insecure

    def __init__(self, host, port, logger=None, name=None):
        self.host = host
        self.port = int(port)
        self.logger = logger
        self.name = name
        self.base = f"http://{host}:{port}/api/"
    
    def _log(self, text, level=0):
        if self.logger:
            self.logger.log(text, level)
    
    def speak(self, content):
        
        if type(content) is list:
            content = random.choice(content)

        url = self.base + "speak"
        data = {
            "content": content,
            "from": self.name
        }

        self._log(f"POSTING: to {url} with {data}", 0)
        requests.post(url, json=data)
        self._log(f"POSTED: to {url} with {data}", 0)
    
    def send_data(self, type, data):
        url = self.base + "send_data"
        data = {
            "data": data,
            "type": type,
            "from": self.name
        }

        self._log(f"POSTING: to {url} with {data}", 0)
        requests.post(url, json=data)
        self._log(f"POSTED: to {url} with {data}", 0)

    def get_tags(self, text, tags):
        self._log(f"Retrieving tags {tags} from the text {text}", 0)
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)

        meet_tags = [word for word, tag in tagged if tag in tags]

        self._log(f"Successfully retrieved {meet_tags}", 0)
        return meet_tags
    
    def log(self, text, level=0):
        url = self.base + "log"
        data = {
            "content": str(text),
            "level": level,
            "from": self.name
        }

        self._log(f"POSTING: to {url} with {data}", 0)
        requests.post(url, json=data)
        self._log(f"POSTED: to {url} with {data}", 0)
    

