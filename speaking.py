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

# --- PyInstaller를 위한 경로 설정 함수 ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- 설정 (Configuration) ---
# 본인의 파일 이름으로 되어 있는지 다시 한번 확인해주세요!
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

        self.question_label = tk.Label(root, text="TOEFL 독립형 스피킹 연습", font=self.title_font, wraplength=750)
        self.question_label.pack(pady=20)

        self.question_text = tk.Text(root, height=10, width=80, font=self.text_font, wrap=tk.WORD, padx=10, pady=10)
        self.question_text.pack(pady=10)
        self.question_text.insert(tk.END, "아래 '다음 문제 시작' 버튼을 눌러 연습을 시작하세요.")
        self.question_text.config(state=tk.DISABLED)

        self.status_label = tk.Label(root, text="상태: 대기 중", font=self.text_font)
        self.status_label.pack(pady=10)

        self.timer_label = tk.Label(root, text="", font=self.timer_font, fg="blue")
        self.timer_label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.listen_button = tk.Button(self.button_frame, text="답변 듣기", font=self.button_font, command=self.play_last_recording, bg="orange", fg="white")

        self.start_button = tk.Button(self.button_frame, text="다음 문제 시작", font=self.button_font, command=self.start_next_question, bg="green", fg="white")
        self.start_button.pack()
        
    def load_questions(self):
        try:
            return pd.read_csv(CSV_FILE)['question'].tolist()
        except FileNotFoundError:
            messagebox.showerror("오류", f"필수 파일을 찾을 수 없습니다:\n{os.path.basename(CSV_FILE)}\n\n프로그램을 종료합니다.")
            self.root.quit()
            return []
        except Exception as e:
            messagebox.showerror("오류", f"파일을 읽는 중 오류가 발생했습니다:\n{e}\n\n프로그램을 종료합니다.")
            self.root.quit()
            return []

    def start_next_question(self):
        self.listen_button.pack_forget()
        self.start_button.config(text="다음 문제 시작")

        if not self.questions:
            self.start_button.config(state=tk.DISABLED, text="오류 발생")
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
            self.status_label.config(text="🎉 모든 질문을 완료했습니다! 수고하셨습니다.")
            self.start_button.pack()
            self.start_button.config(text="종료", command=self.root.quit)

    def run_practice_flow(self, question):
        self.status_label.config(text="상태: 질문을 듣는 중...")
        self.speak(question)

        self.countdown(PREP_TIME, "준비 시간", "blue")
        
        self.last_recording_filename = f"response_{self.current_question_index + 1}.wav"
        
        recording_thread = threading.Thread(target=self.record_audio, args=(RECORD_TIME, self.last_recording_filename))
        recording_thread.start()
        
        self.countdown(RECORD_TIME, "답변 녹음 중", "red")
        recording_thread.join()
        
        self.status_label.config(text=f"상태: 녹음 완료! ({self.last_recording_filename} 저장)")
        
        self.listen_button.pack(side=tk.LEFT, padx=10)
        self.start_button.pack(side=tk.LEFT, padx=10)
    
    def play_last_recording(self):
        if self.last_recording_filename and os.path.exists(self.last_recording_filename):
            def play_sound():
                self.listen_button.config(state=tk.DISABLED)
                self.start_button.config(state=tk.DISABLED)
                self.status_label.config(text=f"상태: '{self.last_recording_filename}' 재생 중...")
                
                playsound(self.last_recording_filename)
                
                self.status_label.config(text=f"상태: 녹음 완료! ({self.last_recording_filename} 저장)")
                self.listen_button.config(state=tk.NORMAL)
                self.start_button.config(state=tk.NORMAL)
            
            threading.Thread(target=play_sound).start()

    def countdown(self, seconds, message, color="blue"):
        self.status_label.config(text=f"상태: {message}")
        self.timer_label.config(fg=color)
        for i in range(seconds, 0, -1):
            self.timer_label.config(text=f"{i}")
            time.sleep(1)
        self.timer_label.config(text="")

    # ▼▼▼▼▼ speak 함수가 요청하신 대로 최종 수정되었습니다 ▼▼▼▼▼
    def speak(self, text, temp_filename="_temp_question.mp3"):
        """임시 파일을 만들고 재생 후 즉시 삭제하는 함수"""
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Studio-O")
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            
            # 음성 데이터를 임시 파일로 저장
            with open(temp_filename, "wb") as out:
                out.write(response.audio_content)
            
            # 저장된 임시 파일 재생
            playsound(temp_filename)

        except Exception as e:
            messagebox.showerror("TTS API 오류", f"음성 변환 중 오류가 발생했습니다:\n{e}\n\n인증 키 파일이 올바른지 확인하세요.")
            self.status_label.config(text="오류: TTS API 인증 실패")
        finally:
            # 재생이 끝나거나 오류가 발생해도 임시 파일은 반드시 삭제
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def record_audio(self, duration, filename):
        recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()
        write(filename, SAMPLE_RATE, recording)

if __name__ == "__main__":
    if not os.path.exists(CSV_FILE) or not os.path.exists(GCP_KEY_FILE):
        error_msg = ""
        if not os.path.exists(CSV_FILE): error_msg += f"질문 파일 없음: {os.path.basename(CSV_FILE)}\n"
        if not os.path.exists(GCP_KEY_FILE): error_msg += f"인증 키 파일 없음: {os.path.basename(GCP_KEY_FILE)}\n"
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("파일 없음 오류", f"필수 파일이 없습니다:\n{error_msg}\n프로그램을 종료합니다.")
    else:
        root = tk.Tk()
        app = TOEFLPracticeApp(root)
        root.mainloop()