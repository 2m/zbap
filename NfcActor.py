from subprocess import Popen, PIPE
import re, logging

from TickActor import TickActor

LONG_PRESS_IN_SECONDS = 5

class NfcActor(TickActor):
    def __init__(self, tagActor, sleepSeconds):
        super(NfcActor, self).__init__(sleepSeconds)

        self.tagActor = tagActor

        self.currentTag = None

    def doTick(self):
        tag = self.getTag()
        if tag != self.currentTag:
            self.currentTag = tag
            if tag != None:
                self.doAction(tag)

    def doAction(self, tag):
        logging.getLogger('zbap').info('Calling tagActor.playByTag() with tag: %s' % tag)
        self.tagActor.playByTag(tag)

    def getCurrentTag(self):
        return self.currentTag

    def getTag(self):
        p = Popen("nfc-list", shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        for line in out.decode("utf-8").split("\n"):
            m = re.match(r"[\s]*UID \(NFCID1\): ([a-z0-9 ]+)\b", line)
            if m:
                return m.group(1).replace(" ", "")

        return None
