from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import os
import time
import threading
from mutagen.mp3 import MP3
from pygame import mixer

r = Tk()

statusbar = Label(r, text="Welcome to VLC", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(r)
r.config(menu=menubar)

playlist = []

def browser():
   global filename_path
   filename_path = filedialog.askopenfilename()
   add_to_playlist(filename_path)

def add_to_playlist(filename):
   filename = os.path.basename(filename)
   index=0
   playlistbox.insert(index, filename)
   playlist.insert(index, filename_path)
   index+=1

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browser)
subMenu.add_command(label="Exit", command=r.destroy)

def about_us():
   tkinter.messagebox.showinfo('About App', 'This is a music player')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About us", command=about_us)

mixer.init()
r.title("VLC")
r.iconbitmap(r'VLCicon.ico')

leftframe = Frame(r)
leftframe.pack(side=LEFT,padx=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = Button(leftframe, text='+Add',command=browser)
addbtn.pack(side=LEFT)

def delete_song():
   selected_song = playlistbox.curselection()
   selected_song = int(selected_song[0])
   playlistbox.delete(selected_song)
   playlist.pop(selected_song)

delbtn = Button(leftframe, text='-Del', command=delete_song)
delbtn.pack(side=LEFT)

rightframe = Frame(r)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = Label(topframe, text="Total Length : --:--")
lengthlabel.pack(pady=5)

currenttimelabel = Label(topframe, text="Current Time : --:--", relief=GROOVE)
currenttimelabel.pack()

def showed_detail(play_it):
   file_data = os.path.splitext(play_it)

   if file_data[1] == '.mp3':
       audio = MP3(play_it)
       total_length = audio.info.length
   else:
       a = mixer.Sound(play_it)
       total_length = a.get_length()

   mins, secs = divmod(total_length, 60)
   mins = round(mins)
   secs = round(secs)
   timeformat = '{:02d}:{:02d}'.format(mins, secs)
   lengthlabel['text'] = 'Total Length' + ' - ' + timeformat

   t1 = threading.Thread(target=start_count, args=(total_length,))
   t1.start()

def start_count(total_length):
   global paused
   t=0
   while (t<=total_length) and mixer.music.get_busy():
       if paused:
           continue
       else:
           mins, secs = divmod(t, 60)
           mins = round(mins)
           secs = round(secs)
           timeformat = '{:02d}:{:02d}'.format(mins, secs)
           currenttimelabel['text'] = 'Total Length' + ' - ' + timeformat
           time.sleep(1)
           t +=1


def play_music():
   global paused
   if paused:
       mixer.music.unpause()
       statusbar['text']='Music resumed'
       paused=False
   else:
       stop_music()
       time.sleep(1)
       selected_song = playlistbox.curselection()
       selected_song = int(selected_song[0])
       play_it = playlist[selected_song]
       mixer.music.load(play_it)
       mixer.music.play()
       statusbar['text'] = 'Playing music'+' - '+ os.path.basename(play_it)
       showed_detail(play_it)

def stop_music():
   mixer.music.stop()
   statusbar['text']='Music stopped'

paused=False
def pause_music():
   global paused
   paused = True
   mixer.music.pause()
   statusbar['text']='Pause music'

def set_vol(val):
   volume = int(val)/100
   mixer.music.set_volume(volume)

muted=False
def mute_music():
   global muted
   if muted:
       mixer.music.set_volume(0.5)
       scale.set(50)
       volumebtn.configure(image=volumephoto)
       muted=False
   else:
       mixer.music.set_volume(0)
       scale.set(0)
       volumebtn.configure(image=mutephoto)
       muted=True

middleframe = Frame(rightframe)
middleframe.pack(pady=10,padx=10)

playphoto = PhotoImage(file='playimg.png')
playbtn = Button(middleframe, image=playphoto, command=play_music)
playbtn.pack(side=LEFT,padx=10)

stopphoto = PhotoImage(file='stop.png')
stopbtn = Button(middleframe, image=stopphoto, command=stop_music)
stopbtn.pack(side=LEFT,padx=10)

pausephoto = PhotoImage(file='pause.png')
pausebtn = Button(middleframe, image=pausephoto, command=pause_music)
pausebtn.pack(side=LEFT,padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

mutephoto = PhotoImage(file='mute.png')
volumephoto = PhotoImage(file='volume12.png')
volumebtn = Button(bottomframe, image=volumephoto, command=mute_music)
volumebtn.pack(side=LEFT,pady=10,padx=20)

scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)
mixer.music.set_volume(0.5)
scale.pack(side=LEFT,pady=10,padx=20)

def on_closing():
   stop_music()
   r.destroy()

r.protocol("WM_DELETE_WINDOW", on_closing)

r.mainloop()

