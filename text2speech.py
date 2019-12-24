from tkinter import Tk, Label, Button, Text, Scale, Entry, StringVar, DoubleVar, END
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfile
import tkinter.scrolledtext as tkst
from google.cloud import texttospeech
from playsound import playsound

root = Tk()
root.title("Convert text to speech")
# root.geometry("600x400")

client = texttospeech.TextToSpeechClient()
voices = client.list_voices()

Language = ("English (Australia)","English (UK)","English (US)","Mandarin Chinese")
Language_Code = ("en-AU", "en-GB", "en-US", "cmn-CN")
Voice = ("Standard", "WaveNet")
Voice_Type = ("Standard", "Wavenet")

file_path = ""
def uploadAction():
    global file_path
    file_path = askopenfilename(title = "Select file", filetypes = [('txt', '*.txt')])
    entry_filename.insert('insert', file_path)
    if file_path is not None:
        with open(file_path, 'r') as f:
            input_text = f.read()
        maintext.delete('1.0', END)
        maintext.insert(END, input_text)

def method():
    keywords = Language_Code[cb1.current()] + "-" + Voice_Type[cb2.current()]  
    voice_names = []
    for voice in voices.voices:
        voice_name = voice.name
        if str(keywords) in voice_name:
            voice_names.append(voice_name)
    cb3['values'] = voice_names
    return voice_names

def updateVoiceName(*args):
    method()
    cb3.current(0)

def generate_voice(text):
    input_text = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(language_code= cb3.get())
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding = texttospeech.enums.AudioEncoding.MP3,
        speaking_rate = s1.get(), 
        pitch = s2.get())
    response = client.synthesize_speech(input_text, voice, audio_config)
    return response

def save(event):
    response = generate_voice(text = maintext.get('1.0', END))
    out = asksaveasfile(mode='wb', initialfile=".mp3")
    out.write(response.audio_content)
 

# input text file
Label(root, text = "Import Text File:").grid(row = 0, column = 0, sticky = "e")
entry_filename = Entry(root)
entry_filename.grid(row = 0, column = 1, sticky = "we")
Button(root, text = "Browse", command = uploadAction, bg="blue").grid(row = 0, column = 2, sticky = "w")

maintext = tkst.ScrolledText(root, bg="#cccccc", font=("Helvetica", 14), height = 12)
maintext.grid(row = 1, columnspan = 3, sticky = "nsew", padx=2, pady=2)
maintext.insert('1.0', "Enter the text to speak:")

# tool set
## row 2
Label(root, text = "Language / locale").grid(row = 2, column = 0, sticky = "w", pady=2)
Label(root, text = "Voice type").grid(row = 2, column = 1, sticky = "w", pady=2)
Label(root, text = "Voice name").grid(row = 2, column = 2, sticky = "w", pady=2)

## row 3
cb1 = ttk.Combobox(root)
cb1.grid(row = 3, column = 0, sticky = "we")
cb1['value'] = Language
cb1.current(2)
cb1.bind("<<ComboboxSelected>>", updateVoiceName)

cb2 = ttk.Combobox(root)
cb2.grid(row = 3, column = 1, sticky = "we")
cb2['value'] = Voice
cb2.current(1)
cb2.bind("<<ComboboxSelected>>", updateVoiceName)

cb3 = ttk.Combobox(root)
cb3.grid(row = 3, column = 2, sticky = "we")
cb3['value'] = method()
cb3.current(0)

## row 4
v1 = DoubleVar() 
s1 = Scale(root, label = "Speed:", variable = v1, from_=0.25, to=4.00, orient="horizontal", resolution = 0.01)
s1.grid(row = 4, column = 1, sticky = "wens")
s1.set(1.00)

v2 = DoubleVar() 
s2 = Scale(root, label = "Pitch:", variable = v2, from_=-20, to=20.00, orient="horizontal", resolution = 0.01)
s2.grid(row = 4, column = 2, sticky = "wens")
s2.set(0)

# row 5: Check and save
# bt1 = Button(root, text = "SPEAK IT", font=("Helvetica", 18, "bold"))
# bt1.grid(row = 5, column = 1, pady = 20, sticky = "we")
bt2 = Button(root, text = "SAVE", fg = "blue", font=("Helvetica", 20, "bold"))
bt2.grid(row = 5, column = 0, columnspan = 3, ipadx = 10, ipady = 5, pady = 10)
bt2.bind('<Button-1>', save)


root.mainloop()
