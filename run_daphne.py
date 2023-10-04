import sys
import os

if __name__ == '__main__':
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ['DJANGO_SETTINGS_MODULE'] = 'gameproject.settings'

    # Your Daphne command
    sys.argv = ['daphne', '-b', '0.0.0.0', '-p', '8000', 'gameproject.asgi:application']

    from daphne.cli import CommandLineInterface

    CommandLineInterface.entrypoint()

