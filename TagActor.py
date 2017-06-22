import pykka, logging, json

TAGS_FILE = 'data/tags.json'

class TagActor(pykka.ThreadingActor):
    def __init__(self, stateActor):
        super(TagActor, self).__init__()

        self.stateActor = stateActor

    def playByTag(self, tag, fromStart=False):
        try:
            tags = self.loadTags()
            self.stateActor.playFromLastState(tags[tag], fromStart)
        except KeyError:
            logging.getLogger('zbap').error('No such tag %s' % tag)

    def addTag(self, name):
        tag = self.getTagActor().getTag().get()
        if tag != None:
            tags = self.loadTags()
            tags[tag] = name
            self.saveTags(tags)

    def removeTag(self, tag):
        tags = self.loadTags()
        del tags[tag]
        self.saveTags(tags)

    def getTagActor(self):
        return pykka.ActorRegistry.get_by_class_name("NfcActor")[0].proxy()

    def loadTags(self):
        try:
            with open(TAGS_FILE, 'r') as tagsFile:
                return json.load(tagsFile)
        except (IOError, ValueError) as e:
            logging.getLogger('zbap').error('Unable to load tag file %s' % TAGS_FILE)
            logging.getLogger('zbap').exception(e)
            return {}

    def saveTags(self, state):
        with open(TAGS_FILE, 'w') as tagsFile:
            json.dump(state, tagsFile)
