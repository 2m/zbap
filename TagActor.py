import pykka, logging
from pygame import mixer

import data.tags as tags

class TagActor(pykka.ThreadingActor):
    def __init__(self, stateActor):
        super(TagActor, self).__init__()

        self.stateActor = stateActor

        mixer.init()
        self.ack = mixer.Sound('data/ack.wav')
        self.ack.set_volume(1.0)

    def playByTag(self, tag, fromStart=False):
        try:
            self.ack.play()
            self.stateActor.playFromLastState(tags.tags[tag], fromStart)
        except KeyError:
            logging.getLogger('zbap').error('No such tag %s' % tag)
