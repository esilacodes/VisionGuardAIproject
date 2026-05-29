

import customtkinter as ctk
from gui.shared.components import TextInputField, Button, Link
from gui.shared.message_box import MessageBox
from backend.database import db
from config.settings import color, font

class LoginTab:
    def __init__(self, master, on_login=None):
        self.on_login = on_login
        
        # Main frame
        self.frame = ctk.CTkFrame(master, fg_color=color['white'])
        
        # Scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.frame,
            fg_color=color['white'],
            label_text=""
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=50, pady=(15, 20))
        
        # Title
        ctk.CTkLabel(
            self.scroll_frame,
            text="Sign In",
            font=('Arial', 34, 'bold'),
            text_color=color['primary']
        ).pack(pady=(0, 15), anchor='w')
        
        # Description with link
        desc_frame = ctk.CTkFrame(self.scroll_frame, fg_color=color['white'])
        desc_frame.pack(pady=(0, 15), anchor='w', fill='x')
        
        ctk.CTkLabel(
            desc_frame,
            text="Don’t have an account?",
            font=font['label'],
            text_color=color['text_light']
        ).pack(side='left')
        
        self.signup_link = ctk.CTkLabel(
            desc_frame,
            text=" Sign up",
            font=font['label'],
            text_color=color['primary'],
            cursor="hand2"
        )
        self.signup_link.pack(side='left')
        
        # Inputs
        self.name = TextInputField(self.scroll_frame, "your username", icon_text="👤")
        self.password = TextInputField(self.scroll_frame, "password", show="*", icon_text="🔒")
        
        # Button
        self.signin_btn = Button(self.scroll_frame, "Sign In", command=self._handle_login)
        
        # Spacing
        ctk.CTkFrame(self.scroll_frame, fg_color=color['white'], height=50).pack()
    
    def _handle_login(self):
        """Login button tıklandığında"""
        username = self.name.get_value()
        password = self.password.get_value()
        
        # Database'de kontrol et
        success, message = db.login_user(username, password)
        
        if success:
            db.set_current_user(username)
            MessageBox.show_success(self.frame.winfo_toplevel(), "succes", message)
            # Callback'i çağır
            if self.on_login:
                self.on_login()
        else:
            MessageBox.show_error(self.frame.winfo_toplevel(), "error", message)