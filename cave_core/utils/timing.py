import datetime


class Timer_Object:
    def __init__(self):
        self.objects = {}

    def start(self, name):
        self.objects[name] = datetime.datetime.now()

    def end(self, name):
        now = datetime.datetime.now()
        diff = now - self.objects.pop(name, now)
        print(name, ": ", int(diff.total_seconds() * 1000), "ms")

    def unix_time(self):
        print((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


timer = Timer_Object()
