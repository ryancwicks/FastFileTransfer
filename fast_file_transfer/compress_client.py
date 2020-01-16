import socket
import zstandard as zstd
import concurrent.futures
from fast_file_transfer.decompress_server import NUM_CLIENTS
import datetime
import sys
from fast_file_transfer.interrupt import catch_interrupts

COMPRESSION_LEVEL = 1


class CompressClient():
    """
    Client program that sends compressed images over tcp to a DecompressServer
    """

    def __init__(self, files, server_ip, port):
        self._files = files
        self._server = server_ip
        self._port = port
        self._send_files = 0

    def handle_transfer(self, filename):
        """
        Given a filename, connect to a remote server port, get a connection, send a file name, wait for the server to send an OK.
        Then load a file and send it compressed over the network.
        """
        sock = socket.socket()

        sock.connect((self._server, self._port))

        sock.send(filename.encode("utf-8"))

        return_value = sock.recv(1024)

        if not return_value:
            raise RuntimeError(
                "Failed to send " + filename + " because socket did not accept the filename.")

        compressor = zstd.ZstdCompressor(level=COMPRESSION_LEVEL)
        with open(filename, "rb") as fid, sock.makefile('wb') as sock_file:
            compressor.copy_stream(fid, sock_file)

        sock.close()

        return filename

    def start_transfer(self):
        """
        Take every file and connect to a server to send data.
        """
        start_time = datetime.datetime.now()
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_CLIENTS) as executor:
            future_connections = {executor.submit(
                self.handle_transfer, filename): filename for filename in self._files}

            def shutdown_connections():
                raise RuntimeError("User signalled shutdown.")

            catch_interrupts(shutdown_connections)
            for future in concurrent.futures.as_completed(future_connections):
                try:
                    send_file = future.result()
                    self._send_files += 1
                    if self._send_files % 10 == 0:
                        sys.stdout.write(
                            "Download progress: " + str((self._send_files+1) / len(self._files) * 100) + "% Sent: " + send_file + "  \r")
                        sys.stdout.flush()
                except Exception as e:
                    print(e)
        print("")
        print("Transfer Finished in " + str(datetime.datetime.now() - start_time))


def main():
    import argparse
    import glob
    from pathlib import Path

    parser = argparse.ArgumentParser(
        "Client that takes an input directory, ip address and port, and sends all the files in that directory to a decompress server.")
    parser.add_argument("directory", type=str,
                        help="path to directory to copy.")
    parser.add_argument("ip_address", type=str, help="ip address of server")
    parser.add_argument("--port", type=int, default=7777,
                        help="port to connect to.")

    args = parser.parse_args()

    files = glob.glob(str(Path(args.directory) / "**/*"),  recursive=True)

    client = CompressClient(files, args.ip_address, args.port)

    client.start_transfer()
