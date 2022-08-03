from tkinter import *
from tkinter import filedialog as fd
from mutagen.mp3 import MP3
import time
import pygame as pg  # pygame renamed as pg
root = Tk()
root.title(" new mp3 player")
root.geometry("1000x400")

paused = False  # variable to check if song is paused
# shows the list of songs added
songs_list = Listbox(root, bg='black', fg='yellow', width=90, selectbackground='gray', selectforeground='yellow', font=20)
songs_list.pack(pady=20)


def pause():  # linked to pause button
    pg.mixer.music.pause()
    global paused
    paused = True
    root_label.config(text='pausing song')


def play():  # linked to play button. acts as play and unpause
    global paused
    if not paused:
        pg.mixer.init()
        now = songs_list.get(ACTIVE)
        now = 'c:/Users/Aditya/Desktop/songsmp/' + now
        pg.mixer.music.load(now)
        pg.mixer.music.play(1)
        song_length()

    else:
        pg.mixer.music.unpause()
        paused = False
        root_label.config(text='unpausing song')
        song_length()


def stop():  # linked to stop button
    root_label.config(text='stop song')
    pg.mixer.music.stop()
    songs_list.selection_clear(ACTIVE)
    status.config(text='')


def next_song():  # linked to next song button
    global paused
    nsong = songs_list.curselection()
    nsong = nsong[0] + 1
    songs_list.selection_clear(0, END)
    songs_list.activate(nsong)
    songs_list.selection_set(nsong, last=None)
    paused = False
    play()


def previous():  # linked to previous song button
    global paused
    psong = songs_list.curselection()
    psong = psong[0] - 1
    songs_list.selection_clear(0, END)
    songs_list.activate(psong)
    songs_list.selection_set(psong, last=None)
    paused = False
    play()
    root_label.config(text='previous song')


def song_length():  # function to get current position of song
    current_pos = pg.mixer.music.get_pos()//1000
    position = time.strftime('%M:%S', time.gmtime(current_pos))
    status.after(1000, song_length)
    csong = songs_list.curselection()
    song = songs_list.get(csong)
    song = 'songsmp/' + song
    temp = MP3(song)
    length = temp.info.length
    total = time.strftime('%M:%S', time.gmtime(length))
    status.config(text=position+' / '+total)


def add_songs():  # linked to add songs menu
    songs = fd.askopenfilenames(initialdir='songsmp/', title='add songs', filetypes=(('mp3 files', '*.mp3'), ))
    for i in songs:
        song = i[32:]
        songs_list.insert(END, song)
        root_label.config(text=songs_list.get(END))


def remove_song():  # linked to remove song menu
    songs_list.delete(ANCHOR)
    stop()


buttons_frame = Frame(root)
buttons_frame.pack()
# button images
play_img = PhotoImage(file='imagesmp/play.png')
pause_img = PhotoImage(file='imagesmp/pause.png')
stop_img = PhotoImage(file='imagesmp/stop.png')
next_img = PhotoImage(file='imagesmp/next.png')
previous_img = PhotoImage(file='imagesmp/previous.png')

# creating buttons
play_but = Button(buttons_frame, image=play_img, command=play, borderwidth=0)
pause_but = Button(buttons_frame, image=pause_img, command=pause, borderwidth=0)
stop_but = Button(buttons_frame, image=stop_img, command=stop, borderwidth=0)
next_but = Button(buttons_frame, image=next_img, command=next_song, borderwidth=0)
previous_but = Button(buttons_frame, image=previous_img, command=previous, borderwidth=0)

# buttons placing
play_but.grid(row=0, column=2, padx=20)
pause_but.grid(row=0, column=3, padx=20)
stop_but.grid(row=0, column=1, padx=20)
next_but.grid(row=0, column=4, padx=20)
previous_but.grid(row=0, column=0, padx=20)

# creating add and remove menu
song_menu = Menu(root)
root.config(menu=song_menu)
song_menu.add_command(label='add songs', command=add_songs)
song_menu.add_command(label='remove song', command=remove_song)

status = Label(root, text='', anchor=E, bd=1)
status.pack(fill=X, ipady=2, side=BOTTOM)
# root label to show what is currently happening
root_label = Label(root, text='')
root_label.pack(pady=20)
mainloop()
