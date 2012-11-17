import os
import subprocess
import sys
import web

urls = (
    '/images/current.png'   , 'currentPNG',
    '/.*'                   , 'index',
)

render = web.template.render('templates/')

commands = {
        'prev'      : 'DOWN',
        'next'      : 'UP',
        'less'      : 'LEFT',
        'more'      : 'RIGHT',
        'mute'      : 'TOGGLE_MUTE',
        'fullscreen': 'TOGGLE_FULLSCREEN',
        'quit'      : 'QUIT',
        '0'         : 'CHANNEL_0',
        '1'         : 'CHANNEL_1',
        '2'         : 'CHANNEL_2',
        '3'         : 'CHANNEL_3',
        '4'         : 'CHANNEL_4',
        '5'         : 'CHANNEL_5',
        '6'         : 'CHANNEL_6',
        '7'         : 'CHANNEL_7',
        '8'         : 'CHANNEL_8',
        '9'         : 'CHANNEL_9',
        'screenshot': 'SCREENSHOT',
        }

path = "/home/janus/Projects/python/webapp/images/current.png"

def setup_xmltv_environ():
    os.environ.pop('LC_ALL', None)
    os.environ['LC_MESSAGES'] = 'C'

def run_xmltv_command(cmd, arg=None):
    """
    Returns without value if command succesfully sent, and returns error string otherwise.
    """
    cmdline = []
    for add in cmd.split(" "):
        cmdline.append(add)
    cmdline.insert(0, 'tvtime-command')
    if arg:
        cmdline.append(arg)

    try:
        p = subprocess.Popen(cmdline, stdin=None, stdout=None, stderr=subprocess.PIPE)
        (stdout, stderr) = p.communicate()

        # Everything is ok
        if p.returncode == 0:
            return
        # Error occured, reason is in last line of stderr
        return stderr.rstrip('\n').split('\n')[-1]
    except OSError, e:
        # Error occured, return the error to caller
        return str(e)

def check_xmltv():
    return run_xmltv_command('SCREENSHOT', path)

def numToChannelId(num):
    output = ""
    for i in range(0, len(num)):
        if i != " ":
            try:
                output += "%s " % commands[num[i]]
            except:
                output += ""
    if len(num) > 1:
        return "%sENTER" % output
    else:
        return "%s" % output


class index:
    def GET(self):
        name = check_xmltv()
        return render.index(name)

    def POST(self):
        iPost = web.input()
        action = iPost.keys()[0]
        if action in commands:
            if action == "screenshot":
                name = run_xmltv_command(commands[action], path)
            else:
                name = run_xmltv_command(commands[action])
        else:
            name = run_xmltv_command(numToChannelId(action))
        return render.index(name)

class currentPNG:
    def GET(self):
        path = "/home/janus/Projects/python/webapp/images/current.png"

        if not os.path.exists(path):
            raise web.NotFound()

        with open(path) as f:
            content = f.read()

        web.header("Content-Type", "image/png")
        return content

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
