


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from config import (
    BUTTON_FONT, BUTTON_COLOR, BUTTON_HEIGHT, BUTTON_TEXT_COLOR,
    LABEL_FONT, TITLE_FONT, ENTRY_WIDTH, BUTTON_WIDTH,
    ERROR_COLOR, SUCCESS_COLOR
)
from ui.basewindow import BaseWindow
from services.validation_service import CheckValid
from ui.main_panel import MainPanel
class LoginScreen(BaseWindow):
    
    
    def __init__(self):
        super().__init__(title="Motion Detection - Login", width=500, height=600)
        self.service=CheckValid()
        self.create_widgets()
        
    
    def create_widgets(self):
        
        # main farme(clear grey)
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # title
        title_label = tk.Label(
            main_frame,
            text="Motion Detection System",
            font=TITLE_FONT,
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=10)
        
        # Nested Frame (dark gri)
        input_frame = tk.Frame(main_frame, bg="#e0e0e0")
        input_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # loading imagine
        try:
            # fing path
            image_path = os.path.join(os.path.dirname(__file__), "resim.png")
            
            # check imagine
            if os.path.exists(image_path):
                self.image = tk.PhotoImage(file=image_path)
                # smallset imagine
                self.image = self.image.subsample(2, 2)
                
                image_label = tk.Label(
                    input_frame,
                    image=self.image,
                    bg="#f0f0f0"
                )
                image_label.pack(pady=10)
            else:
                print(f"❌ imagine could not fingind: {image_path}")
        except Exception as e:
            print(f"❌ error imagine cold not loading : {e}")
        

        #username label
        username_label = tk.Label(
            input_frame,
            text="Username:",
            font=LABEL_FONT,
            bg="#e0e0e0",  
            fg="#333333"
        )
        username_label.pack(anchor="w", pady=5, padx=10)
        
        # Username Entry
        self.username_entry = tk.Entry(
            input_frame,
            width=ENTRY_WIDTH,
            font=LABEL_FONT
        )
        self.username_entry.pack(pady=5, padx=10)
        
        # Password Label
        password_label = tk.Label(
            input_frame,
            text="Password:",
            font=LABEL_FONT,
            bg="#e0e0e0",  
            fg="#333333"
        )
        password_label.pack(anchor="w", pady=5, padx=10)
        
        # Password Entry
        self.password_entry = tk.Entry(
            input_frame,
            width=ENTRY_WIDTH,
            font=LABEL_FONT,
            show="*"  
        )
        self.password_entry.pack(pady=5, padx=10)
        
        # log in frame
        button_frame = tk.Frame(input_frame, bg="#e0e0e0")
        button_frame.pack(pady=20)
        
        # Login Button
        login_button = tk.Button(
            button_frame,
            text="Login",
            font=BUTTON_FONT,
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            width=BUTTON_WIDTH,
            height=2,
            command=self.on_login_button_clicked
        )
        login_button.pack(padx=10, pady=10)
    
    def on_login_button_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        
        if self.service.check_credentials(username,password):
            # Başarılı giriş
            messagebox.showinfo(
                "Başarı",
                f"Hoşgeldiniz {username}!"
            )
            self.clear_fields()
            self.main=MainPanel()
            self.close_window()
            self.main.open_window()
            
        else:
            # Başarısız giriş
            error_message = self.service.get_error_message()
            
            messagebox.showerror(
                "Hata",
                error_message  # ← Hata mesajını göster
            ) 
            self.clear_fields()
            
    
    def clear_fields(self):
        
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
   



