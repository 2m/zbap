import pykka, logging

from time import sleep 

from WebActor import WebActor
from MpdActor import MpdActor
from StateActor import StateActor
from TagActor import TagActor

sleepSeconds = 0.5

if __name__ == "__main__":

    logging.basicConfig(filename='zbap.log', format="%(asctime)s [%(module)s.%(funcName)s] %(levelname)s: %(message)s")
    logging.getLogger('pykka').setLevel(logging.DEBUG)
    logging.getLogger('zbap').setLevel(logging.DEBUG)

    mpdActor = MpdActor.start().proxy()
    stateActor = StateActor.start(mpdActor, sleepSeconds).proxy()

    tagActor = TagActor.start(stateActor).proxy()
    webActor = WebActor.start(tagActor).proxy()

    stateActor.playFromLastState()

    try:
        while True:
            stateActor.tick()
            sleep(sleepSeconds)
    except KeyboardInterrupt:
        print "Exiting main loop."

    pykka.ActorRegistry.stop_all()
