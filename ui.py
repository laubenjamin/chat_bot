from tkinter import ttk
import tkinter as tk
from octo_ai import ai_chat

class GUI(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        #self.ai = ai_chat()
        #self.recorder = 
        self.frames = {} 
        self.name = None
        screens = (StartScreen, ChatScreen)
        container = tk.Frame(self, padx=100, pady=100)
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        for x in screens:

            frame = x(container, self)
            self.frames[x] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.display(StartScreen)

    def display(self, cur_screen):
        frame = self.frames[cur_screen]
        frame.tkraise()
    
class StartScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.name_var = tk.StringVar()
        name_label = tk.Label(self, text = 'What is your name?', font=('calibre',10, 'bold'))
        name_entry = tk.Entry(self, textvariable = self.name_var, font=('calibre',10,'normal'))
        sub_btn = tk.Button(self,text = 'Sumbit', command = self.submit)
        name_label.grid(row=0,column=0)
        name_entry.grid(row=0,column=1)
        sub_btn.grid(row=2,column=1)

    def submit(self):
        if self.name_var != "":
            self.controller.name = self.name_var
            self.controller.display(ChatScreen)

class ChatScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.greetings = ["Ciao Ryan, piacere di conoscerti", "Certo, sarei felice di aiutarti! Cosa ti piacerebbe imparare sull'italiano?"]
        self.greeting_count = 0
        self.controller = controller
        self.starting_mic = True
        self.audio = None
        self.chosen_langauge = ""
        self.response_box = tk.Label(self, font=('calibre',10, 'bold'))
        self.lang_dropdown = ttk.Combobox(self,
            state="readonly",
            values=["English", "Italian"]
        )
        self.lang_dropdown.bind("<<ComboboxSelected>>", self.update_chat)
        dropdown_label = tk.Label(self, text= "Select Language", font=('calibre',10, 'bold'))
        microphone_butt = tk.Button(self,text = 'Start 5 Second Recording', command = self.record_audio)
        self.response_box.grid(row=3, column=0)
        dropdown_label.grid(row=0, column=0)
        self.lang_dropdown.grid(row=1, column=0)
        microphone_butt.grid(row=2, column=0)

    def record_audio(self):
        self.response_box.text = "RECORDING"
        #self.audio = self.controller.recorder.start(5)
        #text = self.controller.ai.getAIResponse(self.audio)
        self.controller.after(5000)
        response = self.greetings[self.greeting_count]
        self.typing(response)
        self.starting_mic = True
        if self.greeting_count < 1:
            self.greeting_count += 1
        #convert response: str to voice

        #display response:

    def typing(self, text, counter=1):
        self.response_box.config(text=text[:counter])
        if counter < len(text):
            self.controller.after(50, lambda: self.typing(text, counter+1))

    def update_chat(self):
        self.greeting_count = 0
        self.chosen_langauge = self.lang_dropdown.get()
        #self.controller.ai.language_update(self.lang_dropdown.get())
        pass

app = GUI()
app.mainloop()