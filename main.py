from re import A
import urwid
import audio
import os

player = audio.Player()

class FButton(urwid.Button):
    def __init__(self, label, on_press=None, user_data=None):
        self.button_left, self.button_right = urwid.Text(""),urwid.Text("")
        super().__init__(label, on_press, user_data)



def quit_(key):
    if key in ("q","Q","й","Й"):
        raise urwid.ExitMainLoop()

def pervious(arg,args1):
    player.pervious()
    pl = player.now["playlist"]
    idx = player.now["index"]
    sng = player.playlists[pl]["list"][idx]

    
    args1[0].set_text(sng)
    args1[1].set_text(str(idx+1))

def plpa(arg):
    player.play_pause()

def next(arg,args1):
    player.next()
    pl = player.now["playlist"]
    idx = player.now["index"]
    sng = player.playlists[pl]["list"][idx]

    args1[0].set_text(sng)
    args1[1].set_text(str(idx+1))
def shuffle(arg,args1):
    player.shuffle()
    pl = player.now["playlist"]
    idx = player.now["index"]
    sng = player.playlists[pl]["list"][idx]

    
    args1[0].set_text(sng)
    args1[1].set_text(str(idx+1))

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


    c,r = urwid.raw_display.Screen().get_cols_rows()

    lb  = urwid.Filler(label)
    
    pr = FButton("",on_press=pervious,user_data=(label,numb))
    pr = urwid.LineBox(pr,title="<<")

    pp = FButton("",on_press=plpa)
    pp = urwid.LineBox(pp,title="||")

    nex = FButton("",on_press=next,user_data=(label,numb))
    nex = urwid.LineBox(nex,title=">>")

    shuf = FButton("",on_press=shuffle,user_data=(label,numb))
    shuf = urwid.LineBox(shuf, title="~")
    shuf = urwid.Filler(shuf)
    


    btn = [pr,pp,nex]

    buttons = urwid.Columns(btn)
    buttons = urwid.Filler(buttons)
    pille = urwid.Pile([nm,lb, buttons, shuf])
    win = urwid.LineBox(pille,title="Just Player")

    ml = urwid.MainLoop(win, unhandled_input=quit_)
    ml.run()



if __name__ == "__main__":
    from sys import argv
    main(argv[1:])
