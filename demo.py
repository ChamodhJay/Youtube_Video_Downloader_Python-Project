import tkinter
import customtkinter
from pytube import YouTube

# system setting
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# our app frame

app = customtkinter.CTk()
app.geometry("720x500")
app.title("Youtube Downloader")

# Run app
app.mainloop()
