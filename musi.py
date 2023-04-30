import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.geometry("500x250")
        self.master.resizable(False, False)
        
        self.current_track = ""
        self.paused = False
        self.duration = 0
        self.time = 0
        
        self.master.configure(bg='#333333')
        
        self.select_button = tk.Button(self.master, text="Select", command=self.select_file, bg='#555555', fg='#FFFFFF', activebackground='#777777', activeforeground='#FFFFFF')
        self.select_button.place(relx=0.5, rely=0.1, anchor="center")
        
        self.play_button = tk.Button(self.master, text="Play", command=self.play, bg='#555555', fg='#FFFFFF', activebackground='#777777', activeforeground='#FFFFFF')
        self.play_button.place(relx=0.35, rely=0.25, anchor="center")
        
        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause, bg='#555555', fg='#FFFFFF', activebackground='#777777', activeforeground='#FFFFFF')
        self.pause_button.place(relx=0.5, rely=0.25, anchor="center")
        
        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop, bg='#555555', fg='#FFFFFF', activebackground='#777777', activeforeground='#FFFFFF')
        self.stop_button.place(relx=0.65, rely=0.25, anchor="center")
        
        self.file_label = tk.Label(self.master, text="No file selected.", bg='#333333', fg='#FFFFFF')
        self.file_label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.progress_bar_label = tk.Label(self.master, text="00:00 / 00:00", bg='#333333', fg='#FFFFFF')
        self.progress_bar_label.place(relx=0.5, rely=0.55, anchor="center")
        
        self.progress_bar = tk.ttk.Progressbar(self.master, orient="horizontal", length=400, mode="determinate", style='Custom.Horizontal.TProgressbar')
        self.progress_bar.place(relx=0.5, rely=0.65, anchor="center")
        self.progress_bar.configure(style='Custom.Horizontal.TProgressbar')
        
        pygame.mixer.init()
    
    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.current_track = file_path
        self.file_label.config(text=file_path)
        self.duration = pygame.mixer.Sound(file_path).get_length()
        self.progress_bar_label.config(text=f"00:00 / {self.format_time(self.duration)}")
        
    def play(self):
        if not self.paused:
            pygame.mixer.music.load(self.current_track)
            self.time = 0
        pygame.mixer.music.play(start=self.time)
        self.paused = False
        self.update_progress()
        
    def pause(self):
        self.time = pygame.mixer.music.get_pos() / 1000
        pygame.mixer.music.pause()
        self.paused = True
        
    def stop(self):
        pygame.mixer.music.stop()
        self.paused = False
        self.time = 0
        self.progress_bar["value"] = 0
        self.progress_bar_label.config(text="00:00 / 00:00")
        
    def update_progress(self):
        self.time = pygame.mixer.music.get_pos() / 1000
        if not self.paused:
            self.progress_bar["value"] = self.time
            self.progress_bar_label.config(text=f"{self.format_time(self.time)} / {self.format_time(self.duration)}")
        self.master.after(100, self.update_progress)
        
    def format_time(self, time_in_seconds):
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        return f"{minutes:02}:{seconds:02}"

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
