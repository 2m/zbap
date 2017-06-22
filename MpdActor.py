import pykka, mpd, logging

DEFAULT_VOLUME = 100

class MpdActor(pykka.ThreadingActor):
    def __init__(self):
        super(MpdActor, self).__init__()

        self.client = mpd.MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None
        self.client.connect("localhost", 6600)

    def getCurrentSong(self):
        try:
            name = self.client.currentsong()["file"]
            elapsed = int(float(self.client.status()["elapsed"]))

            return {"name": name, "elapsed": elapsed}
        except KeyError:
            return None

    def playByNameFrom(self, name, playFrom):
        try:
            self.client.setvol(0)

            self.client.clear()
            self.client.add(name)
            self.client.play()

            currentSong = self.client.currentsong()
            if playFrom + 20 > int(currentSong['time']):
                # play from start, if trying to play too close from the end
                playFrom = 0

            logging.getLogger('zbap').info('Playing %s from %s' % (name, playFrom))
            self.client.seekid(currentSong['id'], playFrom)

            self.client.setvol(DEFAULT_VOLUME)

        except mpd.CommandError as e:
            logging.getLogger('zbap').error('MPD Command error')
            logging.getLogger('zbap').exception(e)


    def pause(self):
        self.client.pause()
