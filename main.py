import urwid
import audio

player = audio.Player()


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
    nm = urwid.Filler(numb)
    label = urwid.Text("",align="center")
    label.set_text(sng)

    lb  = urwid.Filler(label)

    pr = urwid.Button("<<",on_press=pervious,user_data=(label,numb))
    pr.button_left = ""
    pr.button_right = ""

    pp = urwid.Button("||",on_press=plpa)
    pr.button_left = ""
    pr.button_right = ""

    nex = urwid.Button(">>",on_press=next,user_data=(label,numb))
    pr.button_left = ""
    pr.button_right = ""

    btn = [pr,pp,nex]

    buttons = urwid.Filler(urwid.Columns(btn),valign="bottom")

    pille = urwid.Pile([nm,lb, buttons,urwid.Filler(urwid.Button(u"~",on_press=shuffle,user_data=(label,numb)))])
    win = urwid.LineBox(pille,title="Just Player")

    ml = urwid.MainLoop(win, unhandled_input=quit_)
    ml.run()



if __name__ == "__main__":
    from sys import argv
    main(argv[1:])