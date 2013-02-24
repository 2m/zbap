import pykka, web 

tagActor = None

urls = (
    '/play/([0-9]*)', 'Play',
    '/play/([0-9]*)/fromStart', 'FromStart'
)

class Play:
    def GET(self, tag):
        tagActor.playByTag(tag)
        return 'Called tagActor with tag: %s\n' % tag

class FromStart:
    def GET(self, tag):
        tagActor.playByTag(tag, fromStart=True)
        return 'Called tagActor with tag: %s and fromStart=True\n' % tag

def runInThread(function):
    from threading import Thread
    t = Thread(target=function)
    t.setDaemon(True)
    t.start()

def runWebApp():
    app = web.application(urls, globals())
    app.run()

class WebActor(pykka.ThreadingActor):
    def __init__(self, tagAct):
        super(WebActor, self).__init__()

        global tagActor
        tagActor = tagAct 

        runInThread(runWebApp)
