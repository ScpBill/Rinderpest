import os
from inputimeout import inputimeout, TimeoutOccurred

TIMEOUT = 3


def main():
    from bot.main import start_bot
    start_bot()


if __name__ == '__main__':
    print('[!!] Type any char or the console to close after {} sec.'.format(TIMEOUT))

    try:
        inputimeout(prompt='... ', timeout=TIMEOUT)
        print('[>_] The console is open (write "exit" to close):')
    except TimeoutOccurred:
        os.system('git reset --hard')
        os.system('git pull origin master')
    else:
        while (msg := input('> ')) != 'exit':
            os.system(msg)

    print('[==] The console is close, starting bot...')
    main()
