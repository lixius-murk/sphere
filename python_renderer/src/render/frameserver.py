import socket
import threading
import struct
import time
import numpy as np

class FrameServer:
    def __init__(self, port=12345):
        self.port = port
        self.client_connected = threading.Event()  # Use Event for signaling
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('127.0.0.1', port))
        self.server.listen(5)
        self.running = True
        threading.Thread(target=self._accept_clients, daemon=True).start()

    def _accept_clients(self):
        while self.running:
            try:
                client, addr = self.server.accept()
                print(f"Qt client connected from {addr}")
                self.clients.append(client)
                self.client_connected.set()  # Signal that we have a client
            except:
                break

    def send_frame(self, w, h, rgb_bytes):
        # Wait for client to connect
        if not self.client_connected.is_set():
            return  # No client yet, skip frame
            
        MAGIC = 0xDEADBEEF
        header = struct.pack('III', MAGIC, w, h)
        to_remove = []
        for client in self.clients:
            try:
                client.sendall(header + rgb_bytes)
            except:
                to_remove.append(client)
        for client in to_remove:
            self.clients.remove(client)