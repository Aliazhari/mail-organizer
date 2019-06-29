from controller.controllers import *


def main():
    passcode = get_passcode()
    print(passcode)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')
