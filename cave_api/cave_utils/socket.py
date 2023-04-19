class Socket:
    def __init__(self):
        pass

    def broadcast(self, *args, **kwargs):
        print("broadcast: ", {"args": args, "kwargs": kwargs})

    def notify(self, *args, **kwargs):
        print("notify: ", {"args": args, "kwargs": kwargs})