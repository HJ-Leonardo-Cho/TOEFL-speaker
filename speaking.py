import tkinter as tk
from tkinter import font, messagebox
import os
import sys
import time
import pandas as pd
from google.cloud import texttospeech
from playsound import playsound
import sounddevice as sd
from scipy.io.wavfile import write
import threading

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

####################      Configuration       ##############################
#######            Google cloud key, question CSV                 ##########
GCP_KEY_FILE = resource_path("toefl-speaking-468212-e1c9137fbacc.json")
CSV_FILE = resource_path("questions_vol1.csv")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_KEY_FILE
PREP_TIME = 15
RECORD_TIME = 45
SAMPLE_RATE = 44100

class TOEFLPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TOEFL Speaking Practice")
        self.root.geometry("800x600")

        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.text_font = font.Font(family="Helvetica", size=12)
        self.timer_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.questions = self.load_questions()
        self.current_question_index = -1
        self.last_recording_filename = ""

        self.question_label = tk.Label(root, text="TOEFL Independent Speaking Practice", font=self.title_font, wraplength=750)
        self.question_label.pack(pady=20)

        self.question_text = tk.Text(root, height=10, width=80, font=self.text_font, wrap=tk.WORD, padx=10, pady=10)
        self.question_text.pack(pady=10)
        self.question_text.insert(tk.END, "Press the 'Next Question' button below to begin.")
        self.question_text.config(state=tk.DISABLED)

        self.status_label = tk.Label(root, text="Status: Waiting", font=self.text_font)
        self.status_label.pack(pady=10)

        self.timer_label = tk.Label(root, text="", font=self.timer_font, fg="blue")
        self.timer_label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.listen_button = tk.Button(self.button_frame, text="Review My Answer", font=self.button_font, command=self.play_last_recording, bg="orange", fg="white")

        self.start_button = tk.Button(self.button_frame, text="Next Question", font=self.button_font, command=self.start_next_question, bg="green", fg="white")
        self.start_button.pack()
        
        ###################credit for HJ Leonardo###############
        self.credit_font = font.Font(family="Helvetica", size=10, slant="italic")
        self.credit_label = tk.Label(root, text="Made by HJ Leonardo", font=self.credit_font, fg="gray70")
        self.credit_label.pack(side=tk.BOTTOM, pady=5)
        ########################################################
        
    def load_questions(self):
        try:
            return pd.read_csv(CSV_FILE)['question'].tolist()
        except FileNotFoundError:
            messagebox.showerror("Error", f"Required file not found:\n{os.path.basename(CSV_FILE)}\n\nExiting the application.")
            self.root.quit()
            return []
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file:\n{e}\n\nExiting the application.")
            self.root.quit()
            return []

    def start_next_question(self):
        self.listen_button.pack_forget()
        self.start_button.config(text="Next Question")

        if not self.questions:
            self.start_button.config(state=tk.DISABLED, text="Error: No Questions")
            return

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            
            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete('1.0', tk.END)
            self.question_text.insert(tk.END, f"Q{self.current_question_index + 1}: {question}")
            self.question_text.config(state=tk.DISABLED)

            self.start_button.pack_forget()
            threading.Thread(target=self.run_practice_flow, args=(question,)).start()
        else:
            self.status_label.config(text="🎉 All questions completed! Well done.")
            self.start_button.pack()
            self.start_button.config(text="Exit", command=self.root.quit)

    def run_practice_flow(self, question):
        self.status_label.config(text="Status: Listening to the question...")
        self.speak(question)

        self.countdown(PREP_TIME, "Preparation Time", "blue")
        
        self.last_recording_filename = f"response_{self.current_question_index + 1}.wav"
        
        recording_thread = threading.Thread(target=self.record_audio, args=(RECORD_TIME, self.last_recording_filename))
        recording_thread.start()
        
        self.countdown(RECORD_TIME, "Recording Answer...", "red")
        recording_thread.join()
        
        self.status_label.config(text=f"Status: Recording complete! ({self.last_recording_filename} saved)")
        
        self.listen_button.pack(side=tk.LEFT, padx=10)
        self.start_button.pack(side=tk.LEFT, padx=10)
    
    def play_last_recording(self):
        if self.last_recording_filename and os.path.exists(self.last_recording_filename):
            def play_sound():
                self.listen_button.config(state=tk.DISABLED)
                self.start_button.config(state=tk.DISABLED)
                self.status_label.config(text=f"Status: Playing '{self.last_recording_filename}'...")
                
                playsound(self.last_recording_filename)
                
                self.status_label.config(text=f"Status: Recording complete! ({self.last_recording_filename} saved)")
                self.listen_button.config(state=tk.NORMAL)
                self.start_button.config(state=tk.NORMAL)
            
            threading.Thread(target=play_sound).start()

    def countdown(self, seconds, message, color="blue"):
        self.status_label.config(text=f"Status: {message}")
        self.timer_label.config(fg=color)
        for i in range(seconds, 0, -1):
            self.timer_label.config(text=f"{i}")
            time.sleep(1)
        self.timer_label.config(text="")

    def speak(self, text, temp_filename="_temp_question.mp3"):
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Studio-M") ## M : male, O:Female
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            
            with open(temp_filename, "wb") as out:
                out.write(response.audio_content)
            
            playsound(temp_filename)

        except Exception as e:
            messagebox.showerror("TTS API Error", f"An error occurred during speech synthesis:\n{e}\n\nPlease check if your authentication key file is correct.")
            self.status_label.config(text="Error: TTS API Authentication Failed")
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def record_audio(self, duration, filename):
        recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()
        write(filename, SAMPLE_RATE, recording)

if __name__ == "__main__":
    if not os.path.exists(CSV_FILE) or not os.path.exists(GCP_KEY_FILE):
        error_msg = ""
        if not os.path.exists(CSV_FILE): error_msg += f"Question file not found: {os.path.basename(CSV_FILE)}\n"
        if not os.path.exists(GCP_KEY_FILE): error_msg += f"Auth key file not found: {os.path.basename(GCP_KEY_FILE)}\n"
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("File Not Found Error", f"Required files are missing:\n{error_msg}\nExiting the application.")
    else:
        root = tk.Tk()
        app = TOEFLPracticeApp(root)
        root.mainloop()