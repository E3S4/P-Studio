import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pygame
from pydub import AudioSegment
from pydub.generators import Sine

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Map the notes to frequencies (C4 to B5 for two octaves)
note_frequencies = {
    "C": 261.63,   # C4
    "C#": 277.18,  # C#4
    "D": 293.66,   # D4
    "D#": 311.13,  # D#4
    "E": 329.63,   # E4
    "F": 349.23,   # F4
    "F#": 369.99,  # F#4
    "G": 392.00,   # G4
    "G#": 415.30,  # G#4
    "A": 440.00,   # A4
    "A#": 466.16,  # A#4
    "B": 493.88,   # B4
    "C2": 523.25,  # C5
    "C#2": 554.37, # C#5
    "D2": 587.33,  # D5
    "D#2": 622.25, # D#5
    "E2": 659.26,  # E5
    "F2": 698.46,  # F5
    "F#2": 739.99, # F#5
    "G2": 783.99,  # G5
    "G#2": 830.61, # G#5
    "A2": 880.00,  # A5
    "A#2": 932.33, # A#5
    "B2": 987.77   # B5
}

# Function to generate note sound
def generate_sound(note, duration=500):
    if note in note_frequencies:
        frequency = note_frequencies[note]
        sound = Sine(frequency).to_audio_segment(duration=duration)
        return sound
    return None

# Play a note sound (this can be hooked into the piano roll interaction)
def play_note(note):
    sound = generate_sound(note)
    if sound:
        pygame.mixer.Sound(sound.raw_data).play()

# Piano Roll Class (updated with sound and recording)
class PianoRoll(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Piano Roll")
        self.geometry("800x400")
        self.configure(bg='#141d25')

        # Create canvas
        self.canvas = tk.Canvas(self, width=800, height=400, bg="lightgray")
        self.canvas.pack()

        # Draw piano keys
        key_width = 20
        key_height = 40
        white_keys = ["C", "D", "E", "F", "G", "A", "B"]
        black_keys = ["C#", "D#", "F#", "G#", "A#"]

        # Draw white keys
        for i, key in enumerate(white_keys):
            x1 = i * key_width * 2
            x2 = x1 + key_width * 2
            y1, y2 = 0, key_height
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
            self.canvas.create_text((x1 + x2) / 2, y2 + 5, text=key, fill="black", font=("Arial", 10))

        # Draw black keys
        for i, key in enumerate(black_keys):
            x1 = (i * key_width * 2) + key_width
            x2 = x1 + key_width
            y1, y2 = 0, key_height / 2
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
            self.canvas.create_text((x1 + x2) / 2, y2 + 5, text=key, fill="white", font=("Arial", 10))

        # Draw time grid
        time_unit = 40
        for i in range(1, 20):
            x = i * time_unit
            self.canvas.create_line(x, 0, x, 400, width=1, fill="black")

        # Bind mouse events for note drawing
        self.canvas.bind("<Button-1>", self.draw_note)

        # Store notes
        self.notes = []

        # Add Play button
        self.play_button = tk.Button(self, text="Play Notes", command=self.play_recorded_notes, font=("Arial", 12), bg='green', fg='white')
        self.play_button.pack(pady=10)

    def draw_note(self, event):
        pitch = int(event.y // 40)
        if pitch < 0 or pitch >= 7:  # Limit to 7 pitches (C to B)
            return

        start_time = int(event.x // 40)
        if start_time < 0:
            return

        # Get pitch name based on y-coordinate
        pitch_names = ["C", "D", "E", "F", "G", "A", "B"]
        pitch_name = pitch_names[pitch]

        # Visual feedback for note
        x1 = start_time * 40
        x2 = x1 + 40
        y1 = pitch * 40
        y2 = y1 + 40
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")

        # Store the note (note format: (start_time, duration, pitch))
        self.notes.append((start_time, 1, pitch_name))  # Duration is 1 for now

        # Play the note
        play_note(pitch_name)  # Play sound when note is drawn

    # Playback function to replay the recorded notes
    def play_recorded_notes(self):
        start_time = 0  # Start at time 0 for playback
        for note in self.notes:
            note_start_time, duration, pitch_name = note

            # Play the note after the correct delay (this ensures sequential playback)
            delay = (note_start_time - start_time) * 1000  # Convert to milliseconds
            self.after(delay, play_note, pitch_name)  # Schedule note to play

            # Update start_time for the next note
            start_time = note_start_time

# Function Definitions
def open_piano_roll():
    PianoRoll()

def open_plugins_in_use():
    clear_playlist()
    label = tk.Label(playlist_frame, text="Plugins In Use", bg='#141d25', fg='white', font=("Arial", 16))
    label.pack()

def open_mixer():
    clear_playlist()
    label = tk.Label(playlist_frame, text="Mixer", bg='#141d25', fg='white', font=("Arial", 16))
    label.pack()

def open_playlist():
    clear_playlist()
    label = tk.Label(playlist_frame, text="Playlist", bg='#141d25', fg='white', font=("Arial", 16))
    for track in playlist:
        tk.Label(playlist_frame, text=track, bg='#141d25', fg='white').pack()

def open_browser():
    clear_playlist()
    label = tk.Label(playlist_frame, text="Browser", bg='#141d25', fg='white', font=("Arial", 16))
    label.pack()

def open_channel_rack():
    clear_playlist()
    label = tk.Label(playlist_frame, text="Channel Rack", bg='#141d25', fg='white', font=("Arial", 16))
    label.pack()

def start_recording():
    clear_playlist()
    label = tk.Label(playlist_frame, text="Recording...", bg='#141d25', fg='red', font=("Arial", 16))
    label.pack()

def stop_recording():
    clear_playlist()
    label = tk.Label(playlist_frame, text="Stopped Recording", bg='#141d25', fg='white', font=("Arial", 16))
    label.pack()

def clear_playlist():
    for widget in playlist_frame.winfo_children():
        widget.destroy()

def add_track():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file_path:
        playlist.append(file_path)
        open_playlist()


# Main Application Window
def start_app():
    global window, playlist_frame, playlist
    playlist = []

    window = tk.Tk()
    window.geometry('1360x680')
    window.config(background='#17202a')
    window.title("P-Studio")

    toolbar = tk.Frame(window, bg='#17202a', height=50)
    toolbar.pack(fill='x')

    # Toolbar buttons
    buttons = [
        ("🎹 Piano Roll", open_piano_roll),
        ("🔌 Plugins", open_plugins_in_use),
        ("🎚 Mixer", open_mixer),
        ("📋 Playlist", open_playlist),
        ("📁 Browser", open_browser),
        ("🎛 Channel Rack", open_channel_rack),
        ("● Record", start_recording),
        ("■ Stop", stop_recording),
        ("➕ Add Track", add_track)
    ]

    for text, command in buttons:
        tk.Button(toolbar, text=text, command=command, font=("Arial", 12), bg='black', fg='white').pack(side='left', padx=5)

    playlist_frame = tk.Frame(window, bg='#141d25')
    playlist_frame.pack(fill='both', expand=True, padx=10, pady=10)

    window.mainloop()

# Run the Application
if __name__ == "__main__":
    start_app()
