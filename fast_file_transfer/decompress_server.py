import socket
import zstandard as zstd
import threading
from pathlib import Path
from fast_file_transfer.interrupt import catch_interrupts

NUM_CLIENTS = 8


class DecompressServer ():

    def __init__(self, port, save_directory=None):
        self._port = port
        self._save_directory = "./" if not save_directory else save_directory
        self._save_directory = Path(self._save_directory)
        self._save_directory.mkdir(parents=True, exist_ok=True)

    def handle_client(self, conn):

        filename = conn.recv(1024)
        filename = Path(filename.decode())
        filename = self._save_directory / filename

        filename.parent.mkdir(exist_ok=True, parents=True)

        print(f"Transferring {str(filename)}")
        conn.send("Go".encode("utf-8"))

        decompressor = zstd.ZstdDecompressor()
        with conn.makefile('rb') as sock_fid, open(str(filename), 'wb') as fid:
            decompressor.copy_stream(sock_fid, fid)
        conn.close()
        return

    def start_listening(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        def cleanup_socket():
            sock.close()

        catch_interrupts(cleanup_socket)

        sock.bind(("", self._port))

        sock.listen(NUM_CLIENTS)

        try:
            while (True):
                conn, _ = sock.accept()
                client_handler = threading.Thread(
                    target=self.handle_client, args=(conn,))
                client_handler.start()
        except KeyboardInterrupt:
            pass
        sock.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        "Server that decompresses and saves compressed files sent to it.")
    parser.add_argument("--port", type=int, default=7777,
                        help="port to connect to.")
    parser.add_argument("--directory", type=str, default="./",
                        help="path to directory to copy.")

    args = parser.parse_args()

    server = DecompressServer(args.port, args.directory)

    server.start_listening()
