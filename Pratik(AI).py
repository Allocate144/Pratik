import tkinter as tk
from tkinter import simpledialog, font
from PIL import Image, ImageTk, ImageOps
import openai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
from datetime import datetime
import math
import threading
import time
import pyautogui

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Set your OpenAI API key from environment variable
openai.api_key = 'OPENAI_API_KEY'

# Store the name of the creator
creator_name = "Mayank"
creator_title = "Master"  # Can be "Sir" or "Master"

# Initialize conversation history
conversation_history = []
typing_mode = False  # State to keep track of typing mode

def record_audio(filename, duration=5, fs=44100):
    """Record audio from the microphone and save it to a file."""
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wav.write(filename, fs, recording)

def listen(filename="output.wav"):
    """Capture audio and convert it to text."""
    record_audio(filename)
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            return ""

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()  # Process and complete the text-to-speech request

def get_response(prompt):
    """Get response from OpenAI GPT using the conversation history."""
    conversation_history.append({"role": "user", "content": prompt})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an Assistant named 'Pratik', who works and talks just like JARVIS. Your creator is {creator_name}, and you regard {creator_name} as your {creator_title} who created you using Python. Your creator is a Male of 15 years"}
            ] + conversation_history
        )
        response_content = response.choices[0].message['content'].strip()
        conversation_history.append({"role": "assistant", "content": response_content})
        return response_content
    except Exception as e:
        return "I am sorry, I am unable to process your request at the moment, Master."

def open_website(site_name):
    """Open a specific website based on the site name."""
    urls = {
        "chrome": "https://www.google.com",
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.org",
        "instagram": "https://www.instagram.com",
        "gmail": "https://mail.google.com",
        "discord": "https://discord.com/app"
    }
    url = urls.get(site_name)
    if url:
        webbrowser.open(url)
        return True
    else:
        return False

def open_spotify():
    """Open Spotify and start playing music."""
    pyautogui.hotkey('win', 's')  # Open Windows search
    time.sleep(1)
    pyautogui.typewrite('Spotify')
    time.sleep(1)
    pyautogui.press('enter')  # Press Enter to open Spotify
    time.sleep(5)  # Wait for Spotify to open
    pyautogui.press('space')  # Press Space to play music

def open_chrome():
    pyautogui.hotkey('win', 's')  # Open Windows search
    time.sleep(1)
    pyautogui.typewrite('Google Chrome')
    time.sleep(1)
    pyautogui.press('enter')  # Press Enter to open the app

def open_chrome():
    pyautogui.hotkey('win', 's')  # Open Windows search
    time.sleep(1)
    pyautogui.typewrite('Camera')
    time.sleep(1)
    pyautogui.press('enter')  # Press Enter to open the app
    time.sleep(6)
    pyautogui.press('enter')

def get_time():
    """Get the current time."""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}, {creator_title}."

def process_input(user_input):
    global typing_mode
    """Process the user's input and respond."""
    if user_input.lower() in ["exit", "quit", "stop", "go to sleep"]:
        root.quit()

    if user_input.lower() == "the typing is done":
        typing_mode = False
        text_output.set("Pratik: Typing mode deactivated.")
        speak("Typing mode deactivated.")
        return

    if typing_mode:
        pyautogui.typewrite(user_input + " ")
        return

    if user_input.lower() == "type what i say":
        typing_mode = True
        text_output.set("Pratik: Typing mode activated. Start speaking...")
        speak("Typing mode activated. Start speaking...")
        return

    # Check if the user input contains any website command
    for site in ["chrome", "google", "youtube", "wikipedia", "instagram", "gmail", "discord"]:
        if site in user_input.lower():
            open_website(site)
            return

    # Check if the user input is a command to play music
    if "play some music" in user_input.lower() or "open spotify" in user_input.lower():
        open_spotify()
        return
    
    if "open the search engine" in user_input.lower() or "open chrome" in user_input.lower():
        open_chrome()
        return
    
    # Process the input as a general prompt
    if "time" in user_input.lower():
        current_time = get_time()
        text_output.set(f"Pratik: {current_time}")
        speak(current_time)
    else:
        response = get_response(user_input)
        text_output.set(f"Pratik: {response}")
        speak(response)

