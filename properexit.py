import signal

def quithandler(stack, frame):
    raise SystemExit

signal.signal(signal.SIGINT, quithandler)
signal.signal(signal.SIGTERM, quithandler)
signal.signal(signal.SIGQUIT, quithandler)