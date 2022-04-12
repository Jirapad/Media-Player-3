from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import time
from mutagen.mp3 import MP3


# timeSong
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000

    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))

    song = song_box.get(ACTIVE)
    song = f'C:/SE KMITL/Python/Project/songList/{song}.mp3'
    song_mut = MP3(song)
    song_length = song_mut.info.length
    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))

    status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')

    status_bar.after(1000, play_time)


# addSongF
def add_song():
    songs = filedialog.askopenfilenames(initialdir='songlist/', title="Choose A Song",
                                        filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace("C:/SE KMITL/Python/Project/songList/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)


# play
def play():
    song = song_box.get(ACTIVE)
    song = f'C:/SE KMITL/Python/Project/songList/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    play_time()


# stop
def stop():
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)

    status_bar.config(text='Stop')


# nextSong
def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    song = f'C:/SE KMITL/Python/Project/songList/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


# previous
def previous_song():
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song = f'C:/SE KMITL/Python/Project/songList/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


# delete
def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


# pause
global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


# volume
def volume(x):
    pygame.mixer.music.set_volume(volumelevel.get())


# window
root = Tk()
root.title("MCmp3")
root.iconbitmap("C:/SE KMITL/Python/Project/filephotoshop/icon.ico")
root.minsize(300,275)
root.maxsize(300,275)
root.config(background='black')

# init pygame
pygame.mixer.init()

wall = Frame(root, bg='black')
wall.pack()
# platlistbox
song_box = Listbox(wall, bg="white", fg="black", width=40, height=10, selectbackground="Black",
                   selectforeground="White")
song_box.grid(row=0, column=0, pady=20)

# playerbutton
back_btn_img = PhotoImage(file="C:/SE KMITL/Python/Project/filephotoshop/previous.png")
forward_btn_img = PhotoImage(file="C:/SE KMITL/Python/Project/filephotoshop/next.png")
play_btn_img = PhotoImage(file="C:/SE KMITL/Python/Project/filephotoshop/play.png")
pause_btn_img = PhotoImage(file="C:/SE KMITL/Python/Project/filephotoshop/pause.png")
stop_btn_img = PhotoImage(file="C:/SE KMITL/Python/Project/filephotoshop/stop.png")

controls_frame = Frame(root)
controls_frame.pack()

back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# menu
my_menu = Menu(root)
root.config(menu=my_menu)

# addSong
add_song_menu = Menu(my_menu, tearoff=0, background="gray", foreground='black', activeforeground='gray', activebackground='black')
my_menu.add_cascade(label="Menu", menu=add_song_menu)
add_song_menu.add_command(label="Add songs", command=add_song)
add_song_menu.add_command(label="Remove songs", command=delete_song)

# timeSong
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E, background="gray")
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# volume
volumelevel = ttk.Scale(wall, from_=1, to=0, orient=VERTICAL, value=1, length=164, command=volume)
volumelevel.grid(row=0, column=1, pady=15)

root.mainloop()