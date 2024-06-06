import os
import openai
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import json

def generate_response(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    return response.choices[0].message.content.strip()

class PowerShellGPT:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerShellGPT")
        self.root.attributes('-fullscreen', True)
        
        # Ask for OpenAI API key
        self.api_key = simpledialog.askstring("OpenAI API Key", "Please enter your OpenAI API key:", show='*')
        if self.api_key is None or self.api_key.strip() == "":
            tk.messagebox.showerror("Error", "API key is required to use this application.")
            root.destroy()
            return
        
        # Setting up the UI
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg='black', fg='white', font=('Consolas', 12))
        self.text_area.pack(expand=1, fill="both")
        self.text_area.bind("<Return>", self.send_command)
        
        self.prompt = [{"role": "system", "content": "You are a helpful assistant that mimics a PowerShell console."}]
        
    def send_command(self, event):
        user_command = self.text_area.get("end-2l", "end-1c").strip()
        if user_command:
            self.text_area.insert(tk.END, "\n")
            self.prompt.append({"role": "user", "content": user_command})
            
            ai_response = generate_response(self.prompt, self.api_key)
            
            self.prompt.append({"role": "assistant", "content": ai_response})
            self.text_area.insert(tk.END, ai_response + "\n")
            self.text_area.see(tk.END)
        
        return "break"

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerShellGPT(root)
    root.mainloop()
