import os
from inputimeout import inputimeout, TimeoutOccurred


if __name__ == '__main__':
    print('==> Warning <==')

    try:
        inputimeout(prompt='> ', timeout=10)
    except TimeoutOccurred:
        os.system('git pull origin master')
    else:
        while True:
            if (msg := input('> ')) != 'exit':
                os.system(msg)
            else:
                break

    from bot import start_bot
    start_bot()
