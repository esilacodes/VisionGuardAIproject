import tkinter as tk

class BasePage:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.setup_page()
        self.render()
    
    def setup_page(self):
        # Subclass'lar override edecek
        pass
    
    def render(self):
        # Subclass'lar override edecek
        pass
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
