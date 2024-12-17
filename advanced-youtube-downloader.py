import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import tkinter.font as tkFont


class AdvancedYouTubeDownloader:
    def __init__(self, master):
        """
        Initialize an advanced, modern YouTube Downloader
        """
        self.master = master
        # master.title("UltraDown - YouTube Downloader")
        # master.geometry("800x650")

        # Theme tracking
        self.current_theme = 'dark'

        # Configure themes
        self.themes = {
            'dark': {
                'bg_primary': '#070F2B',
                'bg_secondary': '#16213E',
                'bg_tertiary': '#0F3460',
                'fg_primary': '#ffffff',
                'fg_secondary': '#E94560',
                'entry_bg': '#1B1A55',
                'progress_bg': '#9290C3'
            },
            'light': {
                'bg_primary': '#F7FBFC',
                'bg_secondary': '#ffffff',
                'bg_tertiary': '#769FCD',
                'fg_primary': '#000000',
                'fg_secondary': '#0F3460',
                'entry_bg': '#B9D7EA',
                'progress_bg': '#E3DFFD'
            }
        }

        # Apply initial theme
        self.apply_theme(self.current_theme)

        # Create UI components
        self.create_header()
        self.create_download_section()
        self.create_progress_section()

    def apply_theme(self, theme_name):
        """
        Apply selected theme to the entire application
        """
        theme = self.themes[theme_name]

        # Configure master window
        self.master.configure(bg=theme['bg_primary'])

        # Update header if exists
        if hasattr(self, 'header_frame'):
            self.header_frame.configure(bg=theme['bg_tertiary'])
            self.logo_label.configure(
                bg=theme['bg_tertiary'], fg=theme['fg_primary'])
            self.theme_toggle.configure(
                bg=theme['bg_tertiary'], fg=theme['fg_primary'])

        # Update download section if exists
        if hasattr(self, 'download_frame'):
            self.download_frame.configure(bg=theme['bg_primary'])
            self.url_label.configure(
                bg=theme['bg_primary'], fg=theme['fg_primary'])
            self.url_entry.configure(
                bg=theme['entry_bg'],
                fg=theme['fg_primary'],
                insertbackground=theme['fg_primary']
            )

        # Update quality radio buttons if exists
        if hasattr(self, 'quality_frame'):
            self.quality_frame.configure(bg=theme['bg_primary'])
            for rb in self.quality_radios:
                rb.configure(
                    bg=theme['bg_primary'],
                    fg=theme['fg_primary'],
                    selectcolor=theme['bg_tertiary']
                )

        # Update progress section if exists
        if hasattr(self, 'progress_frame'):
            self.progress_frame.configure(bg=theme['bg_primary'])
            self.download_btn.configure(
                bg=theme['bg_tertiary'],
                fg=theme['fg_primary'],
                activebackground=theme['bg_secondary']
            )
            self.status_label.configure(
                bg=theme['bg_primary'],
                fg=theme['fg_secondary']
            )

    def create_header(self):
        """
        Create a modern header with theme toggle
        """
        theme = self.themes[self.current_theme]

        # Header Frame
        self.header_frame = tk.Frame(
            self.master,
            bg=theme['bg_tertiary'],
            height=80
        )
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        self.header_frame.pack_propagate(False)

        # Logo
        self.logo_label = tk.Label(
            self.header_frame,
            text="🎥 UltraDown",
            font=("Helvetica", 24, "bold"),
            fg=theme['fg_primary'],
            bg=theme['bg_tertiary']
        )
        self.logo_label.pack(side=tk.LEFT, padx=20)

        # Theme Toggle Button
        self.theme_toggle = tk.Button(
            self.header_frame,
            text="🌓",
            font=("Helvetica", 16),
            bg=theme['bg_tertiary'],
            fg=theme['fg_primary'],
            borderwidth=0,
            command=self.toggle_theme
        )
        self.theme_toggle.pack(side=tk.RIGHT, padx=20)

    def create_download_section(self):
        """
        Create download input section
        """
        theme = self.themes[self.current_theme]

        # Download Frame
        self.download_frame = tk.Frame(
            self.master,
            bg=theme['bg_primary']
        )
        self.download_frame.pack(padx=40, pady=20, fill=tk.X)

        # URL Label
        self.url_label = tk.Label(
            self.download_frame,
            text="Enter YouTube URL",
            font=tkFont.Font(family="Helvetica", size=17, weight="bold"),
            bg=theme['bg_primary'],
            fg=theme['fg_primary']
        )
        self.url_label.pack(anchor='w')

        # URL Entry
        self.url_entry = tk.Entry(
            self.download_frame,
            font=("Helvetica", 12),
            width=70,
            bg=theme['entry_bg'],
            fg=theme['fg_primary'],
            insertbackground=theme['fg_primary']
        )
        self.url_entry.pack(fill=tk.X, pady=10)

        # Quality Selection
        self.quality_frame = tk.Frame(
            self.download_frame,
            bg=theme['bg_primary']
        )
        self.quality_frame.pack(fill=tk.X)

        self.quality_var = tk.StringVar(value='best')
        qualities = [
            ('Best Quality', 'best'),
            ('Audio Only', 'audio'),
            ('720p', '720p'),
            ('Lowest', 'worst')
        ]

        self.quality_radios = []
        for text, value in qualities:
            rb = tk.Radiobutton(
                self.quality_frame,
                text=text,
                variable=self.quality_var,
                value=value,
                font=tkFont.Font(family="Helvetica", size=11, weight="bold"),
                bg=theme['bg_primary'],
                fg=theme['fg_primary'],
                selectcolor=theme['bg_tertiary']
            )
            rb.pack(side=tk.LEFT, padx=10)
            self.quality_radios.append(rb)

    def create_progress_section(self):
        """
        Create progress tracking section
        """
        theme = self.themes[self.current_theme]

        # Progress Frame
        self.progress_frame = tk.Frame(
            self.master,
            bg=theme['bg_primary']
        )
        self.progress_frame.pack(padx=40, pady=20, fill=tk.X)

        # Download Button
        self.download_btn = tk.Button(
            self.progress_frame,
            text="Download",
            command=self.start_download,
            font=("Helvetica", 16, "bold"),
            bg=theme['bg_tertiary'],
            fg=theme['fg_primary'],
            activebackground=theme['bg_secondary']
        )
        self.download_btn.pack(fill=tk.X, pady=10)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=10)

        # Status Label
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            self.progress_frame,
            textvariable=self.status_var,
            font=("Helvetica", 11),
            bg=theme['bg_primary'],
            fg="#66ffcc",
        )
        self.status_label.pack()

    def toggle_theme(self):
        """
        Toggle between dark and light themes
        """
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.apply_theme(self.current_theme)

    def start_download(self):
        """
        Initiate video download in a separate thread
        """
        # Validate URL
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        # Disable download button during download
        self.download_btn.config(state=tk.DISABLED)
        self.status_var.set("Downloading...")
        self.progress_var.set(0)

        # Start download in a separate thread
        download_thread = threading.Thread(
            target=self.download_video,
            args=(url, self.quality_var.get())
        )
        download_thread.start()

    def download_video(self, url, quality):
        """
        Download YouTube video with progress tracking

        Args:
        url (str): YouTube video URL
        quality (str): Selected video quality
        """
        try:
            # Quality mapping
            quality_formats = {
                'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'audio': 'bestaudio/best',
                '720p': 'bestvideo[height=720]+bestaudio/best[height=720]',
                'worst': 'worst'
            }

            # yt-dlp configuration
            ydl_opts = {
                'format': quality_formats[quality],
                'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video information
                info_dict = ydl.extract_info(url, download=True)

                # Update UI with success message
                self.master.after(0, self._download_complete,
                                  f"Download complete!\nSaved to: {os.getcwd()}")

        except Exception as e:
            # Show error message
            self.master.after(0, self._download_error, str(e))

    def _progress_hook(self, d):
        """
        Update progress bar and status

        Args:
        d (dict): Progress dictionary from yt-dlp
        """
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            percent = float(p.replace('%', ''))
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')

            # Update progress bar and status
            self.master.after(0, self._update_progress, percent, speed, eta)

    def _update_progress(self, percent, speed, eta):
        """
        Update GUI progress and status

        Args:
        percent (float): Download percentage
        speed (str): Download speed
        eta (str): Estimated time of arrival
        """
        self.progress_var.set(percent)
        self.status_var.set(
            f"Downloading: {percent}% (Speed: {speed}, ETA: {eta})")

    def _download_complete(self, message):
        """
        Handle successful download

        Args:
        message (str): Completion message
        """
        messagebox.showinfo("Download Complete", message)
        self.download_btn.config(state=tk.NORMAL)
        self.status_var.set("Ready")
        self.progress_var.set(0)

    def _download_error(self, error_message):
        """
        Handle download errors

        Args:
        error_message (str): Error description
        """
        messagebox.showerror("Download Error", error_message)
        self.download_btn.config(state=tk.NORMAL)
        self.status_var.set("Error occurred")
        self.progress_var.set(0)


def main():
    root = tk.Tk()
    root.title("UltraDown By CjaySolutions - YouTube Downloader")
    window_width = 800
    window_height = 550

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{
                  window_height}+{x_coordinate}+{y_coordinate}")

    app = AdvancedYouTubeDownloader(root)

    root.mainloop()


if __name__ == "__main__":
    main()
