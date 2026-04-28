
# ui/base_window.py

import sys
import os

# Proje kökünü path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from config import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH, BG_COLOR  # ← Düz import

class BaseWindow(tk.Tk):
    
    
    def __init__(self, title=WINDOW_TITLE, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        """BaseWindow sınıfını başlat"""
        super().__init__()
        
        # Özellikler
        self.title_text = title
        self.width = width
        self.height = height
        self.background_color = BG_COLOR
        
        # Pencereyi ayarla
        self.title(self.title_text)
        self.geometry(f"{self.width}x{self.height}")
        self.configure(bg=self.background_color)
        self.resizable(False, False)

    def open_window(self):
        """Pencereyi aç"""
        self.mainloop()

    def close_window(self):
        """Pencereyi kapat"""
        self.destroy()