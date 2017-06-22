import pykka

class TickActor(pykka.ThreadingActor):
    def __init__(self, sleepSeconds):
        super(TickActor, self).__init__()

        self.sleepSeconds = sleepSeconds
        self.intervalSeconds = 2
        self.intervalCounter = 0

    def tick(self):
        self.intervalCounter += 1
        if self.intervalSeconds / self.sleepSeconds <= self.intervalCounter:
            try:
                self.doTick()
            finally:
                self.intervalCounter = 0

    def doTick(self):
        pass
