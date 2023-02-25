import os

TIMEOUT = 3


def main():
    from bot import start_bot
    start_bot()


if __name__ == '__main__':
    print('[!] Type any char or the console to close after {} sec [!]'.format(TIMEOUT))

    print('[>_] The console is open:')
    while (msg := input('> ')) != 'exit':
        os.system(msg)

    print('[=] The console is close, starting bot...')
    main()
