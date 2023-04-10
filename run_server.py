#! /usr/bin/env python
"""This Module creates and runs the HTTP server with which our website/client will interact with.
    This server will run on either a default port or a port passed to the module by the user"""
import argparse # handle command-line arguments
import sys
from game import app

def main():
    """Main function of program."""
    connection_info = get_port()
    run_app(connection_info)

def get_port():
    """Gets the number of the port on which the program will listen
        for connections from the command line arguments.
        Utilizes argparse module to read command line arguments
        Returns a dictionary with the port number

        - parser is the parser object that will be used to read the command line arguments
        - args is the namespace object that contains the port number
        """

    parser = argparse.ArgumentParser(description="A timezone search application.",
        allow_abbrev=False)
    parser.add_argument("port",
        help="the port at which the server should listen")
    args = vars(parser.parse_args())
    return args

def run_app(connection_info):
    """Runs an instance of the Flask server on the specified port,
        which in turn runs the application"""
    try:
        port = int(connection_info["port"])
    except ValueError:
        print('Port must be a valid integer.', file = sys.stderr)
        sys.exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except OverflowError as err:
        print("This is an invalid port number.", file = sys.stderr)
        print(err, file = sys.stderr)
        sys.exit(1)
    except OSError as err:
        print("Connection failed. Please try another port", file = sys.stderr)
        print(err, file = sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
