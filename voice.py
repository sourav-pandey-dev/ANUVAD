import tkinter as tk
from tkinter import ttk
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import speech_recognition as sr
from datetime import date
import google.generativeai as genai

# Initialize the mixer
mixer.init()

# Set Google Gemini API key
genai.configure(api_key="AIzaSyCaFda7lfrVBBSkbIRnLJVuI52pKqH13Es")

today = str(date.today())

# Configure the Generative AI model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()
gf = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 128,
}

safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Language options and mapping
language_map = {
    "English": "en",
    "Chinese": "zh-CN",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

# Text-to-speech function
def speak_text(text):
    mp3audio = BytesIO()
    tts = gTTS(text, lang=language_map[target_language.get()], tld='us')
    tts.write_to_fp(mp3audio)
    mp3audio.seek(0)
    mixer.music.load(mp3audio, "mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    mp3audio.close()

# Save conversation to a log file
def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a", encoding='utf-8') as f:
        f.write(text + "\n")

# Main function to process speech and translation
def translate_speech():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400

    try:
        with mic as source1:
            status_label.config(text="Listening...")
            root.update()
            rec.adjust_for_ambient_noise(source1, duration=0.5)
            audio = rec.listen(source1, timeout=20, phrase_time_limit=30)

        user_text = rec.recognize_google(audio, language=language_map[source_language.get()])
        if len(user_text) < 2:
            status_label.config(text="Could not recognize speech. Try again.")
            return

        request = f"Translate this to {language_map[target_language.get()]}: {user_text}"
        append2log(f"You: {user_text}\n")

        response = chat.send_message(request, generation_config=gf, safety_settings=safety_settings)
        translated_text = response.text.replace("*", "")
        append2log(f"AI: {translated_text}\n")

        output_label.config(text=f"Translation: {translated_text}")
        speak_text(translated_text)

        status_label.config(text="Translation complete.")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Speech Translator")
root.geometry("500x400")

# Source Language Dropdown
source_language_label = tk.Label(root, text="Source Language:")
source_language_label.pack(pady=5)
source_language = ttk.Combobox(root, values=list(language_map.keys()))
source_language.set("English")
source_language.pack(pady=5)

# Target Language Dropdown
target_language_label = tk.Label(root, text="Target Language:")
target_language_label.pack(pady=5)
target_language = ttk.Combobox(root, values=list(language_map.keys()))
target_language.set("Chinese")
target_language.pack(pady=5)

# Translate Button
translate_button = tk.Button(root, text="Translate", command=translate_speech)
translate_button.pack(pady=20)

# Output Label
output_label = tk.Label(root, text="Translation: ", wraplength=400)
output_label.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Waiting", wraplength=400)
status_label.pack(pady=10)

# Run the application
root.mainloop()
