
def main():
    print('hello')
    name= input('Your name: ')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')

