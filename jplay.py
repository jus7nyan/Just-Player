#! /bin/python3
from time import sleep
import urwid
import audio
import os

import asyncio

player = audio.Player()
ppl = 0
MLEN = [0,0]

class FButton(urwid.Button):
    def __init__(self, label, on_press=None, user_data=None):
        self.button_left, self.button_right = urwid.Text(""),urwid.Text("")
        super().__init__(label, on_press, user_data)



def quit_(key):
    if key in ("q","Q","й","Й"):
        raise urwid.ExitMainLoop()
    elif key in ("meta right","ctrl right"):
        next()
    elif key in ("meta left", "ctrl left"):
        pervious()
    elif key == "s":
        shuffle()
    elif key == "p":
        plpa()

def pervious(arg=None):
    player.pervious()
    pl = player.now["playlist"]
    idx = player.now["index"]
    sng = player.playlists[pl]["list"][idx]

    
    args1[0].set_text(sng)
    args1[1].set_text(str(idx+1))
    mll.set_title("0:0 / 0:0")

def plpa(arg=None):
    player.play_pause()
    global ppl
    if ppl % 2 == 0:
        pp.set_title("|>")
    else:
        pp.set_title("||")
    ppl += 1

def next(arg=None):
    player.next()
    pl = player.now["playlist"]
    idx = player.now["index"]
    sng = player.playlists[pl]["list"][idx]
    mll.set_title("0:0 / 0:0")

    args1[0].set_text(sng)
    args1[1].set_text(str(idx+1))

def shuffle(arg=None):
    player.shuffle()
    pl = player.now["playlist"]
    idx = player.now["index"]
    sng = player.playlists[pl]["list"][idx]

    
    args1[0].set_text(sng)
    args1[1].set_text(str(idx+1))
    mll.set_title("0:0 / 0:0")


async def mlen():
    global mll
    while True:
        inf = player.get_info()
        ind = inf[1]
        pl = inf[2]
        lst = inf[3]
        dur = lst["metadata"][ind].streaminfo.duration
        # dur = lst.keys()
        l = [player.mixer.get_pos()/1000,dur]
        try:
            sec = l[0] % (24*3600)
            hour = round(sec // 3600)
            sec = sec % 3600
            min = round(sec // 60)
            sec = round(sec % 60)

            sec1 = l[1] % (24*3600)
            hour1 = round(sec1 // 3600)
            sec1 = sec1 % 3600
            min1 = round(sec1 // 60)
            sec1 = round(sec1 % 60)
            
            if (hour == 23) and (min == 59) and (sec == 60):
                next()
                continue

            elif (hour != 0 and min != 0):
                mll.set_title(f"{hour}:{min}:{sec} / {hour1}:{min1}:{sec1}")
            else:
                mll.set_title(f"{min}:{sec} / {min1}:{sec1}")
        except:
            continue
        
        await asyncio.sleep(0.3)

def lyr_now(arg):
    sngs = player.get_lyr()
    try:
        lyrics, art,tit = player.get_text(sngs[0])
        string = f"{art} -- {tit}\n\n{lyrics}"
        with open(f"/tmp/lyr.txt","+w") as file:
            file.write(string)
        os.popen("x-terminal-emulator -e 'less /tmp/lyr.txt'")
    except:
        pass




def main(args):
    player.playlist_gen(path=args[0],name="rnd")
    player.start_playing("rnd",start=True, shuffle=True)

    pl = player.now["playlist"]
    idx = player.now["index"]
    sng = player.playlists[pl]["list"][idx]
    
    numb = urwid.Text(str(idx+1),align="center")
    nm = urwid.LineBox(numb)
    nm = urwid.Filler(nm)
    label = urwid.Text("",align="center")
    label.set_text(sng)

    global args1
    args1 = (label, numb)

    lb  = urwid.Filler(label)
    
    pr = FButton("",on_press=pervious)
    pr = urwid.LineBox(pr,title="<<")
    
    global pp, lyr
    pp = FButton("",on_press=plpa)
    pp = urwid.LineBox(pp,title="||")

    nex = FButton("",on_press=next)
    nex = urwid.LineBox(nex,title=">>")

    lyr = FButton("",on_press=lyr_now)
    lyr = urwid.LineBox(lyr,title="TEXT")
    
    shuf = FButton("",on_press=shuffle)
    shuf = urwid.LineBox(shuf, title="~")
    shuf = urwid.Columns([shuf,lyr])
    shuf = urwid.Filler(shuf)
    


    global mll
    mll = urwid.Text("")
    mll = urwid.LineBox(mll,title="0/0")
    btn = [pr,pp,nex]

    buttons = urwid.Columns(btn)
    buttons = urwid.Filler(buttons)
    pille = urwid.Pile([nm,lb,urwid.Filler(mll), buttons, shuf])
    win = urwid.LineBox(pille,title="Just Player")


    aloop = asyncio.get_event_loop()

    ev_loop = urwid.AsyncioEventLoop(loop=aloop)
    loop = urwid.MainLoop(win,
                      unhandled_input=quit_, event_loop=ev_loop)
    aloop.create_task(mlen())
    loop.run()

   



if __name__ == "__main__":
    from sys import argv
    if argv[1:]:
        main(argv[1:])
    else:
        try:
            main("./")
        except:
            print("please specify the path to the playlist in the launch argument")
