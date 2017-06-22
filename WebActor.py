from subprocess import Popen, PIPE
import pykka, logging, os, re
from bottle import Bottle, view, redirect

tagActor = None

FILE_DIR = '/var/lib/mpd/music/'

app = Bottle()

@app.route('/')
@view('index')
def index():
    total, free = getDiskInfo()
    return dict(items=items(), totalMem=total, freeMem=free)

@app.route('/add/<name>')
def add(name):
    tagActor.addTag(name).get()
    redirect('/')

@app.route('/remove/<tag>')
def remove(tag):
    tagActor.removeTag(tag).get()
    redirect('/')

@app.route('/play/<tag>')
def play(tag):
    tagActor.playByTag(tag)
    return 'Called tagActor with tag: %s\n' % tag

@app.route('/play/<tag>/fromStart')
def play_from_start(tag):
    tagActor.playByTag(tag, fromStart=True)
    return 'Called tagActor with tag: %s and fromStart=True\n' % tag

def getDiskInfo():
    p = Popen("df -h .", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    m = re.match("([0-9KMGTP\.]+)[\s]+[0-9KMGTP\.]+[\s]+([0-9KMGTP\.]+)", out.decode("utf-8"))
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


    return filesTagArray

def runInThread(function):
    from threading import Thread
    t = Thread(target=function)
    t.setDaemon(True)
    t.start()

def runWebApp():
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception:
        logging.getLogger('zbap').info('Shutting down web server.')

class WebActor(pykka.ThreadingActor):
    def __init__(self, tagAct):
        super(WebActor, self).__init__()

        global tagActor
        tagActor = tagAct

        runInThread(runWebApp)
