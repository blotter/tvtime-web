import os
import subprocess
import sys
import web

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
    return run_xmltv_command('SCREENSHOT', '/home/janus/Projects/python/webapp/images/current.png')

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
        'zero'      : 'CHANNEL_0',
        'one'       : 'CHANNEL_1',
        'two'       : 'CHANNEL_2',
        'three'     : 'CHANNEL_3',
        'four'      : 'CHANNEL_4',
        'five'      : 'CHANNEL_5',
        'six'       : 'CHANNEL_6',
        'seven'     : 'CHANNEL_7',
        'eight'     : 'CHANNEL_8',
        'nine'      : 'CHANNEL_9',
        'ard'       : 'CHANNEL_5 ENTER',
        'zdf'       : 'CHANNEL_6 ENTER',
        'rbb'       : 'CHANNEL_7 ENTER',
        'vox'       : 'CHANNEL_8 ENTER',
        'kika'      : 'CHANNEL_9 ENTER',
        'ntv'       : 'CHANNEL_1 CHANNEL_0 ENTER',
        'n24'       : 'CHANNEL_1 CHANNEL_1 ENTER',
        'mdr'       : 'CHANNEL_1 CHANNEL_2 ENTER',
        'qvc'       : 'CHANNEL_1 CHANNEL_8 ENTER',
        'rtl'       : 'CHANNEL_1 CHANNEL_9 ENTER',
        'sat'       : 'CHANNEL_2 CHANNEL_0 ENTER',
        'ltv'       : 'CHANNEL_2 CHANNEL_1 ENTER',
        'sport'     : 'CHANNEL_2 CHANNEL_2 ENTER',
        'pro7'      : 'CHANNEL_2 CHANNEL_3 ENTER',
        'rtl2'      : 'CHANNEL_2 CHANNEL_4 ENTER',
        'kabel1'    : 'CHANNEL_2 CHANNEL_5 ENTER',
        'super'     : 'CHANNEL_2 CHANNEL_6 ENTER',
        'br'        : 'CHANNEL_2 CHANNEL_7 ENTER',
        '3sat'      : 'CHANNEL_2 CHANNEL_8 ENTER',
        'tele5'     : 'CHANNEL_2 CHANNEL_9 ENTER',
        'ndr'       : 'CHANNEL_3 CHANNEL_0 ENTER',
        'viva'      : 'CHANNEL_3 CHANNEL_1 ENTER',
        'nick'      : 'CHANNEL_3 CHANNEL_2 ENTER',
        'astro'     : 'CHANNEL_3 CHANNEL_3 ENTER',
        'arte'      : 'CHANNEL_3 CHANNEL_4 ENTER',
        'juwelo'    : 'CHANNEL_3 CHANNEL_5 ENTER',
        'hse24'     : 'CHANNEL_4 CHANNEL_7 ENTER',
        'mdr'       : 'CHANNEL_6 CHANNEL_9 ENTER',
        'eurosport' : 'CHANNEL_9 CHANNEL_2 ENTER',
        'phoenix'   : 'CHANNEL_9 CHANNEL_3 ENTER',
        'dmax'      : 'CHANNEL_9 CHANnel_4 ENTER',
        'screenshot': 'SCREENSHOT /home/janus/Projects/python/webapp/images/current.png',
        }

class index:
    def GET(self):
        name = check_xmltv()
        return render.index(name)

    def POST(self):
        iPost = web.input()
        action = iPost.keys()[0]
        if action in commands:
            if action == "screenshot":
                name = run_xmltv_command(commands[action].split(" ")[0], commands[action].split(" ")[1])
            else:
                name = run_xmltv_command(commands[action])
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
