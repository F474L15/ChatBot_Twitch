import tkinter as tk

class ChatWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CHAT")

        self.root.geometry("400x600")
        self.root.resizable(False, False)

        self.text_area = tk.Text(self.root, font=("Arial", 12), bg="white", fg="black")
        self.text_area.pack(expand=True, fill="both")

        self.text_area.config(state=tk.DISABLED)
    
    def update_chat(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert("end", message + "\n")
        self.text_area.see("end")
        self.text_area.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()