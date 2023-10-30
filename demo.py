import tkinter
import customtkinter
from pytube import YouTube


def startDownload():
    try:
        Ytlink = link.get()
        ytObject = YouTube(Ytlink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        video.download()
        finishLabel.configure(text="Downloaded!")
    except:
        finishLabel.configure(text="Download Error!", text_color="red")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_download = total_size-bytes_remaining
    percentage_of_completion = bytes_download/total_size*100
    per = str(int(percentage_of_completion))
    Ppercentage.configure(text=per+"%")
    Ppercentage.update()
# Update Progress Bar
    progressBar.set(float(percentage_of_completion)/100)


# system setting
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# our app frame
app = customtkinter.CTk()
app.geometry("720x500")
app.title("Youtube Downloader")

# adding ui elements

title = customtkinter.CTkLabel(app, text="Enter a Yourube Link here:")
title.pack(padx=10, pady=10)

# link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finish Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress Percentage
Ppercentage = customtkinter.CTkLabel(app, text="0%")
Ppercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Run app
app.mainloop()