def rotate_image(image, angle):
    """Rotate an image by a given angle."""
    return ImageOps.exif_transpose(image.rotate(angle, resample=Image.BICUBIC, expand=True))

def update_animation():
    global angle, tk_image
    angle += 10  # Increase rotation speed
    if angle >= 360:
        angle = 0

    rotated_image = rotate_image(sharingan_image, angle)
    tk_image = ImageTk.PhotoImage(rotated_image)
    canvas.create_image(200, 200, image=tk_image)

    # Schedule the next animation frame with a shorter delay
    canvas.after(30, update_animation)

def listen_loop():
    """Continuously listen for audio input."""
    while True:
        user_input = listen()
        if user_input:
            process_input(user_input)
        else:
            speak(" ")

def create_rounded_button(canvas, text, x, y, width, height, radius, command, font, bg, fg):
    """Create a rounded button on the canvas."""
    id = canvas.create_rectangle(x, y, x + width, y + height, outline=bg, fill=bg)
    canvas.create_oval(x, y, x + 2*radius, y + 2*radius, outline=bg, fill=bg)
    canvas.create_oval(x + width - 2*radius, y, x + width, y + 2*radius, outline=bg, fill=bg)
    canvas.create_oval(x, y + height - 2*radius, x + 2*radius, y + height, outline=bg, fill=bg)
    canvas.create_oval(x + width - 2*radius, y + height - 2*radius, x + width, y + height, outline=bg, fill=bg)
    text_id = canvas.create_text(x + width/2, y + height/2, text=text, font=font, fill=fg)
    canvas.tag_bind(id, '<ButtonPress-1>', lambda e: command())
    canvas.tag_bind(text_id, '<ButtonPress-1>', lambda e: command())

def set_timer():
    """Set a timer based on user input."""
    duration = simpledialog.askinteger("Input", "Enter the duration for the timer in seconds:", minvalue=1)
    if duration:
        threading.Thread(target=start_timer, args=(duration,)).start()

def start_timer(duration):
    """Start the countdown timer."""
    for i in range(duration, 0, -1):
        text_output.set(f"Pratik: Timer: {i} seconds remaining")
        time.sleep(1)
    text_output.set("Pratik: Time is up!")
    speak("Time is up!")

# Create the GUI application
root = tk.Tk()
root.title("Pratik")
root.geometry("400x600")
root.configure(bg='black')

# Define fonts and colors
title_font = font.Font(family='Helvetica', size=16, weight='bold')
button_font = font.Font(family='Helvetica', size=12)
button_bg = '#FFC107'
button_fg = '#FFFFFF'
text_fg = '#FFFFFF'

# Load Sharingan image
sharingan_image_path = "C:/Users/mayan/OneDrive/Documents/Visual_Code/Python/test/Sharingan.png"
sharingan_image = Image.open(sharingan_image_path)
tk_image = ImageTk.PhotoImage(sharingan_image)

# Create UI elements
frame = tk.Frame(root, padx=10, pady=10, bg='black')
frame.pack(expand=True, fill='both')

title_label = tk.Label(frame, text="Pratik", font=title_font, bg='black', fg='white')
title_label.pack(pady=10)

canvas = tk.Canvas(frame, width=400, height=400, bg='black', highlightthickness=0)
canvas.pack()

text_output = tk.StringVar()
text_output.set("Pratik: How can I assist you today?")

output_label = tk.Label(frame, textvariable=text_output, wraplength=350, bg='black', fg=text_fg)
output_label.pack(pady=10)

# Draw custom curved buttons
create_rounded_button(canvas, "Process Input", 100, 420, 200, 50, 25, lambda: threading.Thread(target=listen_loop).start(), button_font, button_bg, button_fg)
create_rounded_button(canvas, "Set Timer", 100, 480, 200, 50, 25, set_timer, button_font, button_bg, button_fg)
create_rounded_button(canvas, "Exit", 100, 540, 200, 50, 25, root.quit, button_font, button_bg, button_fg)

# Initialize animation variables
angle = 0

# Start the animation
update_animation()

# Start the listening loop in a separate thread
threading.Thread(target=listen_loop).start()

# Run the application
root.mainloop()
