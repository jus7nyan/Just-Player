import audio_metadata
import pygame
from random import randint
import time
import os

pygame.init()

class Player:
    def __init__(self) -> None:
        self.mixer = pygame.mixer.music
        self.playlists= {}
        self.now = {"playing": False, "playlist": None, "index": 0}
        
    
    def get_info(self):
        playing = self.mixer.get_busy
        playlist = self.now["playlist"]
        index = self.now["index"]
        lst = self.playlists[playlist]

        return (playing, index, playlist, lst)

    def playlist_gen(self, path, name=None):
        if path[-1] != "/":
            path += '/'
        lst = os.listdir(os.path.abspath(path))
        lst_t = []
        lst_m = []
        lst_p = []
        for i in range(len(lst)):
            if os.path.splitext(lst[i])[1] in (".mp3",".wav"):
                lst_t.append(lst[i])
                lst_m.append(audio_metadata.load(path+lst[i]))
                lst_p.append(path+lst[i])
        
        if not name:
            name = str(int(list(self.playlists.keys())[-1])+1)

        self.playlists.update({f"{name}":{"list":lst_t, "metadata":lst_m, "path":lst_p}})
    
    def play_pause(self):
        if self.now["playing"]:
            self.mixer.pause()
            self.now["playing"] = False

        elif not self.now["playing"]:
            self.mixer.unpause()
            self.now["playing"] = True
            if not self.mixer.get_busy():
                self.mixer.play()
    
    def start_playing(self, playlist, idx = 0, start=False, shuffle=False):
        try:
            lst = self.playlists[playlist]
        except:
            lst = self.playlists[list(self.playlists.keys())[0]]
        
        name = lst["list"][idx]
        path = lst["metadata"][idx].filepath
        dur = lst["metadata"][idx].streaminfo.duration
        self.mixer.load(path)
        if start:
            self.mixer.play()
            self.now["playing"] = True
            self.mixer.pause()
            self.mixer.unpause()
        else:
            self.now["playing"] = False
        self.now["playlist"] = playlist
        self.now["index"] = idx

        if shuffle:
            self.shuffle()
            self.mixer.play()

        return (name, path, dur)
    
    def get_playlist(self, playlist):
        return self.playlists[playlist]
    
    def shuffle(self):
        p_name = self.now["playlist"]
        lst = self.playlists[p_name]["list"]
        mdata = self.playlists[p_name]["metadata"]
        pathl = self.playlists[p_name]["path"]

        for i in range(len(lst)):
            rn = randint(0,len(lst)-1)
            l1,m1,p1 = lst[i], mdata[i], pathl[i]
            l2,m2,p2 = lst[rn], mdata[rn], pathl[rn]
            lst[rn],mdata[rn],pathl[rn] = l1,m1,p1
            lst[i],mdata[i],pathl[i] = l2,m2,p2

        self.playlists[p_name]["list"] = lst
        self.playlists[p_name]["metadata"] = mdata
        self.playlists[p_name]["path"] = pathl
        self.now["playing"] = True
        self.now["index"] = 0
        self.mixer.load(pathl[0])
        self.mixer.play()
    
    def next(self):
        idx = self.now["index"]
        pl = self.now["playlist"]
        try:
            pathn = self.playlists[pl]["path"][idx+1]
            idx += 1
        except:
            pathn = self.playlists[pl]["path"][0]
            idx = 0
        self.mixer.pause()
        self.mixer.load(pathn)
        self.now["playing"] = True
        self.mixer.play()
        self.mixer.pause()
        self.mixer.unpause()
        self.now["index"] = idx


    def pervious(self):
        idx = self.now["index"]
        pl = self.now["playlist"]
        lst = self.playlists[pl]["path"]
        if idx == 0:
            idx = len(lst)-1
        else:
            idx -= 1
        pathn = lst[idx]
        self.mixer.pause()
        self.mixer.load(pathn)
        self.now["playing"] = True
        self.mixer.play()
        self.mixer.pause()
        self.mixer.unpause()
        self.now["index"] = idx

        

if __name__ == "__main__":
    from sys import argv
    p = Player()
    p.playlist_gen(argv[1:][0], "pl1")
    song = p.start_playing("pl1",13,True)


    while True:
        a = input()
        if ("nex") in a:
            p.next()
        elif ("pre") in a:
            p.pervious()
        elif ("sh") in a:
            p.shuffle()
        elif ("p") in a:
            p.play_pause()