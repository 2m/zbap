from subprocess import Popen, PIPE
import pykka, web, logging, os, re

tagActor = None

FILE_DIR = '../music/'

urls = (
    '/', 'Index',
    '/add/(.+)', 'AddTag',
    '/remove/(.+)', 'RemoveTag',
    '/play/([a-z0-9]+)', 'Play',
    '/play/([a-z0-9]+)/fromStart', 'FromStart'
)

t_globals = dict(datestr=web.datestr)

render = web.template.render('templates/', cache=False, globals=t_globals)
render._keywords['globals']['render'] = render

class Index:
    def GET(self):
        total, free = getDiskInfo()
        return render.base(items(), total, free)

class AddTag:
    def GET(self, name):
        tagActor.addTag(name).get()
        raise web.seeother('/')

class RemoveTag:
    def GET(self, tag):
        tagActor.removeTag(tag).get()
        raise web.seeother('/')

class Play:
    def GET(self, tag):
        tagActor.playByTag(tag)
        return 'Called tagActor with tag: %s\n' % tag

class FromStart:
    def GET(self, tag):
        tagActor.playByTag(tag, fromStart=True)
        return 'Called tagActor with tag: %s and fromStart=True\n' % tag

def getDiskInfo():
    p = Popen("df -h | grep rootfs", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    m = re.match("rootfs[\s]+([0-9KMGTP\.]+)[\s]+[0-9KMGTP\.]+[\s]+([0-9KMGTP\.]+)", out)
    total = "N/A"
    free = "N/A"
    if m != None:
        total = m.group(1)
        free = m.group(2)
    return total, free

def items(**k):
    currentFiles = sorted(os.listdir(FILE_DIR))
    tags = {name:tag for tag, name in tagActor.loadTags().get().items()}

    filesTagArray = []
    for fileName in currentFiles:
        if fileName in tags:
            filesTagArray.append({"name": fileName, "tag": tags[fileName]})
        else:
            filesTagArray.append({"name": fileName, "tag": None})


    return render.items(filesTagArray)

def runInThread(function):
    from threading import Thread
    t = Thread(target=function)
    t.setDaemon(True)
    t.start()

def runWebApp():
    try:
        app = web.application(urls, globals())
        app.run()
    except Exception:
        logging.getLogger('zbap').info('Shutting down web server.')

class WebActor(pykka.ThreadingActor):
    def __init__(self, tagAct):
        super(WebActor, self).__init__()

        global tagActor
        tagActor = tagAct 

        runInThread(runWebApp)
