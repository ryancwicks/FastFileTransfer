from signal import signal, SIGINT
from sys import exit


def cleanup_handler(cleanup_function):
    """
    Generates a cleanup function
    """

    def handler(signal_received, frame):
        """
        Handle any cleanup here.
        """
        print("SIGINT or CTRL-C detected. Exiting...")
        cleanup_function()
        exit(0)

    return handler


def catch_interrupts(cleanup_function):
    signal(SIGINT, cleanup_handler(cleanup_function))
