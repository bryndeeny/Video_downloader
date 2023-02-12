from os import path
from tkinter import *
from tkinter import filedialog
import youtube_dl
import shutil
import threading
from tkinter import ttk
import time

def animate_button(button):
    # Change the button's background color to light blue
    button.config(bg='lightblue')
    # Pause for 0.1 seconds to create a "flash" effect
    time.sleep(0.1)
    # Change the button's background color back to the original color
    button.config(bg='SystemButtonFace')

def select_path():
    animate_button(select_btn)
    #allows user to select a path from explorer
    path = filedialog.askdirectory()
    path_label.config(text=path)

def download_file():
    animate_button(select_btn)
    #get user path
    get_link = link_field.get()
    #get selected path
    user_path = path_label.cget("text")
    screen.title('Downloading...')
    ydl_opts = {
        'outtmpl': f'{user_path}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_bar]
    }
    def download():
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([get_link])
            download_message_label.config(text="Download Completed!")
            screen.title('Download Completed. Download another video?...')
        except:
            screen.title("Invalid URL or Video not found")
    thread = threading.Thread(target=download)
    thread.start()

def progress_bar(d):
    if d['status'] == 'downloading':
        file_size = float(d.get('total_bytes', 0))
        if file_size > 0:
            fraction = d['downloaded_bytes'] / file_size
            progress_bar_widget.config(value=int(fraction * 100))
            download_message_label.config(text="{:.0%} of {:.2f} MB".format(fraction, file_size / (1024*1024)))


def clear_text():
    animate_button(select_btn)
    link_field.delete(0, END)
    download_message_label.config(text="")


# GUI code ...

screen = Tk()
screen.geometry('500x500')
screen.title('Video Downloader')
canvas = Canvas(screen, width=500, height=500, bg='#333333')
canvas.pack()

#image logo
logo_img = PhotoImage(file='3ec1.png')
#rezise
logo_img = logo_img.subsample(4, 4)
canvas.create_image(250, 50, image=logo_img)

#link
link_field = Entry(screen, width=40, font=('Arial', 12))
link_label = Label(screen, text="Enter download link: ", font=('Arial', 18), bg='#333333', fg='#f0f0f0')

#select path for saving vids
path_label = Label(screen, text="Select file path: ", font=('Arial', 18), bg='#333333', fg='#f0f0f0')
select_btn = Button(screen, text="Select here", font=('Arial', 15), bg='#f0f0f0', fg='#333333', relief=SUNKEN, command=select_path)

#add to window
canvas.create_window(250, 250, window=path_label)
canvas.create_window(250, 300, window=select_btn)

#add widgets to window
canvas.create_window(250, 150, window=link_label)
canvas.create_window(250, 200, window=link_field)

#Download button
download_btn = Button(screen, text="Download", font=('Arial', 15), bg='#f0f0f0', fg='#333333', relief=SUNKEN, command=download_file)
canvas.create_window(250, 400, window=download_btn)

#download message
download_message_label = Label(screen, text="", font=('Arial', 18), bg='#333333', fg='#f0f0f0')
canvas.create_window(250, 450, window=download_message_label)

#clear button
clear_btn = Button(screen, text="Clear", font=('Arial', 15), bg='#f0f0f0', fg='#333333', relief=SUNKEN, command=clear_text)
canvas.create_window(400, 400, window=clear_btn)

# Add the progress bar widget to your GUI
progress_bar_widget = ttk.Progressbar(screen, orient='horizontal', length=200, mode='determinate')
progress_bar_widget.pack()

#run GUI
screen.mainloop()
