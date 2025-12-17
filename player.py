import tkinter as tk
import sys
import os
import glob

# Audio handling using ONLY Standard Library
# 'winsound' is built-in on Windows. 
# For Mac/Linux, we can use subprocess to call system audio players.
if sys.platform == "win32":
    import winsound

def play_audio(path):
    if sys.platform == "win32":
        # SND_FILENAME = play from file
        # SND_ASYNC = play in background (don't freeze the video)
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif sys.platform == "darwin": # Mac
        import subprocess
        subprocess.Popen(['afplay', path])
    else: # Linux
        import subprocess
        subprocess.Popen(['aplay', path])

class Player:
    def __init__(self, frames_folder, audio_path):
        self.root = tk.Tk()

        # 1. SETUP WINDOW (Frameless & Topmost)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-toolwindow", True) # Hides from taskbar

        # 2. SETUP TRANSPARENCY
        transparent_color = "#00ff00" 
        self.root.config(bg=transparent_color)
        if sys.platform == "win32":
            self.root.wm_attributes("-transparentcolor", transparent_color)

        # 3. FULLSCREEN SETUP
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # 4. LOAD IMAGES
        # Get all png files from the folder and sort them
        search_path = os.path.join(frames_folder, "*.png")
        files = sorted(glob.glob(search_path))
        
        if not files:
            print("Error: No PNGs found in", frames_folder)
            sys.exit(1)

        # Pre-load all images into memory to prevent lag
        self.frames = []
        for f in files:
            self.frames.append(tk.PhotoImage(file=f))

        self.total_frames = len(self.frames)
        self.current_frame = 0

        # 5. UI SETUP
        self.label = tk.Label(self.root, bg=transparent_color, borderwidth=0)
        self.label.pack(expand=True)

        # 6. START audio
        play_audio(audio_path)
        
        # Start animation
        self.root.after(0, self.animate)
        self.root.mainloop()

    def animate(self):
        if self.current_frame >= self.total_frames:
            self.root.destroy()
            sys.exit()
            return

        # Update the image
        self.label.config(image=self.frames[self.current_frame])
        self.current_frame += 1
        
        # Schedule next frame
        self.root.after(33, self.animate)

if __name__ == "__main__":
    # Handle paths
    def resource_path(relative):
        try: base = sys._MEIPASS
        except: base = os.path.abspath(".")
        return os.path.join(base, relative)

    # Expects usage: python player_lite.py <frames_folder> <wav_file>
    if len(sys.argv) < 3:
        frames_dir = resource_path("frames") 
        audio_file = resource_path("jumpscare.wav")
    else:
        frames_dir = sys.argv[1]
        audio_file = sys.argv[2]

    Player(frames_dir, audio_file)