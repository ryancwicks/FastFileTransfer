from fast_file_transfer import DecompressServer, CompressClient
import time
import threading
import glob
import shutil
from pathlib import Path


def test_compress_client_server():

    # set up test directory
    input_file_dir = Path("./input_files/")
    input_file_dir.mkdir(exist_ok=True)
    output_file_dir = Path("./output_files/")
    output_file_dir.mkdir(exist_ok=True)

    test_img_src = "tests/img_orig.tif"

    for i in range(10):
        output_file = input_file_dir / Path(str(i) + ".tif")
        shutil.copy(test_img_src, str(output_file))

    # Start decompress server in a background thread
    server = DecompressServer(7777, str(output_file_dir))
    server_thread = threading.Thread(target=server.start_listening)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(0.00001)

    files = glob.glob(str(input_file_dir / "*"))
    send_client = CompressClient(files, "127.0.0.1", 7777)
    send_client.start_transfer()

    input_count = len(glob.glob(str(input_file_dir / "*")))
    output_count = len(glob.glob(str(output_file_dir / input_file_dir / "*")))

    assert (input_count == output_count)

    shutil.rmtree(str(input_file_dir))
    shutil.rmtree(str(output_file_dir))

    # Make sure server thread finishes
    while (True):
        try:
            server_thread.join(1)
        except KeyboardInterrupt:
            print("exiting...")
            break


if __name__ == "__main__":
    test_compress_client_server()
